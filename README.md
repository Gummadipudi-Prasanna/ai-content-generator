# AI Content Generator

A full-stack content generation and management application built using **React.js, Django REST Framework, and Contentful CMS**.

The application allows users to generate content based on a selected topic, content type, tone, and length. Users can review, edit, save, update, view, and delete content through an interactive React frontend integrated with Django REST APIs and Contentful CMS.

> **Project Status:** Currently uses mock content generation. Real OpenAI API integration is planned as a future enhancement.

---

## Project Overview

The AI Content Generator aims to simplify content creation and content management.

Users can enter a topic, choose their preferred content type, tone, and length, and generate sample content. Generated content can then be edited and managed using Contentful CMS.

## Features

- Generate content using a mock generation service.
- Select different content types:
  - Blog
  - Product Description
  - Social Media Post
  - SEO Description
- Select content tone:
  - Professional
  - Friendly
  - Creative
- Select content length:
  - Short
  - Medium
  - Long
- Preview generated content.
- Edit generated content before saving.
- Save content to Contentful CMS.
- View saved content.
- Edit and update existing content.
- Delete saved content.
- REST API integration between React and Django.
- Input validation and error handling.

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React.js, JavaScript, HTML5, CSS3 |
| Frontend Tool | Vite |
| Backend | Python, Django |
| API | Django REST Framework |
| CMS | Contentful CMS |
| Database | SQLite |
| API Testing | Postman |
| Version Control | Git, GitHub |

## Project Structure

```text
ai-content-generator/
│
├── config/
├── generator/
│   ├── services.py
│   ├── views.py
│   ├── serializers.py
│   └── contentful_service.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── index.html
│
├── postman/
├── venv/
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
└── README.md
```

## Installation and Setup

### Prerequisites

- Python
- Node.js and npm
- Git
- Contentful account

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-content-generator
```

### 2. Backend Setup

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install django djangorestframework django-cors-headers requests python-dotenv djangorestframework-simplejwt
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=
CONTENTFUL_SPACE_ID=
CONTENTFUL_ENVIRONMENT=master
CONTENTFUL_MANAGEMENT_TOKEN=
```

Add your own credentials locally. Never upload `.env` or API tokens to GitHub.

Run database migrations:

```powershell
python manage.py migrate
```

Start the Django server:

```powershell
python manage.py runserver
```

Backend URL:

`http://127.0.0.1:8000/`

### 3. Frontend Setup

Open a new terminal:

```powershell
cd frontend
```

Install frontend dependencies:

```powershell
npm install
```

Start the React development server:

```powershell
npm run dev
```

Frontend URL:

`http://localhost:5173/`

## API Endpoints

| HTTP Method | Endpoint | Description |
|---|---|---|
| POST | `/api/generate-content/` | Generate content |
| POST | `/api/save-content/` | Save content to Contentful |
| GET | `/api/saved-content/` | Retrieve saved content |
| PUT | `/api/update-content/<entry_id>/` | Update saved content |
| DELETE | `/api/delete-content/<entry_id>/` | Delete saved content |

## Contentful CMS Integration

Contentful CMS is used to store and manage generated content.

The application integrates with the Contentful Content Management API.

Configured content fields:

- `title`
- `topic`
- `contentType`
- `tone`
- `generatedContent`

Supported operations:

- Create content entries.
- Retrieve saved entries.
- Update existing entries.
- Delete content entries.

Configure your Contentful Space ID, Environment, and Management API token in the local `.env` file.

## Testing

The following functionality has been tested during development:

- Content generation API.
- Input validation.
- Save content to Contentful.
- Retrieve saved content.
- Update existing content.
- Delete saved content.
- Frontend production build.

API testing was performed using Postman, and frontend functionality was tested through the React application.

## Future Enhancements

- Integrate the real OpenAI API for AI-powered content generation.
- Improve generated content quality.
- Add user authentication and authorization.
- Support additional content formats and customization options.

## Author

Developed as a full-stack portfolio project using React.js, Django REST Framework, and Contentful CMS.
