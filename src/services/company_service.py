from src.models.company import Company
from src.models.post import Sentiment
from src.patterns.decorator.sponsered_user import SponsoredUser
from src.patterns.decorator.verified_user import VerifiedUser


class CompanyService:
    # Service for managing companies and sponsorships

    # Singleton pattern
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CompanyService()
        return cls._instance

    def __init__(self):
        self._companies = self._create_default_companies()

    def _create_default_companies(self):
        return [
            Company(
                "EcoTech",
                "Sustainable technology solutions for a greener future",
                political_leaning=Sentiment.LEFT,
            ),
            Company(
                "Global Investments",
                "A leading investment firm with a diverse portfolio",
                political_leaning=Sentiment.RIGHT,
            ),
            Company(
                "Community First",
                "Empowering local communities through grassroots initiatives",
                political_leaning=Sentiment.LEFT,
            ),
            Company(
                "Heritage Brands",
                "Preserving traditional values through quality products",
                political_leaning=Sentiment.RIGHT,
            ),
            Company(
                "Universal Media",
                "Bringing the world together through unbiased news coverage",
                political_leaning=Sentiment.NEUTRAL,
            ),
            Company(
                "Future Technologies",
                "Innovative solutions for tomorrow's challenges",
                political_leaning=Sentiment.NEUTRAL,
            ),
        ]

    @property
    def companies(self):
        return self._companies

    def get_company_by_name(self, name):
        for company in self._companies:
            if company.name.lower() == name.lower():
                return company
        return None

    def add_company(self, company):
        self._companies.append(company)

    def apply_for_sponsorship(self, user, company):
        # Check eligibility and return (success, message) tuple

        # Check if already sponsored
        if isinstance(user, SponsoredUser) or hasattr(user, "company_name"):
            company_name = getattr(user, "company_name", "another company")
            return (
                False,
                f"You can only have one sponsorship at a time. You are currently sponsored by {company_name}.",
            )

        # Must be verified
        if not isinstance(user, VerifiedUser):
            return False, "You must be verified to apply for sponsorships."

        posts = user.posts
        if not posts:
            user_sentiment = Sentiment.NEUTRAL
        else:
            # Determine dominant sentiment from posts
            sentiment_counts = {
                Sentiment.LEFT: 0,
                Sentiment.RIGHT: 0,
                Sentiment.NEUTRAL: 0,
            }

            for post in posts:
                sentiment_counts[post.sentiment] += 1

            max_sentiment = max(sentiment_counts, key=sentiment_counts.get)

            # If tied, use NEUTRAL
            if (
                list(sentiment_counts.values()).count(
                    sentiment_counts[max_sentiment]
                )
                > 1
            ):
                user_sentiment = Sentiment.NEUTRAL
            else:
                user_sentiment = max_sentiment

        # Check for political alignment
        if (
            company.political_leaning == Sentiment.NEUTRAL
            or company.political_leaning == user_sentiment
        ):
            self.logger.info(
                f"User {user.handle} applied for sponsorship from {company.name}"
            )
            return True, "Sponsorship application successful!"
        else:
            return (
                False,
                f"Your content doesn't align with {company.name}'s values.",
            )

    def sponsor_user(self, user, company):
        success, message = self.apply_for_sponsorship(user, company)

        if success:
            # Apply decorator and add to company's list
            sponsored_user = SponsoredUser(user, company.name)
            company.sponsor_user(sponsored_user)
            return sponsored_user, f"You are now sponsored by {company.name}!"

        return user, message

    def remove_sponsorship(self, user):
        if not hasattr(user, "company_name"):
            return user, "You don't have any active sponsorships."

        company_name = user.company_name

        # Unwrap the user from decorators
        if isinstance(user, VerifiedUser) and hasattr(
            user._user, "company_name"
        ):
            unwrapped_user = VerifiedUser(user._user._user)
        elif hasattr(user, "_user"):
            unwrapped_user = user._user
        else:
            return user, "Error removing sponsorship."

        # Remove from company's list
        for company in self._companies:
            if company.name == company_name:
                company.remove_sponsorship(user)
                break

        return (
            unwrapped_user,
            f"Your sponsorship with {company_name} has been terminated.",
        )

    def check_content_alignment(self, user, post=None):
        # Check if user's content aligns with sponsor's values

        if not hasattr(user, "company_name"):
            return None

        company_name = user.company_name
        company = next(
            (c for c in self.companies if c.name == company_name), None
        )

        if not company:
            return None

        company_leaning = company.political_leaning
        user_posts = getattr(user, "posts", [])

        if post:
            all_posts = user_posts + [post]
        else:
            all_posts = user_posts

        if not all_posts:
            return None

        # Track misaligned posts count
        if isinstance(user, VerifiedUser) and hasattr(
            user._user, "company_name"
        ):
            misaligned_count = getattr(user._user, "_misaligned_posts", 0)
        else:
            misaligned_count = getattr(user, "_misaligned_posts", 0)

        # Check for political conflict
        if post and post.sentiment != Sentiment.NEUTRAL:
            if (
                company_leaning == Sentiment.LEFT
                and post.sentiment == Sentiment.RIGHT
            ) or (
                company_leaning == Sentiment.RIGHT
                and post.sentiment == Sentiment.LEFT
            ):
                misaligned_count += 1

                # Store the count
                if isinstance(user, VerifiedUser) and hasattr(
                    user._user, "company_name"
                ):
                    setattr(user._user, "_misaligned_posts", misaligned_count)
                else:
                    setattr(user, "_misaligned_posts", misaligned_count)

                # Terminate after 3 strikes
                if misaligned_count >= 3:
                    if isinstance(user, VerifiedUser) and hasattr(
                        user._user, "company_name"
                    ):
                        setattr(user._user, "_misaligned_posts", 0)
                    else:
                        setattr(user, "_misaligned_posts", 0)

                    return f"Your sponsorship has been terminated after {misaligned_count} posts that conflict with your sponsor's values."
                else:
                    return f"Warning: This is your {misaligned_count}/3 post that conflicts with your sponsor's values. Further conflicts may result in termination of your sponsorship."

        return None

    def on_post_created(self, user, post):
        # Handle post creation for sponsored users

        if not (
            hasattr(user, "company_name") or isinstance(user, SponsoredUser)
        ):
            return user, None

        result = self.check_content_alignment(user, post)

        # Handle sponsorship termination
        if result and "terminated" in result.lower():
            company_name = getattr(user, "company_name", "your sponsor")
            updated_user, removal_message = self.remove_sponsorship(user)

            if not hasattr(updated_user, "company_name"):
                return (
                    updated_user,
                    f"Your sponsorship with {company_name} has been terminated due to repeated content that conflicts with their values.",
                )
            else:
                return (
                    user,
                    "Warning: Your content conflicts with your sponsor's values.",
                )

        return user, result
