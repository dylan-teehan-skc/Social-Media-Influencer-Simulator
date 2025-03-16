# Social Media Influencer Simulator

A PyQt6-based social media simulator application that demonstrates various software design patterns and principles.

## Overview

This application simulates a social media platform where users can create profiles, make posts with political sentiment analysis, gain followers, and interact with content. It serves as a practical demonstration of software engineering concepts including MVC architecture and various design patterns.

## Features

- **User Profile Management**: Create and customize your social media persona
- **Post Creation**: Create text and image posts with sentiment analysis
- **Sentiment Analysis**: Uses Google Gemini AI to analyze political sentiment of content
- **Follower System**: Gain followers with different political alignments
- **Interactive Feed**: View and interact with posts in your feed
- **Post Interactions**: Like, comment, and share posts
- **Company Sponsorships**: Get sponsored by companies with different political leanings
- **News & Trending**: View news and apply for company sponsorships
- **Theme Switching**: Toggle between light and dark themes

## Architecture

```mermaid
%%{init: {
  'theme': 'base', 
  'themeVariables': { 
    'primaryColor': '#f0f8ff', 
    'primaryTextColor': '#000000', 
    'primaryBorderColor': '#7C0200', 
    'lineColor': '#000000', 
    'secondaryColor': '#f5f5f5', 
    'tertiaryColor': '#fff0f0',
    'background': '#e6f2ff'
  }
}}%%
graph TD
    %% Main Application Flow
    subgraph Application["Application"]
        Main[main.py] --> MainController
    end

    %% MVC Architecture
    subgraph Controllers["Controllers"]
        MainController[MainController] --> UserController
        MainController --> PostController
        MainController --> FollowerController
        MainController --> CompanyService
    end

    subgraph Models["Models"]
        User[User Model] --> Post[Post Model]
        User --> Follower[Follower Model]
        Post --> Sentiment[Sentiment Enum]
        Company[Company Model]
    end

    subgraph Views["Views"]
        MainWindow[MainWindow] --> SocialMediaView
        SocialMediaView --> UserProfileWidget
        SocialMediaView --> FeedWidget
        SocialMediaView --> FollowerListWidget
        SocialMediaView --> NewsWidget
        FeedWidget --> PostWidget
        FeedWidget --> CreatePostWidget
        SocialMediaView --> ThemeSwitcherWidget
    end

    %% Services
    subgraph Services["Services"]
        SentimentService[Sentiment Service] --> GoogleGeminiAPI[Google Gemini API]
        LoggerService[Logger Service]
        CompanyService[Company Service]
    end

    %% Design Patterns
    subgraph DesignPatterns["Design Patterns"]
        %% Factory Pattern
        Factory[Factory Pattern] --> PostBuilderFactory
        PostBuilderFactory --> TextPostBuilder
        PostBuilderFactory --> ImagePostBuilder
        
        %% Builder Pattern
        Builder[Builder Pattern] --> BasePostBuilder
        BasePostBuilder --> TextPostBuilder
        BasePostBuilder --> ImagePostBuilder
        
        %% Command Pattern
        Command[Command Pattern] --> LikeCommand
        Command --> CommentCommand
        Command --> ShareCommand
        Command --> CommandHistory
        
        %% Decorator Pattern
        Decorator[Decorator Pattern] --> BaseUser
        BaseUser --> VerifiedUser
        BaseUser --> SponsoredUser
        
        %% Interceptor Pattern
        Interceptor[Interceptor Pattern] --> Dispatcher
        Dispatcher --> PostCreationInterceptor
        Dispatcher --> SpamFilter
        Dispatcher --> InappropriateContentFilter
    end

    %% Connections between components
    MainController ==> MainWindow
    
    UserController ==> User
    UserController ==> Dispatcher
    UserController ==> PostBuilderFactory
    
    PostController ==> Post
    PostController ==> SentimentService
    PostController ==> PostBuilderFactory
    
    FollowerController ==> Follower
    FollowerController ==> LikeCommand
    FollowerController ==> CommentCommand
    FollowerController ==> ShareCommand
    
    CompanyService ==> Company
    CompanyService ==> SponsoredUser
    CompanyService ==> VerifiedUser
    
    CreatePostWidget ==> PostController
    PostWidget ==> PostController
    UserProfileWidget ==> UserController
    FollowerListWidget ==> FollowerController
    NewsWidget ==> CompanyService
    
    %% Data Flow
    User ===> Post
    User ===> Follower
    User ===> Company
    Post ===> SentimentService
    Post ===> Dispatcher
    Post ===> PostBuilderFactory
    
    %% Styling
    classDef controller fill:#e6f7ff,stroke:#0066cc,stroke-width:2px,color:#003366,font-weight:bold
    classDef model fill:#f0fff0,stroke:#006600,stroke-width:2px,color:#003300,font-weight:bold
    classDef view fill:#fff0f5,stroke:#cc0066,stroke-width:2px,color:#660033,font-weight:bold
    classDef service fill:#fffaf0,stroke:#cc6600,stroke-width:2px,color:#663300,font-weight:bold
    classDef pattern fill:#f5f0ff,stroke:#6600cc,stroke-width:2px,color:#330066,font-weight:bold
    classDef edge stroke:#000000,stroke-width:3px
    
    class MainController,UserController,PostController,FollowerController controller
    class User,Post,Follower,Sentiment,Company model
    class MainWindow,SocialMediaView,UserProfileWidget,FeedWidget,FollowerListWidget,NewsWidget,PostWidget,CreatePostWidget,ThemeSwitcherWidget view
    class SentimentService,LoggerService,CompanyService service
    class Factory,Builder,Command,Decorator,Interceptor,PostBuilderFactory,BasePostBuilder,TextPostBuilder,ImagePostBuilder,LikeCommand,CommentCommand,ShareCommand,CommandHistory,BaseUser,VerifiedUser,SponsoredUser,Dispatcher,PostCreationInterceptor,SpamFilter,InappropriateContentFilter pattern
```

## Entity Relationship Diagram

The following diagram illustrates the data model relationships in the Social Media Influencer Simulator:

```mermaid
%%{init: {
  'theme': 'base', 
  'themeVariables': { 
    'primaryColor': '#f0f8ff', 
    'primaryTextColor': '#000000', 
    'primaryBorderColor': '#7C0200', 
    'lineColor': '#000000', 
    'secondaryColor': '#f5f5f5', 
    'tertiaryColor': '#fff0f0',
    'background': '#e6f2ff'
  }
}}%%
erDiagram
    USER {
        string handle PK
        string bio
        int followers_count
        int posts_count
        bool is_verified
        bool is_sponsored
    }
    
    POST {
        string id PK
        string content
        string image_path
        datetime created_at
        int likes
        int shares
        string author_handle FK
    }
    
    COMMENT {
        string id PK
        string content
        string author
        datetime created_at
        string post_id FK
    }
    
    FOLLOWER {
        string id PK
        string handle
        int political_leaning
        datetime followed_at
        string user_handle FK
    }
    
    COMPANY {
        string name PK
        string description
        enum political_leaning
    }
    
    SENTIMENT {
        enum value "LEFT|RIGHT|NEUTRAL"
    }
    
    USER ||--o{ POST : "creates"
    USER ||--o{ FOLLOWER : "has"
    USER }o--|| COMPANY : "sponsored by"
    POST ||--o{ COMMENT : "has"
    POST }o--|| SENTIMENT : "has"
    COMPANY }o--|| SENTIMENT : "has"
```

## Design Patterns Implemented

This project demonstrates several key software design patterns:

1. **Model-View-Controller (MVC)**: Separates the application into three interconnected components
2. **Factory Pattern**: Creates different types of post builders
3. **Builder Pattern**: Constructs complex post objects step by step
4. **Command Pattern**: Encapsulates post interactions as objects
5. **Decorator Pattern**: Adds features to users dynamically (verification, sponsorships)
6. **Interceptor Pattern**: Processes posts before they're created
7. **Singleton Pattern**: Ensures only one instance of certain services

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

## Project Structure

### Models (`src/models/`)
- `user.py`: User model with profile information
- `post.py`: Post model with content and interactions
- `follower.py`: Follower model with political alignment
- `sentiment.py`: Enum for political sentiment (LEFT, RIGHT, NEUTRAL)
- `company.py`: Company model for sponsorships

### Views (`src/views/`)
- `main_window.py`: Main application window
- `social_media_view.py`: Main view container
- `user_profile_widget.py`: Profile editing interface
- `create_post_widget.py`: Post creation interface
- `feed_widget.py`: Post feed display
- `post_widget.py`: Individual post display
- `follower_list_widget.py`: Follower management
- `news_widget.py`: News and company sponsorship interface
- `theme_switcher_widget.py`: Theme toggle control
- `style_manager.py`: UI styling management

### Controllers (`src/controllers/`)
- `main_controller.py`: Main application controller
- `user_controller.py`: User operations controller
- `post_controller.py`: Post operations controller
- `follower_controller.py`: Follower operations controller

### Services (`src/services/`)
- `sentiment_service.py`: Google Gemini AI integration
- `logger_service.py`: Application logging service
- `logger.py`: Logger implementation
- `company_service.py`: Company management service

### Design Patterns (`src/patterns/`)
- `command/`: Command pattern implementation
  - `post_commands.py`: Like, comment, share commands
  - `command_history.py`: Command history for undo
- `factory/`: Factory pattern implementation
  - `post_builder_factory.py`: Creates post builders
- `builders/`: Builder pattern implementation
  - `base_post_builder.py`: Abstract post builder
  - `text_post_builder.py`: Text post builder
  - `image_post_builder.py`: Image post builder
- `decorator/`: Decorator pattern implementation
  - `base_user.py`: Base user interface
  - `verified_user.py`: Verified user decorator
  - `sponsered_user.py`: Sponsored user decorator
- `interceptors/`: Interceptor pattern implementation
  - `dispatcher.py`: Interceptor dispatcher
  - `post_creation_interceptor.py`: Post validation
  - `spam_filter.py`: Spam content detection
  - `inappropriate_content_filter.py`: Content moderation

## Usage

The application has four main tabs:

1. **Profile**: View and edit your user profile
2. **Feed**: Create new posts and view your existing posts
3. **Followers**: View your followers and their political alignment
4. **News**: View trending content and apply for company sponsorships

### Company Sponsorships

In the News tab, you can:
- View available companies with different political alignments
- Apply for sponsorships from companies that match your content's political leaning
- Receive the [Sponsored] tag on your profile when sponsored
- Terminate sponsorships if you no longer want to be associated with a company

When creating a post, you can specify:
- Post content
- Sentiment (LEFT, RIGHT, or NEUTRAL)
- Optional image path

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT 