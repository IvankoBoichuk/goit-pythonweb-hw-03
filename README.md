# GoIT Python Web Homework 03

A bare-bones Python HTTP server built with only the standard library, demonstrating basic web concepts without frameworks like Flask or Django.

## Features

- **Static File Serving**: Automatically serves CSS, JavaScript, images, and other static assets
- **Form Handling**: POST endpoint for message submissions with data persistence
- **Jinja2 Templates**: Dynamic page rendering for displaying stored messages
- **Docker Support**: Containerized deployment with volume persistence
- **Bootstrap UI**: Responsive frontend with consistent navigation

## Project Structure

```
goit-pythonweb-hw-03/
├── main.py              # HTTP server implementation
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
├── storage/
│   └── data.json       # Form submissions storage
├── templates/
│   └── read.html       # Jinja2 template for messages
├── index.html          # Home page
├── message.html        # Contact form
├── error.html          # 404 error page
├── style.css           # Custom styles
└── logo.png           # Site logo
```

## API Endpoints

### GET Routes
- `GET /` → Home page (`index.html`)
- `GET /message.html` → Contact form
- `GET /read` → All submitted messages (Jinja2 template)
- `GET /style.css` → Custom stylesheet
- `GET /logo.png` → Site logo
- `GET /*` → Static files (auto-detected by extension)

### POST Routes
- `POST /message` → Form submission handler
  - Saves to `storage/data.json` with timestamp
  - Redirects to home page

## Data Storage Format

Messages are stored in `storage/data.json` with ISO timestamps as keys:

```json
{
  "2025-09-20T10:30:45.123456": {
    "username": "john_doe",
    "message": "Hello, this is my message!"
  },
  "2025-09-20T10:35:12.789012": {
    "username": "jane_smith",
    "message": "Thanks for the website!"
  }
}
```

## Development

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run server**:
   ```bash
   python main.py
   ```

3. **Access application**:
   - Home: http://localhost:3000
   - Send Message: http://localhost:3000/message.html
   - Read Messages: http://localhost:3000/read

### Docker Development

1. **Build image**:
   ```bash
   docker build -t python-web-hw03 .
   ```

2. **Run container**:
   ```bash
   docker run -p 3000:3000 python-web-hw03
   ```

3. **Run with data persistence**:
   ```bash
   # Create named volume
   docker volume create hw03-data
   
   # Run with persistent storage
   docker run -p 3000:3000 -v hw03-data:/app/storage python-web-hw03
   ```

4. **Development mode** (live code reload):
   ```bash
   docker run -p 3000:3000 -v "$(pwd):/app" -v hw03-data:/app/storage python-web-hw03
   ```

## Docker Volumes

### Data Persistence
- **Volume Mount**: `/app/storage` → preserves `data.json` across container restarts
- **Named Volume**: `hw03-data` for production deployment
- **Bind Mount**: Local directory mounting for development

### Volume Commands
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect hw03-data

# Remove volume (deletes all data!)
docker volume rm hw03-data
```

## Technical Implementation

### HTTP Server Architecture
- **BaseHTTPRequestHandler**: Core request handling
- **Static File Detection**: Automatic MIME type detection for multiple extensions
- **Template Rendering**: Jinja2 integration for dynamic content
- **Form Processing**: URL-encoded form parsing with timestamp keys

### Supported Static File Types
```python
'.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
'.woff', '.woff2', '.ttf', '.eot', '.pdf', '.txt', '.xml'
```

### Security Considerations
- Basic path traversal protection via `pathlib`
- UTF-8 encoding for international characters
- Error handling for malformed requests

## Dependencies

- **Python 3.10+**: Base runtime
- **Jinja2 3.1.2**: Template engine for dynamic pages
- **Bootstrap 5.2.2**: Frontend framework (CDN)

## Contributing

This is a homework project for GoIT Python Web Development course. The architecture is intentionally simple to demonstrate HTTP fundamentals without web frameworks.

### Key Learning Objectives
1. HTTP request/response cycle
2. Static file serving
3. Form data processing
4. Template rendering
5. Data persistence
6. Docker containerization

## License

Educational project - GoIT Bootcamp 2025