# McKinsey PPT Generator System

AI-powered professional presentation generation system with FastAPI and Docker.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for local development)

### Installation

1. Clone the repository:
```bash
cd mckinsey-ppt-generator
```

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

### Verification

After starting the containers, verify the system:

1. **Health Check**:
```bash
curl http://localhost:8000/health
```

2. **API Documentation**: Visit http://localhost:8000/docs

3. **Root Endpoint**:
```bash
curl http://localhost:8000
```

## 📁 Project Structure

```
mckinsey-ppt-generator/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       └── __init__.py
│   ├── agents/                 # AI agents module
│   │   └── __init__.py
│   ├── core/                   # Core configuration and utilities
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/                 # Pydantic models
│   │   └── __init__.py
│   ├── services/               # Business logic
│   │   └── __init__.py
│   ├── templates/              # PPT templates
│   │   └── __init__.py
│   └── utils/                  # Utility functions
│       └── __init__.py
├── tests/                      # Test suite
│   └── __init__.py
├── docker/                     # Docker-related files
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

## 🛠️ Development

### Local Development (without Docker)

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
cd app
python main.py
```

### Docker Development

The Docker Compose setup includes:
- **app**: FastAPI application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)

Hot reload is enabled for development through volume mounting.

## 📊 API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## 🔧 Configuration

Environment variables can be set in `.env` file:

```env
APP_ENV=development
APP_NAME="McKinsey PPT Generator"
LOG_LEVEL=INFO
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ppt_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key_here
```

## 📝 Next Steps

- Day 2: Database connection setup
- Day 2: Logging system implementation
- Day 3: Authentication and authorization
- Day 4: PPT generation engine
- Day 5: AI agent integration

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

Private project - All rights reserved