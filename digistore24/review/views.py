from django.shortcuts import render
from django.shortcuts import redirect, render
from digistore24.review.forms import PredictionReviewForm
from digistore24.review.models import PredictionReview
from digistore24.review.services import assign_oldest_unassigned_prediction_review
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404


@login_required
def review_product(request):
    if request.method == "POST":
        form = PredictionReviewForm(request.POST)
        if form.is_valid():
            review_decision = form.cleaned_data["review_decision"]
            corrected_explanation = form.cleaned_data["corrected_explanation"]
            pk = form.cleaned_data["pk"]
            try:
                prediction_review = PredictionReview.objects.get(pk=pk)
            except PredictionReview.DoesNotExist:
                raise Http404("PredictionReview not found.")
            prediction_review.reviewed = True
            prediction_review.decision = review_decision
            prediction_review.corrected_explanation = corrected_explanation
            prediction_review.save()
            return redirect("review_product")
        else:
            try:
                prediction_review = PredictionReview.objects.get(pk=form.data.get("pk"))
            except PredictionReview.DoesNotExist:
                prediction_review = None
            return render(
                request,
                "review.html",
                {"prediction_review": prediction_review, "form": form},
            )
    else:
        assign_oldest_unassigned_prediction_review(request.user)
        prediction_review = (
            PredictionReview.objects.select_related("prediction")
            .filter(user=request.user, reviewed=False)
            .order_by("created_at")
            .first()
        )
        if prediction_review is None:
            return render(
                request,
                "review.html",
                {"prediction_review": None},
            )
        form = PredictionReviewForm(
            initial={
                "pk": prediction_review.pk if prediction_review else None,
                "review_decision": prediction_review.decision
                if prediction_review
                else 1,
                "corrected_explanation": prediction_review.corrected_explanation
                if prediction_review
                else "",
            }
        )
    return render(
        request, "review.html", {"prediction_review": prediction_review, "form": form}
    )


@login_required
def update_review_product(request, pk):
    prediction_review = get_object_or_404(PredictionReview, id=pk, user=request.user)
    if request.method == "POST":
        form = PredictionReviewForm(request.POST)
        if form.is_valid():
            review_decision = form.cleaned_data["review_decision"]
            corrected_explanation = form.cleaned_data["corrected_explanation"]
            prediction_review.reviewed = True
            prediction_review.decision = review_decision
            prediction_review.corrected_explanation = corrected_explanation
            prediction_review.save()
            return redirect("rejection_reasons")
    else:
        form = PredictionReviewForm(
            initial={
                "review_decision": prediction_review.decision,
                "corrected_explanation": prediction_review.corrected_explanation,
            }
        )
    return render(
        request,
        "update_review.html",
        {"prediction_review": prediction_review, "form": form},
    )
