# MySTRO - My Sound Track Recommendations, Organised

A Flask-based web application that recommends classical music based on weather conditions and provides a comprehensive music library management system.

## Features

- **Composer Search**: Browse and search through a comprehensive database of classical composers using OpenOpus API integration
- **Genre Filtering**: Filter music pieces by different genres (Keyboard, Orchestral, Chamber, etc.)
- **Library Database Management**: Organise and maintain your personal classical music collection, individual to each user
- **AI Powered Weather-Based Music Suggestions**: Uses Gemini AI to recommend classical pieces based on current weather conditions

## Components

- **`app.py`**: The main entry point of the application, handling the core logic and routing.
- **`cli.py`**: Responsible for the population of the database.
- **`Blueprint/`**: Contains the blueprint for organizing the library management functionalities.
  - **`library.py`**: Manages user music pieces and library operations.
- **`database/`**: Handles database initialization and connections.
- **`unit_tests/`**: Contains unit tests for various components of the application.
  - **`api_test.py`**: Tests for API integrations such as Google Gemini, OpenOpus, and Weather APIs.
  - **`database_test.py`**: Tests for database operations including creation, population, and CRUD operations.
  - **`email_test.py`**: Tests for email sharing functionality.
  - **`twitter_test.py`**: Tests for Twitter sharing functionality.
- **`templates/`**: Contains HTML templates for rendering views.
  - **`index.html`**: The main landing page of the application.
  - **`form.html`**: The form page for user input.
  - **`library.html`**: The library page displaying the user's music collection.
  - **`about.html`**: The about page with information about the application.
- **`models/`**: Defines the data models used in the application.
  - **`musicpiece.py`**: Contains the `MusicPiece` model which represents a music piece in the library.
- **`instance/`**: Holds instance-specific database.
- **`static/`**: Contains static image files and CSS styling.
- **`tailwind.config.js`**: Configuration file for Tailwind CSS.
- **`requirements.txt`**: Lists the Python dependencies required for the project.
- **`package.json`**: Lists the Node.js dependencies required for the project.
- **`Procfile`**: Defines the commands to run the application on impaas.

## Prerequisites

- Python 3.12
- Node.js (for Tailwind CSS)
- Google Gemini API key
- Weather API key

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies:
```bash
npm install
```

5. Set up environment variables:
Create a .env file with:
```
WEATHER_API_KEY=your_weather_api_key
GOOGLE_API_KEY=your_google_api_key
```

6. Build Tailwind CSS:
```bash
npm run build:css
```

## Running the Application

1. Initialise the database:
```bash
flask drop_all
flask create_all
flask populate
```

2. Run the application:
```bash
flask run
```

The application will be available at http://localhost:8000

## Testing
Run the test suite using:
```bash
pytest api_test.py
pytest database_test.py
```
## CI/CD
The project uses GitHub Actions for continuous integration and deployment, including:
- Code formatting checks (black)
- Automated testing
- Database migration
- Deployment to ImPaaS

## API Integration
MySTRO integrates with:
- OpenOpus API for classical music data
- Weather API for current weather conditions
- Google Gemini AI for music recommendations