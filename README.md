# Service Management System for Computer Repair Shops

A Django REST API backend for managing computer repair shop operations, including customer management, repair job tracking, and parts replacement records.

## Description

This project provides a comprehensive backend API for computer repair shops to manage their daily operations. It allows tracking customers, creating and managing repair jobs, assigning engineers, and recording replaced parts with costs.

## Features

- **User Management**: Custom user model with roles for staff and engineers
- **Customer Management**: Store customer details including contact information and address
- **Repair Job Tracking**: Create, update, and track repair jobs with device details, status, and assignments
- **Parts Management**: Record replaced parts with costs for each repair job
- **Status Tracking**: Monitor repair progress (pending, in progress, completed)
- **Image Upload**: Support for device images
- **RESTful API**: Built with Django REST Framework for easy integration

## Tech Stack

- **Backend**: Django 6.0.1
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django's built-in authentication with custom user model

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd DRS_API
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup:**
   - Create a PostgreSQL database named `vedb`
   - Update database credentials in `backend_api/backend_api/settings.py` if needed

5. **Run migrations:**
   ```bash
   cd backend_api
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

## Usage

### Running the Development Server

```bash
cd backend_api
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/` using the superuser credentials.

## API Endpoints

*(Note: API endpoints are planned but not yet implemented. The following are the intended endpoints:)*

- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create a new customer
- `GET /api/repair-jobs/` - List all repair jobs
- `POST /api/repair-jobs/` - Create a new repair job
- `PUT /api/repair-jobs/{id}/` - Update repair job status
- `GET /api/replaced-parts/` - List replaced parts
- `POST /api/replaced-parts/` - Add replaced part to a repair job

## Models

### CustomUser
- username, email, phone
- Extends Django's AbstractUser

### Customer
- customer_name, customer_phone, customer_email, address
- created_at timestamp

### RepairJob
- customer (ForeignKey)
- device details (type, brand, model, serial number)
- device_image
- problem_description
- status (pending, in_progress, completed)
- assigned_engineer (ForeignKey to CustomUser)
- created_by (ForeignKey to CustomUser)
- timestamps

### ReplacedParts
- repair_job (ForeignKey)
- part_name, cost
- replaced_at timestamp

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.