from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from .models import Prediction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class RejectionReasonListView(LoginRequiredMixin, ListView):
    model = Prediction
    template_name = "rejection_reasons.html"
    context_object_name = "predictions"
    ordering = ["-created_at"]


@login_required
def update_prediction(request, pk):
    if request.method == "POST":
        prediction = get_object_or_404(Prediction, id=pk)
        prediction.reason = request.POST.get("reason", "")
        prediction.confidence = request.POST.get("confidence", "")
        prediction.save()
    return redirect("rejection_reasons")
