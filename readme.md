# socio-backend

An ongoing backend development project for a social media application built using **FastAPI**.

## Features
This project aims to implement the following features:
- User authentication and authorization
- Post creation and management
- Real-time chat functionality
- Secure data handling

## Directory Structure
```
anuragpandey01-socio-backend/
├── app.py                # Entry point of the application
├── database.py           # Database connection and models
├── devserver.sh          # Script to start the development server
├── requirements.txt      # Python dependencies
├── security.py           # Security-related utilities (e.g., authentication)
├── .deepsource.toml      # Configuration for DeepSource code analysis
├── models/               # ORM models for database entities
│   ├── __init__.py       
│   ├── chat.py           # Chat-related models
│   ├── post.py           # Post-related models
│   └── user.py           # User-related models
├── routers/              # API routers for organizing endpoints
│   ├── __init__.py       
│   ├── post.py           # Endpoints for post management
│   └── user.py           # Endpoints for user management
└── services/             # Business logic and background services
    ├── __init__.py       
    └── connection_manager.py  # Handles WebSocket connections
```

## Requirements
- Python 3.9+
- FastAPI
- Other dependencies listed in `requirements.txt`

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/anuragpandey01/anuragpandey01-socio-backend.git
   cd anuragpandey01-socio-backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server:**
   ```bash
   ./devserver.sh
   ```

   Alternatively, you can start the server manually:
   ```bash
   uvicorn app:app --reload
   ```

## Contribution Guidelines
- Ensure your code follows the PEP 8 style guide.
- Use `black` for code formatting and `isort` for import organization.
- Run static code analysis using [DeepSource](https://deepsource.io/).
- Write unit tests for new features and run them before pushing changes.

## Future Plans
- Implement more endpoints for additional features.
- Integrate a caching mechanism for improved performance.
- Add comprehensive documentation for the API.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

