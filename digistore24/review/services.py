from digistore24.prediction_result.models import Prediction
from .models import PredictionReview


def assign_oldest_unassigned_prediction_review(user):
    """
    Find the oldest Prediction that doesn't have a PredictionReview
    and create a PredictionReview assigned to the given user.
    """
    unassigned_prediction = (
        Prediction.objects.filter(predictionreview__isnull=True)
        .order_by("created_at")
        .first()
    )
    if unassigned_prediction:
        review = PredictionReview.objects.create(
            prediction=unassigned_prediction, user=user, reviewed=False
        )
        return review
    return None
