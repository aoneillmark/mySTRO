# MySTRO - My Sound Track Recommendations, Organised

A Flask-based web application that recommends classical music based on weather conditions and provides a comprehensive music library management system.

## Features

- **Weather-Based Music Suggestions**: Uses AI to recommend classical pieces based on current weather conditions
- **Composer Search**: Browse and search through a comprehensive database of classical composers
- **Genre Filtering**: Filter music pieces by different genres (Keyboard, Orchestral, Chamber, etc.)
- **Library Management**: Organise and maintain your personal classical music collection
- **OpenOpus API Integration**: Access a vast database of classical music works and composers

## Components

### Core Application
- `app.py`: Main application file
- `cli.py`: Command-line interface utilities
- `Blueprint/library.py`: Library blueprint for music management
- `models/musicpiece.py`: Music piece data model

### Database
- `database/__init__.py`: Database initialization
- `instance/mystro.db`: SQLite database file

### Testing
- `api_test.py`: API testing suite
- `database_test.py`: Database testing suite
- `test_youtube.py`: YouTube integration tests

### Configuration
- `.github/workflows/build.yml`: CI/CD pipeline configuration
- `tailwind.config.js`: Tailwind CSS configuration
- `pyproject.toml`: Python project configuration
- `Procfile`: Process file for deployment
- `requirements.txt`: Python dependencies

## Prerequisites

- Python 3.12
- Node.js (for Tailwind CSS)
- Flask
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
- Code formatting checks (flake8)
- Automated testing
- Database migration
- Deployment to ImPaaS

## API Integration
MySTRO integrates with:
- OpenOpus API for classical music data
- Weather API for current weather conditions
- Google Gemini AI for music recommendations