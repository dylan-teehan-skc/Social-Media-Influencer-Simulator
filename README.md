# Social Media Simulator

A simple PyQt5-based social media simulator application that demonstrates the use of the models in the `src/models` directory.

## Features

- User profile management
- Post creation with sentiment analysis
- Follower management
- Feed display

## Requirements

- Python 3.6+
- PyQt5
- python-dotenv
- pygame

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, execute:

```bash
python -m src.main
```

## Application Structure

- `src/models/`: Contains the data models for the application
  - `user.py`: User model representing a social media account
  - `post.py`: Post model representing a social media post
  - `follower.py`: Follower model representing a user who follows another user
  - `sentiment.py`: Sentiment enum representing the political sentiment of content

- `src/views/`: Contains the PyQt5 views for the application
  - `social_media_view.py`: Main view for the social media application

## Usage

The application has three main tabs:

1. **Profile**: View and edit your user profile
2. **Feed**: Create new posts and view your existing posts
3. **Followers**: View your followers

When creating a post, you can specify:
- Post content
- Sentiment (LEFT, RIGHT, or NEUTRAL)
- Optional image path

## License

MIT 