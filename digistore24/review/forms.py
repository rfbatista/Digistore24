from django import forms


class PredictionReviewForm(forms.Form):
    REVIEW_CHOICES = [
        (1, "Confirm ✅"),
        (2, "Override ❌"),
    ]
    pk = forms.IntegerField(widget=forms.HiddenInput())
    review_decision = forms.TypedChoiceField(
        choices=REVIEW_CHOICES, coerce=int, widget=forms.RadioSelect, initial=1
    )
    corrected_explanation = forms.CharField(
        widget=forms.Textarea(attrs={"class": "w-full p-2 border rounded"}),
        required=False,
        label="Corrected Explanation (optional)",
    )
