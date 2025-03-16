from datetime import datetime

from PyQt6.QtWidgets import QMessageBox

from src.controllers.follower_controller import FollowerController
from src.controllers.post_controller import PostController
from src.models.post import Comment, Sentiment
from src.models.user import User
from src.patterns.decorator.verified_user import VerifiedUser
from src.patterns.factory.post_builder_factory import PostBuilderFactory
from src.patterns.interceptors.dispatcher import Dispatcher
from src.patterns.interceptors.inappropriate_content_filter import (
    InappropriateContentFilter,
)
from src.patterns.interceptors.post_creation_interceptor import (
    PostCreationInterceptor,
)
from src.patterns.interceptors.spam_filter import SpamFilter
from src.services.logger_service import LoggerService


class UserController:
    """Controller for User model operations."""

    def __init__(self, user=None):
        """Initialize with a user model."""
        self.user = user or User("default_user", "Default bio")
        self.logger = LoggerService.get_logger()
        self.follower_controller = FollowerController()
        self.post_controller = (
            PostController()
        )  # Make sure this is initialized

        # Initialize the dispatcher and add interceptors
        self.dispatcher = Dispatcher()
        self.dispatcher.add_interceptor(PostCreationInterceptor())
        self.dispatcher.add_interceptor(SpamFilter())
        self.dispatcher.add_interceptor(InappropriateContentFilter())

    def create_post(self, content, image_path=None, parent_widget=None):
        """
        Create a new post for the user.

        Args:
            content: The content of the post
            image_path: Optional path to an image to include in the post
            parent_widget: Optional parent widget for displaying warning dialogs

        Returns:
            The created post, or None if creation failed
        """
        # Use the factory to create the appropriate post builder
        factory = PostBuilderFactory()

        # Determine the post type based on whether an image is provided
        post_type = "image" if image_path else "text"

        # Get the appropriate builder
        builder = factory.get_builder(post_type)

        # Build the post
        builder.set_content(content)
        builder.set_author(self.user)

        if image_path:
            builder.set_image_path(image_path)

        # Get the post from the builder
        post = builder.build()

        # Store reference to dispatcher in post for warning collection
        post._dispatcher = self.dispatcher

        # Process the post through the interceptor chain
        self.dispatcher.process_post(post)

        # Check if there are any warnings
        warnings = self.dispatcher.get_warnings()
        if warnings and parent_widget:
            # Display warnings to the user
            warning_text = "\n\n".join(warnings)

            # Create a message box with the warnings
            msg_box = QMessageBox(parent_widget)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Post Warning")
            msg_box.setText("Your post has the following issues:")
            msg_box.setInformativeText(warning_text)
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Ok
                | QMessageBox.StandardButton.Cancel
            )
            msg_box.setDefaultButton(QMessageBox.StandardButton.Cancel)

            # Show the message box and get the user's response
            response = msg_box.exec()

            # If the user clicked Cancel, abort post creation
            if response == QMessageBox.StandardButton.Cancel:
                self.logger.info(
                    "User cancelled post creation after seeing warnings"
                )
                return None

            # User clicked OK, proceed with post creation despite warnings
            self.logger.info(
                "User chose to proceed with post creation despite warnings"
            )

        # Only proceed if the post is valid after interceptor processing
        if not hasattr(post, "is_valid") or post.is_valid:
            # Analyze sentiment and set it on the post
            sentiment = self.post_controller.analyze_sentiment(content)
            post.sentiment = sentiment

            # Add the post to the user's posts
            self.user._posts.append(post)

            # Emit the post_created signal
            self.user.post_created.emit(post)

            # Log the post creation
            self.logger.info(
                f"User {self.user.handle} created a post: {content[:30]}..."
            )

            # Generate new followers based on the post
            initial_follower_count = self.user._follower_count
            new_followers = self.generate_new_followers(post)

            if new_followers > 0:
                self.logger.info(
                    f"Post attracted {new_followers} new followers"
                )

                # Use the controller's notify_followers method
                self.notify_followers(post)

                # Add new followers as observers
                for follower in self.user._followers[initial_follower_count:]:
                    self.user.attach(follower, post)
                    self.logger.debug(
                        f"Added follower {follower.handle} as observer"
                    )

            return post
        else:
            # Post was invalid, log the reason and return None
            self.logger.warning("Post creation failed: Post validation failed")
            return None

    def add_follower(self, follower, post=None):
        """Add a follower to the user."""
        if follower not in self.user._followers:
            self.user._followers.append(follower)
            self.user._follower_count += 1
            self.user.follower_added.emit(follower)

            # Add follower as observer
            self.user.attach(follower, post)

            # If a post attracted this follower, make them interact with it
            if post:
                follower.interact_with_post(post)

            # Log the follower addition
            self.logger.info(
                f"User {self.user.handle} gained a follower: {follower.handle}"
            )

            # Check if the user has reached the verification threshold
            if (
                self.user._follower_count >= self.user.VERIFICATION_THRESHOLD
                and not isinstance(self.user, VerifiedUser)
            ):
                # Apply the VerifiedUser decorator
                self.logger.info(
                    f"User {
                        self.user.handle} has reached {
                        self.user.VERIFICATION_THRESHOLD} followers. Applying verified status."
                )
                self.user = VerifiedUser(self.user)

                # Log the verification
                self.logger.info(f"User {self.user.handle} is now verified!")

                # Show verification popup
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle("Account Verified!")
                msg_box.setText(
                    "Congratulations! Your account has been verified!"
                )
                msg_box.setInformativeText(
                    f"You've reached {
                        self.user.VERIFICATION_THRESHOLD} followers and are now a verified user. Your handle will now show a verification badge (✔️)."
                )
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()

                # Update the main controller's reference to the user
                from src.controllers.main_controller import MainController

                main_controller = MainController.get_instance()
                if main_controller:
                    main_controller.user = self.user
                    # Update the UI to reflect the verified status
                    if (
                        hasattr(main_controller, "main_window")
                        and main_controller.main_window
                    ):
                        main_controller.main_window.update_user_profile()

    def remove_follower(self, follower):
        """Remove a follower from the user."""
        if follower in self.user._followers:
            self.user._followers.remove(follower)
            self.user._follower_count -= 1
            self.user.follower_removed.emit(follower)

            # Detach follower as observer
            self.user.detach(follower)

            # Log the follower removal
            self.logger.info(
                f"User {self.user.handle} lost a follower: {follower.handle}"
            )

    def generate_new_followers(self, post, count=None):
        """
        Generate new followers based on a post.

        Args:
            post: The post that might attract followers.
            count: Optional number of followers to try to generate. If None, uses a default value.

        Returns:
            Number of new followers gained.
        """
        if count is None:
            # Default to a number based on current follower count
            # More followers = more potential new followers
            base_count = 5
            follower_bonus = min(15, self.user._follower_count // 10)
            count = base_count + follower_bonus

        # Calculate follow chance based on post sentiment
        follow_chance = self.follower_controller.calculate_follow_chance(
            self.user, post.sentiment
        )

        # Generate potential followers
        potential_followers = (
            self.follower_controller.generate_potential_followers(post, count)
        )

        # Count how many actually follow
        new_followers = 0

        for follower in potential_followers:
            if self.follower_controller.should_follow(
                follower, post, follow_chance
            ):
                self.add_follower(follower, post)
                self.follower_controller.add_follow_comment(follower, post)
                new_followers += 1

        self.logger.info(
            f"Generated {new_followers} new followers from {count} potential followers"
        )
        return new_followers

    def update_reputation(self, initial_followers, post):
        """Update reputation based on follower losses from a post."""
        if self.user._follower_count < initial_followers:
            lost_followers = initial_followers - self.user._follower_count
            self.user._recent_follower_losses += lost_followers
            self.user.reputation_changed.emit(
                self.user._recent_follower_losses
            )

            self.logger.warning(
                "Lost %d followers. Total recent losses: %d",
                lost_followers,
                self.user._recent_follower_losses,
            )

            if (
                self.user._recent_follower_losses
                >= self.user.REPUTATION_WARNING_THRESHOLD
            ):
                post._add_comment(
                    Comment(
                        "Your recent posts are driving followers away...",
                        Sentiment.NEUTRAL,
                        "system_warning",
                    )
                )
                self.logger.warning(
                    "Reputation warning threshold reached: %d",
                    self.user._recent_follower_losses,
                )

            return lost_followers
        return 0

    def update_reputation_recovery(self, current_time=None):
        """Recover reputation over time."""
        if current_time is None:
            current_time = (
                datetime.now().timestamp() * 1000
            )  # Convert to milliseconds

        if (
            current_time - self.user._last_reputation_check
            >= self.user.REPUTATION_RECOVERY_DELAY
        ):
            if self.user._recent_follower_losses > 0:
                old_losses = self.user._recent_follower_losses
                self.user._recent_follower_losses = max(
                    0, self.user._recent_follower_losses - 1
                )
                self.user.reputation_changed.emit(
                    self.user._recent_follower_losses
                )
                self.logger.info(
                    "Reputation recovered: losses decreased from %d to %d",
                    old_losses,
                    self.user._recent_follower_losses,
                )
            self.user._last_reputation_check = current_time

    def edit_post(self, post, new_content=None, new_image_path=None):
        """Edit a post."""
        if post in self.user._posts:
            if new_content:
                post.content = new_content
            if new_image_path:
                post.image_path = new_image_path

            self.logger.info(
                f"User {self.user.handle} edited a post: {post.content[:30]}..."
            )

    def delete_post(self, post):
        """Delete a post."""
        if post in self.user._posts:
            self.user._posts.remove(post)
            self.logger.info(
                f"User {self.user.handle} deleted a post: {post.content[:30]}..."
            )

    def update_profile(self, handle=None, bio=None, profile_picture_path=None):
        """Update the user's profile."""
        if handle:
            self.user.handle = handle
        if bio:
            self.user.bio = bio
        if profile_picture_path:
            self.user.profile_picture_path = profile_picture_path

        self.logger.info(
            f"User profile updated: handle={self.user.handle}, bio={self.user.bio[:30]}..."
        )

        # Return the updated user
        return self.user

    def notify_followers(self, post):
        """
        Notify all followers about a new post.

        Args:
            post: The post to notify followers about.

        Returns:
            Number of followers who unfollowed due to the post.
        """
        unfollowed_count = 0

        # Use a copy of the followers list to avoid modification during
        # iteration
        for follower in self.user._followers.copy():
            # Use the follower controller to update the follower
            if self.follower_controller.update_follower(
                follower, self.user, post
            ):
                # If the follower unfollowed, count it and remove them
                unfollowed_count += 1
                self.remove_follower(follower)
            else:
                self.logger.debug(
                    f"Notified follower {follower.handle} about post"
                )

        if unfollowed_count > 0:
            self.logger.info(
                f"{unfollowed_count} followers unfollowed due to post"
            )

        return unfollowed_count
