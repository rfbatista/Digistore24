from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Prediction


class ProductPredictions(APIView):
    def post(self, request, format=None):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"detail": "Missing product_id"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product, _ = Product.objects.get_or_create(product_id=product_id)
            for item in request.data.get("rejection_reasons", []):
                reason = item.get("explanation", "")
                confidence = item.get("confidence", "")
                Prediction.objects.create(
                    product=product, reason=reason, confidence=confidence
                )
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
