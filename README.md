# Digistore24

## Setup

This guide will help you quickly set up and run the Digistore24 application on your local machine. Follow these steps:

### 1. Install Dependencies

Choose one of the following methods:

- **Using UV (recommended):**  
  ```bash
  uv install
  ```

- **Using Pip:**  
  ```bash
  pip install -r requirements.txt
  ```

### 2. Set Up the Database

Run the migrations to initialize your database schema:

- **Using UV:**  
  ```bash
  uv run python manage.py migrate
  ```

- **Using Pip:**  
  ```bash
  python manage.py migrate
  ```

### 3. Create a Superuser

Generate an administrative user to manage the application and to log in:

- **Using UV:**  
  ```bash
  uv run python manage.py createsuperuser
  ```

- **Using Pip:**  
  ```bash
  python manage.py createsuperuser
  ```

### 4. Seed the Database

Populate the database with initial data:

- **Using UV:**  
  ```bash
  uv run python manage.py seed
  ```

- **Using Pip:**  
  ```bash
  python manage.py seed
  ```

### 5. Start the Application

Launch the development server:

- **Using UV:**  
  ```bash
  uv run python manage.py runserver
  ```

- **Using Pip:**  
  ```bash
  python manage.py runserver
  ```

Open your browser and navigate to: `http://localhost:8000/accounts/login`


## Project Description

Digistore24 is a Django-based web application designed to manage and review product prediction results with an integrated review system. The project implements a comprehensive workflow for handling AI-generated product predictions and enabling human review processes.

### Architecture Overview

The application follows Django's MVT (Model-View-Template) architecture pattern and is structured into three main Django apps:

- **IAM (Identity and Access Management)**: Custom user management system extending Django's AbstractUser
- **Prediction Result**: Core functionality for managing product predictions and rejection reasons
- **Review**: Human review system for validating and correcting AI predictions

### Key Features

#### 1. Product Prediction Management
- RESTful API endpoint (`/api/predictions`) for receiving product predictions
- Automatic product creation and prediction storage
- Support for multiple rejection reasons per product
- Confidence scoring and explanation tracking

#### 2. Review System
- Secure authentication-required review interface
- Automatic assignment of unassigned predictions to reviewers
- Decision tracking (approve/reject) with corrected explanations
- Update capabilities for existing reviews

#### 3. Data Models
- **Product**: Stores product identifiers
- **Prediction**: Manages rejection reasons, confidence scores, and timestamps
- **PredictionReview**: Tracks review decisions, corrections, and reviewer assignments

#### 4. Technical Implementation
- Django 5.2.5 with Python 3.12+
- Django REST Framework for API endpoints
- Custom form handling with validation
- Service layer for business logic (prediction assignment)
- Template-based UI with authentication integration
- SQLite database (configurable for production)

### API Endpoints

- `POST /api/predictions` - Submit product predictions
- `GET /review` - Review interface for predictions
- `GET /review/update/<id>/` - Update existing reviews
- `GET /rejection-reasons/` - View rejection reasons list

### Security Features

- Login-required views for sensitive operations
- CSRF protection enabled
- User authentication and authorization
- Secure form handling with validation

## Data Models

The application uses a well-structured relational database design with three main models that work together to manage the product prediction workflow.

### User Model (`digistore24.iam.models.User`)

```python
class User(AbstractUser):
    pass
```

**Description**: Extends Django's built-in AbstractUser model to provide a foundation for user authentication and authorization.

**Fields Inherited from AbstractUser**:
- `username`: Unique username for login
- `email`: User's email address
- `first_name`, `last_name`: User's full name
- `is_active`, `is_staff`, `is_superuser`: Permission flags
- `date_joined`, `last_login`: Timestamp tracking

**Purpose**: Serves as the authentication backbone for the review system, allowing secure access to prediction review interfaces.

### Product Model (`digistore24.prediction_result.models.Product`)

```python
class Product(models.Model):
    product_id = models.CharField(max_length=255)
```

**Description**: Represents individual products in the system that can have associated predictions.

**Fields**:
- `id`: Primary key (auto-generated)
- `product_id`: Unique identifier for the product (max 255 characters)

**Relationships**:
- **One-to-Many** with `Prediction`: A product can have multiple predictions
- **Cascade Delete**: When a product is deleted, all associated predictions are removed

**Purpose**: Acts as the central entity that groups related predictions together, enabling product-specific analysis and review workflows.

### Prediction Model (`digistore24.prediction_result.models.Prediction`)

```python
class Prediction(models.Model):
    reason = models.CharField(max_length=255)
    confidence = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Description**: Stores AI-generated predictions about product rejection reasons with confidence scores.

**Fields**:
- `id`: Primary key (auto-generated)
- `reason`: The rejection reason explanation (max 255 characters)
- `confidence`: Confidence score for the prediction (max 50 characters)
- `product`: Foreign key to the associated Product
- `created_at`: Timestamp when the prediction was created
- `updated_at`: Timestamp when the prediction was last modified

**Relationships**:
- **Many-to-One** with `Product`: Multiple predictions can belong to one product
- **One-to-One** with `PredictionReview`: Each prediction has one review record

**Methods**:
- `to_dict()`: Serializes the prediction to a dictionary format for API responses

**Purpose**: Captures the core AI prediction data that needs human review and validation.

### PredictionReview Model (`digistore24.review.models.PredictionReview`)

```python
class PredictionReview(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    decision = models.IntegerField(blank=True, null=True)
    corrected_explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Description**: Tracks the human review process for each prediction, including decisions and corrections.

**Fields**:
- `id`: Primary key (auto-generated)
- `prediction`: Foreign key to the Prediction being reviewed
- `user`: Foreign key to the User performing the review
- `reviewed`: Boolean flag indicating if the review is complete
- `decision`: Integer field for review decision (approve/reject)
- `corrected_explanation`: Text field for corrected explanations from reviewers
- `created_at`: Timestamp when the review was created
- `updated_at`: Timestamp when the review was last modified

**Relationships**:
- **Many-to-One** with `Prediction`: Each prediction has one review record
- **Many-to-One** with `User`: Multiple reviews can be assigned to one user

**Purpose**: Enables the human review workflow by tracking review assignments, decisions, and corrections for quality assurance.

### Database Relationships

```
User (1) ←→ (Many) PredictionReview
Product (1) ←→ (Many) Prediction
Prediction (1) ←→ (1) PredictionReview
```

**Key Design Principles**:
1. **Referential Integrity**: Foreign key constraints ensure data consistency
2. **Audit Trail**: Timestamps on all models for tracking changes
3. **Separation of Concerns**: Clear separation between prediction data and review workflow
4. **Scalability**: Efficient querying through proper indexing and relationships

## Thoughts on AI → Human → Automation Transition

The transitions on AI generated to human isn't about choosing between human and artificial intelligence, but about designing systems where they work together synergistically. The goal is to create workflows that leverage the best of both worlds: AI's speed and consistency with human creativity and judgment

## Thoughts on Evaluation and Visualization of Data

Data evaluation and visualization are fundamental to understanding system performance, user behavior, and business outcomes. The goal is to transform raw information into insights that drive better decisions, improve user experiences, and create business value. This requires both technical skills and business acumen, combining analytical rigor with creative presentation.

## Thoughts on integrating Okta SSO

For this proof-of-concept, I used Django’s built-in authentication, but in a real production system we would likely integrate with the company’s identity provider (Okta) to simplify user management and improve security.

There are two realistic approaches:

1. OIDC (OpenID Connect, OAuth2-based)

  - Okta supports OIDC natively, and Django has strong libraries such as django-allauth, mozilla-django-oidc, or python-social-auth.

  - Advantages: easier setup than SAML, well-suited for APIs and modern applications, good support for access/refresh tokens.

  - Recommended if we plan to expose the tool beyond internal use or need tighter integration with other services.

2. SAML 2.0

  - Okta also supports SAML, and Django can integrate using libraries like djangosaml2 or python3-saml.

  - This requires more configuration (certificates, metadata exchange) but is often the mandated standard in enterprise environments.

  - Suitable if the organization’s identity governance mandates SAML for all internal tools.

## Limitations and what it takes to got to production

While the current implementation provides a solid foundation for the technical test, several limitations and production considerations need to be addressed before deploying to a live environment. Understanding these constraints helps set realistic expectations and plan for proper production deployment.

### Current System Limitations

#### **1. Authentication and Security**
- **Basic Authentication**: Django's built-in auth lacks enterprise features like MFA, SSO, and advanced password policies
- **Session Management**: No session timeout controls or concurrent session limits
- **User Management**: Manual user creation and management without role-based access control (RBAC)
- **Audit Logging**: Limited tracking of user actions and system access patterns

#### **2. Data Management and Scalability**
- **SQLite Database**: Not suitable for production workloads, concurrent users, or data persistence
- **No Data Backup**: No automated backup strategy or disaster recovery procedures

#### **3. Performance and Monitoring**
- **No Performance Monitoring**: No metrics collection, logging, or alerting systems
- **No Load Balancing**: Single server deployment without horizontal scaling capabilities
- **No CDN**: Static files served directly from Django without content delivery optimization

#### **4. API and Integration**
- **Basic REST API**: Limited API features like rate limiting, versioning, or comprehensive error handling
- **No API Documentation**: Missing OpenAPI/Swagger documentation for API consumers
- **Limited Validation**: Basic input validation without comprehensive data sanitization

## Time spent on the task

### 2h30 
