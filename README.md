# Social Media Influencer Simulator

A PyQt6-based social media simulator application that demonstrates various software design patterns and principles.

## Features

- User profile management
- Post creation with sentiment analysis using Google Gemini AI
- Follower management with political alignment
- Interactive feed display
- Post interactions (likes, comments, shares)

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

## Running the Application

To run the application, execute:

```bash
python main.py
```

## Application Structure

### Models
- `src/models/`: Contains the data models for the application
  - `user.py`: User model representing a social media account
  - `post.py`: Post model representing a social media post with sentiment analysis
  - `follower.py`: Follower model representing a user who follows another user
  - `sentiment.py`: Sentiment enum representing the political sentiment of content

### Views
- `src/views/`: Contains the PyQt6 views for the application
  - `main_window.py`: Main window for the application
  - `social_media_view.py`: Main view for the social media application
  - `user_profile_widget.py`: Widget for displaying and editing user profile
  - `create_post_widget.py`: Widget for creating new posts
  - `feed_widget.py`: Widget for displaying the post feed
  - `post_widget.py`: Widget for displaying individual posts
  - `follower_list_widget.py`: Widget for displaying followers

### Controllers
- `src/controllers/`: Contains the controllers for the application
  - `main_controller.py`: Main controller for the application
  - `user_controller.py`: Controller for user-related operations
  - `post_controller.py`: Controller for post-related operations
  - `follower_controller.py`: Controller for follower-related operations

### Services
- `src/services/`: Contains services used by the application
  - `sentiment_service.py`: Service for analyzing sentiment using Google Gemini AI
  - `logger_service.py`: Service for logging application events
  - `logger.py`: Logger implementation

### Design Patterns
- `src/patterns/`: Contains implementations of various design patterns
  - `command/`: Command pattern implementation for post interactions
  - `factory/`: Factory pattern implementation for post creation
  - `builders/`: Builder pattern implementation for post creation
  - `decorators/`: Decorator pattern implementation for user types
  - `interfaces/`: Interfaces for the design patterns
  - `interceptors/`: Interceptor pattern implementation
  - `controllers/`: Additional controller patterns

## Usage

The application has three main tabs:

1. **Profile**: View and edit your user profile
2. **Feed**: Create new posts and view your existing posts
3. **Followers**: View your followers and their political alignment

When creating a post, you can specify:
- Post content
- Sentiment (LEFT, RIGHT, or NEUTRAL)
- Optional image path

## License

MIT 