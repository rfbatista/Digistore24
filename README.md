# Digistore24

## Setup Instructions

To start the development server, simply run:

~~~bash
python manage.py runserver
~~~

## Dependencies Installation

To install dependencies, you have two options:

0. Using uv:

   ```bash
   uv install
   ```

1. Using pip and the requirements.txt file:

   ```bash
   pip install -r requirements.txt
   ```

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

