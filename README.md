# E-Library System

A simple library management service using that enables libraries to manage their book inventory efficiently, maintain member records, and process borrowing transactions.

This project is built using FastAPI and adheres to  RESTful API practices.

FEATURES
-------------------
**User Resource Management**
- CREATE, READ, UPDATE, and DELETE operations. 
- State management by Boolean activation flags.
- Response schema validation by Pydantic models.

**Book Resource Administration**
- CREATE, READ, UPDATE, and DELETE operations.
- Query filtering with pagination support.
- Case-insensitive search implementation.

**Borrow processing operations**
- Resource availability check pre-transaction.
- User eligibility validation  pre-transaction.
- Prevention of duplicate transactions.
- Processing returns with date validation.

**Transaction Record Management**
- Detailed borrow history maintenance.
- Ability to filter transactions by user.
- Referential integrity across resources.


API Endpoints
-------------------
### User Endpoints

```plaintext
POST   /v1/users/          Create new user
GET    /v1/users/          Retrieve all users
GET    /v1/users/{id}      Retrieve specific user
PUT    /v1/users/{id}      Update user details
PATCH  /v1/users/{id}      Deactivate user
DELETE /v1/users/{id}      Delete user
```
### Book Endpoints

```plaintext
POST   /v1/books/          Add new book
GET    /v1/books/          List books (with filtering)
GET    /v1/books/{id}      Retrieve specific book
PUT    /v1/books/{id}      Update book details
PATCH  /v1/books/{id}      Mark book unavailable
DELETE /v1/books/{id}      Remove book
```
### Borrowing Endpoints

```plaintext
POST   /v1/borrows/        Record book borrowing
GET    /v1/borrows/        List all borrowing records
GET    /v1/borrows/{id}    Get user's borrowing history
PATCH  /v1/borrows/{id}    Process book return
```


## System Architecture

### Core Components

e-library-system


1. **API Layer** (`routes/`)
   - Implements RESTful endpoints with precise request/response contracts
   - Handles HTTP-specific concerns and parameter validation
   - Routes requests to appropriate CRUD operations
  
2. **CRUD Layer** (`app/crud/`)
   - Defines RESTful endpoint handlers
   - Implements request validation
   - Manages response formatting
   - Handles error scenarios

4. **Service Layer** (`app/services/`)
   - Manages workflows and state transitions
   - Implements validation rules and business constraints

5. **Data Models** (`app/schemas/`)
   - Defines Pydantic model specifications
   - Establishes entity relationships
   - Manages data transformation logic

5. **Tests** (`app/tests/`)
   - Implements comprehensive test cases
   - Defines test fixtures and utilities
   - Manages mock object patterns
   - Validates business rule compliance

6. **Exceptions** (`app/exceptions.py`)
   - Establishes exception hierarchy
   - Defines custom errors

7. **Application Bootstrap** (`app/main.py`)
   - Configures FastAPI application
   - Registers route handlers

 
### System Requirements

1. **Runtime Environment**
   ```bash
   Python >= 3.8
   pip package manager
   Virtual environment management system
   ```

2. **System Dependencies**
   ```bash
   # Core dependencies
   fastapi==0.115.6
   uvicorn==0.34.0
   pydantic==2.10.4
   python-dateutil==2.9.0
   email-validator==2.2.0
   ```

### Application setup

1. **Environment Configuration**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd e-library-system

   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   .\venv\Scripts\activate   # Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Server Initialization**
   ```bash
   # Development server with auto-reload
   uvicorn main:app --reload --port 8000

   # Production server
   uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
   ```



## Test Architecture

The system uses pytest to manage fixtures and mock patterns.

## Test Execution 
1. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   .\venv\Scripts\activate   # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov pytest-asyncio httpx
   ```

### Test Execution 

1. **Full Test Suite**
   ```bash
   # Execute all tests with verbose output
   pytest -v
   ```

2. **Targeted Testing**
   ```bash
   # Run selective test modules
   pytest tests/test_books.py



### Interactive API Documentation

1. **Swagger UI Access**
   ```plaintext
   http://localhost:8000/docs
   ```
   - Interactive endpoint documentation
   -Schema of request and response
   - API testing interface

2. **ReDoc Documentation**
   ```plaintext
   http://localhost:8000/redoc
   ```
   - Alternative API documentation
   - Full schema references
   - Endpoint relationship visualization



