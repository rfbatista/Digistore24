from django.db import models
from django.conf import settings


class Product(models.Model):
    product_id = models.CharField(max_length=255)


class Prediction(models.Model):
    reason = models.CharField(max_length=255)
    confidence = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "reason_id": self.pk,
            "confidence": self.confidence,
            "explanation": self.reason,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
