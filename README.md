# 🎓 Django Course Enrollment API

A REST API built with **Django** and **Django REST Framework** for managing student profiles, courses, and priority-based course enrollments.

## ✨ Key Features

- **Database-Level Duplicate Prevention:** Uses `UniqueConstraint` on `(student, course)` in the `Enrollment` model to prevent duplicate enrollments across both the REST API and Django Admin.
- **Separated Read/Write Serializers:**
  - `POST / PUT / PATCH` endpoints accept flat IDs (`student`, `course`, `priority`) for clean data submission.
  - `GET` endpoints return nested student details (`first_name`, `last_name`) and course titles.
- **Query Optimization:** Eliminates the `N+1` query problem on list and detail endpoints using `select_related('student__user', 'course')`.
- **Interactive API Documentation:** Auto-generated OpenAPI 3.0 schema and interactive **Swagger UI** powered by `drf-spectacular`.

## 🛠 Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **API Documentation:** drf-spectacular (OpenAPI 3.0 / Swagger UI)
- **Database:** SQLite

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com
cd django-course-enrollment-api
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Apply migrations and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run the development server
```bash
python manage.py runserver
```

## 🔗 Main Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/admin/` | `GET` | Django Admin interface |
| `/api/students/` | `GET, POST` | Manage student profiles |
| `/api/courses/` | `GET, POST` | Manage available courses |
| `/api/enrollments/` | `GET, POST` | Manage course enrollments with priority levels |
| `/api/docs/` | `GET` | Interactive **Swagger UI** documentation |
| `/api/schema/` | `GET` | Raw OpenAPI 3.0 YAML/JSON schema |

## 📝 API Usage Examples

**Create an enrollment (`POST /api/enrollments/`):**
```json
{
  "student": 1,
  "course": 2,
  "priority": 1
}
```

**List enrollments (`GET /api/enrollments/`):**
```json
[
  {
    "id": 1,
    "student": {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "age": 16,
      "phone": "+380501234567"
    },
    "course": {
      "id": 2,
      "title": "Python Backend Development"
    },
    "priority": 1
  }
]
```
