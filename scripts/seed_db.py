import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digistore24.settings")
django.setup()

from digistore24.prediction_result.models import Product, Prediction


def seed_db():
    product, created = Product.objects.get_or_create(product_id="123456")
    if created:
        print("Created Product with product_id 123456")
    else:
        print("Product with product_id 123456 already exists")

    predictions_data = [
        {
            "reason": "The sales page uses the term 'lifetime access', which is not permitted.",
            "confidence": "High",
        },
        {
            "reason": "The product may require ZFU registration due to its distance learning structure.",
            "confidence": "Medium",
        },
    ]

    for data in predictions_data:
        prediction, p_created = Prediction.objects.get_or_create(
            product=product,
            reason=data["reason"],
            confidence=data["confidence"],
        )
        if p_created:
            print(f"Created Prediction: {data['reason']}")
        else:
            print(f"Prediction already exists: {data['reason']}")


if __name__ == "__main__":
    seed_db()
    print("Database seeding complete.")
