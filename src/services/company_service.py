from src.models.company import Company
from src.models.post import Sentiment
from src.patterns.decorator.sponsered_user import SponsoredUser
from src.patterns.decorator.verified_user import VerifiedUser


class CompanyService:
    """Service for managing companies and sponsorships."""
    
    # Singleton pattern
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CompanyService()
        return cls._instance
    
    def __init__(self):
        """Initialize the company service with some default companies."""
        self._companies = self._create_default_companies()
    
    def _create_default_companies(self):
        """Create a list of default companies."""
        return [
            Company("EcoTech", "Sustainable technology solutions for a greener future", 
                   political_leaning=Sentiment.LEFT),
            Company("Global Investments", "A leading investment firm with a diverse portfolio", 
                   political_leaning=Sentiment.RIGHT),
            Company("Community First", "Empowering local communities through grassroots initiatives", 
                   political_leaning=Sentiment.LEFT),
            Company("Heritage Brands", "Preserving traditional values through quality products", 
                   political_leaning=Sentiment.RIGHT),
            Company("Universal Media", "Bringing the world together through unbiased news coverage", 
                   political_leaning=Sentiment.NEUTRAL),
            Company("Future Technologies", "Innovative solutions for tomorrow's challenges", 
                   political_leaning=Sentiment.NEUTRAL),
        ]
    
    @property
    def companies(self):
        """Get the list of companies."""
        return self._companies
    
    def get_company_by_name(self, name):
        """Get a company by name."""
        for company in self._companies:
            if company.name.lower() == name.lower():
                return company
        return None
    
    def add_company(self, company):
        """Add a new company."""
        self._companies.append(company)
    
    def apply_for_sponsorship(self, user, company):
        """Apply for sponsorship from a company.
        
        Returns:
            tuple: (success, message) where success is a boolean indicating if the application
                  was successful, and message is a string explaining the result.
        """
        # Check if user is already sponsored by another company (check this first)
        # Use hasattr to check for company_name attribute which is unique to SponsoredUser
        if isinstance(user, SponsoredUser) or hasattr(user, 'company_name'):
            company_name = getattr(user, 'company_name', 'another company')
            return False, f"You can only have one sponsorship at a time. You are currently sponsored by {company_name}."
        
        # Check if user is verified
        if not isinstance(user, VerifiedUser):
            return False, "You must be verified to apply for sponsorships."
        
        posts = user.posts
        if not posts:
            # If no posts, assume neutral
            user_sentiment = Sentiment.NEUTRAL
        else:
            # Count sentiments across all posts
            sentiment_counts = {
                Sentiment.LEFT: 0,
                Sentiment.RIGHT: 0,
                Sentiment.NEUTRAL: 0
            }
            
            for post in posts:
                sentiment_counts[post.sentiment] += 1
            
            # Determine dominant sentiment (or NEUTRAL if tied)
            max_sentiment = max(sentiment_counts, key=sentiment_counts.get)
            
            # If there's a tie, use NEUTRAL
            if list(sentiment_counts.values()).count(sentiment_counts[max_sentiment]) > 1:
                user_sentiment = Sentiment.NEUTRAL
            else:
                user_sentiment = max_sentiment
        
        # Check for alignment (neutral companies accept anyone)
        if company.political_leaning == Sentiment.NEUTRAL or company.political_leaning == user_sentiment:
            return True, "Sponsorship application successful!"
        else:
            return False, f"Your content doesn't align with {company.name}'s values."
    
    def sponsor_user(self, user, company):
        """Apply the sponsorship decorator to a user.
        
        Returns:
            tuple: (new_user, message) where new_user is the decorated user object
                  and message is a string explaining the result.
        """
        # First check if the application would be successful
        success, message = self.apply_for_sponsorship(user, company)
        
        if success:
            # Apply the SponsoredUser decorator
            sponsored_user = SponsoredUser(user, company.name)
            
            # Add the user to the company's sponsored users list
            company.sponsor_user(sponsored_user)
            
            return sponsored_user, f"You are now sponsored by {company.name}!"
        
        return user, message
    
    def remove_sponsorship(self, user):
        """Remove sponsorship from a user.
        
        Returns:
            tuple: (new_user, message) where new_user is the undecorated user object
                  and message is a string explaining the result.
        """
        print(f"Attempting to remove sponsorship from user: {user}")
        
        # Check if the user has a company_name attribute, which indicates it's sponsored
        if not hasattr(user, 'company_name'):
            print(f"User does not have company_name attribute: {type(user)}")
            return user, "You don't have any active sponsorships."
        
        # Store the company name before unwrapping
        company_name = user.company_name
        print(f"Found company name: {company_name}")
        
        # Get the original user by unwrapping the decorated user
        # If the user is a VerifiedUser with a SponsoredUser inside
        if isinstance(user, VerifiedUser) and hasattr(user._user, 'company_name'):
            print(f"User is a VerifiedUser with a SponsoredUser inside")
            # Keep the VerifiedUser wrapper but remove the SponsoredUser wrapper
            unwrapped_user = VerifiedUser(user._user._user)
            print(f"Unwrapped to VerifiedUser with inner user: {unwrapped_user}")
        # If the user is directly a SponsoredUser
        elif hasattr(user, '_user'):
            # Get the inner user
            unwrapped_user = user._user
            print(f"Unwrapped to inner user: {unwrapped_user}")
        else:
            # Shouldn't happen, but just in case
            print(f"User has company_name but no _user attribute: {type(user)}")
            return user, "Error removing sponsorship."
        
        # Find the company and remove the user from its sponsored users list
        for company in self._companies:
            if company.name == company_name:
                print(f"Found company {company_name}, removing user from sponsored list")
                company.remove_sponsorship(user)
                break
        
        print(f"Sponsorship removed, returning unwrapped user: {unwrapped_user}")
        return unwrapped_user, f"Your sponsorship with {company_name} has been terminated."
    
    def check_content_alignment(self, user, post=None):
        """
        Check if the user's content aligns with their sponsor's values.
        If a post is provided, it will be included in the alignment check.
        Returns a message if sponsorship is affected.
        """
        # Check if the user is sponsored
        if not hasattr(user, 'company_name'):
            return None
            
        # Get the company's political leaning
        company_name = user.company_name
        company = next((c for c in self.companies if c.name == company_name), None)
        
        if not company:
            return None
            
        # Get the company's political leaning
        company_leaning = company.political_leaning
        
        # Debug logging
        print(f"Company: {company_name}, Leaning: {company_leaning.name}")
        
        # Get the user's posts
        user_posts = getattr(user, 'posts', [])
        
        # Include the new post if provided
        if post:
            # Create a temporary list with the new post included
            all_posts = user_posts + [post]
        else:
            all_posts = user_posts
            
        # If there are no posts, alignment is fine
        if not all_posts:
            return None
            
        # Count misaligned posts
        misaligned_count = getattr(user, '_misaligned_posts', 0)
        
        # Debug logging
        print(f"Current misaligned posts count: {misaligned_count}")
        
        # Check if the new post is misaligned
        if post and post.sentiment != Sentiment.NEUTRAL:
            if (company_leaning == Sentiment.LEFT and post.sentiment == Sentiment.RIGHT) or \
               (company_leaning == Sentiment.RIGHT and post.sentiment == Sentiment.LEFT):
                # Increment misaligned posts count
                misaligned_count += 1
                
                # Debug logging
                print(f"Post is misaligned! New count: {misaligned_count}")
                
                # Store the count on the user object
                setattr(user, '_misaligned_posts', misaligned_count)
                
                # Check if we've reached the threshold for termination (3 misaligned posts)
                if misaligned_count >= 3:
                    # Reset the counter
                    setattr(user, '_misaligned_posts', 0)
                    
                    # Debug logging
                    print(f"Reached termination threshold! Sponsorship will be terminated.")
                    
                    # Return termination message
                    return f"Your sponsorship has been terminated after {misaligned_count} posts that conflict with your sponsor's values."
                else:
                    # Debug logging
                    print(f"Warning issued for misaligned post ({misaligned_count}/3)")
                    
                    # Return warning message
                    return f"Warning: This is your {misaligned_count}/3 post that conflicts with your sponsor's values. Further conflicts may result in termination of your sponsorship."
        
        # If we get here, the post is aligned or neutral
        return None
    
    def on_post_created(self, user, post):
        """
        Handle post creation events for sponsored users.
        Check if the post aligns with the company's values.
        Return the updated user and a message if sponsorship was affected.
        """
        # Check if the user is sponsored
        if not (hasattr(user, 'company_name') or isinstance(user, SponsoredUser)):
            return user, None
            
        # Get the alignment check result
        result = self.check_content_alignment(user, post)
        
        # Debug logging
        print(f"Alignment check result: {result}")
        print(f"Post sentiment: {post.sentiment.name}")
        print(f"User misaligned posts: {getattr(user, '_misaligned_posts', 0)}")
        
        # If sponsorship was terminated
        if result and "terminated" in result.lower():
            # Store company name before removing sponsorship
            company_name = getattr(user, 'company_name', 'your sponsor')
            
            print(f"Terminating sponsorship with {company_name}")
            
            # Remove the sponsorship - this returns a tuple (user, message)
            updated_user, removal_message = self.remove_sponsorship(user)
            
            # Debug logging
            print(f"After removal - updated user type: {type(updated_user)}")
            print(f"Is still sponsored: {hasattr(updated_user, 'company_name') or isinstance(updated_user, SponsoredUser)}")
            
            # Double check that sponsorship was actually removed
            if not hasattr(updated_user, 'company_name'):
                print(f"Sponsorship successfully removed")
                return updated_user, f"Your sponsorship with {company_name} has been terminated due to repeated content that conflicts with their values."
            else:
                # Error case - sponsorship removal failed
                print(f"Error: Sponsorship removal failed, user still has company_name: {getattr(updated_user, 'company_name', None)}")
                return user, "Warning: Your content conflicts with your sponsor's values."
                
        return user, result 