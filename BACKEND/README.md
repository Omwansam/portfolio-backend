# Portfolio Backend API

A comprehensive Flask-based REST API for managing a personal portfolio website. This backend provides endpoints for managing projects, skills, experience, education, blog posts, and contact forms.

## Features

- **User Authentication**: JWT-based authentication system with user management
- **Project Management**: CRUD operations for portfolio projects
- **Skills Management**: Categorize and manage technical skills
- **Experience & Education**: Track work experience and educational background
- **Blog System**: Full-featured blog with publishing workflow
- **Contact Management**: Handle contact form submissions
- **Portfolio Analytics**: Statistics and overview endpoints
- **RESTful API**: Clean, consistent API design
- **Database Migrations**: Alembic-based database schema management
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error handling and validation

## Tech Stack

- **Framework**: Flask 2.3.3
- **Database**: SQLAlchemy with PostgreSQL support
- **Authentication**: JWT (JSON Web Tokens)
- **Migrations**: Alembic
- **CORS**: Flask-CORS
- **Environment**: Python 3.8+

## Project Structure

```
BACKEND/
├── server/
│   ├── app.py                 # Main application file
│   ├── config.py              # Configuration settings
│   ├── extensions.py          # Flask extensions
│   ├── models.py              # Database models
│   ├── routes/                # API route blueprints
│   │   ├── users_route.py     # User authentication routes
│   │   ├── projects_route.py  # Project management routes
│   │   ├── skills_route.py    # Skills management routes
│   │   ├── experience_route.py # Experience management routes
│   │   ├── education_route.py # Education management routes
│   │   ├── contact_route.py   # Contact form routes
│   │   ├── blog_route.py      # Blog management routes
│   │   └── portfolio_route.py # Portfolio overview routes
│   ├── utils/                  # Utility functions
│   └── migrations/            # Database migrations
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BACKEND
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `server/` directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://username:password@localhost:5432/portfolio_db
   JWT_SECRET_KEY=your-jwt-secret-key-here
   ```

5. **Initialize the database**
   ```bash
   cd server
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token
- `GET /api/auth/protected` - Protected route example
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `PUT /api/auth/change-password` - Change password

### Projects (`/api/projects`)
- `GET /api/projects` - List all projects
- `GET /api/projects/<id>` - Get specific project
- `POST /api/projects` - Create new project (admin)
- `PUT /api/projects/<id>` - Update project (admin)
- `DELETE /api/projects/<id>` - Delete project (admin)

### Skills (`/api/skills`)
- `GET /api/skills` - List all skills
- `GET /api/skills/<id>` - Get specific skill
- `POST /api/skills` - Create new skill (admin)
- `PUT /api/skills/<id>` - Update skill (admin)
- `DELETE /api/skills/<id>` - Delete skill (admin)
- `GET /api/skills/categories` - Get skill categories

### Experience (`/api/experience`)
- `GET /api/experience` - List all experience entries
- `GET /api/experience/<id>` - Get specific experience
- `POST /api/experience` - Create new experience (admin)
- `PUT /api/experience/<id>` - Update experience (admin)
- `DELETE /api/experience/<id>` - Delete experience (admin)

### Education (`/api/education`)
- `GET /api/education` - List all education entries
- `GET /api/education/<id>` - Get specific education
- `POST /api/education` - Create new education (admin)
- `PUT /api/education/<id>` - Update education (admin)
- `DELETE /api/education/<id>` - Delete education (admin)

### Contact (`/api/contact`)
- `POST /api/contact` - Submit contact form
- `GET /api/contact` - List all contacts (admin)
- `GET /api/contact/<id>` - Get specific contact (admin)
- `PUT /api/contact/<id>/read` - Mark as read (admin)
- `DELETE /api/contact/<id>` - Delete contact (admin)
- `GET /api/contact/stats` - Contact statistics (admin)

### Blog (`/api/blog`)
- `GET /api/blog` - List all blogs
- `GET /api/blog/<slug>` - Get blog by slug
- `POST /api/blog` - Create new blog (admin)
- `PUT /api/blog/<id>` - Update blog (admin)
- `DELETE /api/blog/<id>` - Delete blog (admin)
- `GET /api/blog/tags` - Get all blog tags
- `GET /api/blog/search` - Search blogs

### Portfolio (`/api/portfolio`)
- `GET /api/portfolio/overview` - Portfolio overview
- `GET /api/portfolio/stats` - Detailed statistics
- `GET /api/portfolio/sitemap` - Sitemap data

## Database Models

### User
- Basic user information (username, email, password)
- Profile details (bio, social links, avatar)
- Admin privileges

### Project
- Project details (title, description, images)
- Status tracking (completed, in-progress, planned)
- Technology stack and links

### Skill
- Skill name and proficiency level
- Category classification (language, framework, tool, design)
- Icon support

### Experience
- Work experience details
- Company information and dates
- Current position tracking

### Education
- Educational background
- Institution and degree information
- GPA and location

### Blog
- Blog post content and metadata
- Publishing workflow
- Tag system and view tracking

### Contact
- Contact form submissions
- Read/unread status tracking
- Message management

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login**: POST `/api/auth/login` with email/password
2. **Receive**: Access token and refresh token
3. **Use**: Include `Authorization: Bearer <token>` in headers
4. **Refresh**: Use refresh token to get new access token

## Error Handling

The API provides consistent error responses:

```json
{
  "error": "Error message",
  "details": "Additional error details (if available)"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Development

### Running in Development Mode
```bash
python app.py
```

### Database Migrations
```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

### Testing
```bash
# Run tests (if implemented)
python -m pytest

# Run with coverage
python -m pytest --cov=.
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables for Production
```env
FLASK_ENV=production
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=strong-secret-key
JWT_SECRET_KEY=strong-jwt-secret
```

## Security Considerations

- Passwords are hashed using Werkzeug's security functions
- JWT tokens have expiration times
- Admin-only routes are protected
- Input validation on all endpoints
- CORS is configured for security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue in the repository or contact the development team.
