from django.db import models
from django.conf import settings
from digistore24.prediction_result.models import Prediction


class PredictionReview(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    decision = models.IntegerField(blank=True, null=True)
    corrected_explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
