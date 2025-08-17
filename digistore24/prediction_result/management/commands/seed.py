from django.core.management.base import BaseCommand
from digistore24.prediction_result.models import Product, Prediction


class Command(BaseCommand):
    help = "Seed the database with initial Product and Prediction data"

    def handle(self, *args, **kwargs):
        # Create or get product
        product, created = Product.objects.get_or_create(product_id="123456")
        if created:
            self.stdout.write(
                self.style.SUCCESS("Created Product with product_id 123456")
            )
        else:
            self.stdout.write("Product with product_id 123456 already exists")

        # Seed predictions
        predictions_data = [
            {
                "reason": "The sales page uses the term 'lifetime access', which is not permitted.",
                "confidence": "High",
            },
            {
                "reason": "The product may require ZFU registration due to its structure as a distance learning program.",
                "confidence": "Medium",
            },
        ]
        for data in predictions_data:
            prediction, p_created = Prediction.objects.get_or_create(
                product=product, reason=data["reason"], confidence=data["confidence"]
            )
            if p_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created Prediction: {data['reason']}")
                )
            else:
                self.stdout.write(f"Prediction already exists: {data['reason']}")

        self.stdout.write(self.style.SUCCESS("Database seeding complete."))
