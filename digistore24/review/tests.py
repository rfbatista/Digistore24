from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from digistore24.review.services import assign_oldest_unassigned_prediction_review
from digistore24.prediction_result.models import Prediction, Product
from digistore24.review.models import PredictionReview


# Create your tests here.
class AssignOldestUnassignedPredictionReviewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="password")
        # Create a product and a prediction with a created_at timestamp
        self.product = Product.objects.create(product_id="Test Product")
        self.prediction = Prediction.objects.create(
            created_at=timezone.now(), product=self.product
        )

    def test_assign_review(self):
        review = assign_oldest_unassigned_prediction_review(self.user)
        self.assertIsNotNone(review)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.prediction, self.prediction)
        self.assertFalse(review.reviewed)
        self.assertEqual(PredictionReview.objects.count(), 1)
