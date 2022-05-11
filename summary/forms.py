from django.forms import ModelForm
from .models import Prompt,Review, PromptReview

class PromptForm(ModelForm):
    class Meta:
        model = Prompt
        fields = '__all__'

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

class PromptReviewForm(ModelForm):
    class Meta:
        model = PromptReview
        fields = '__all__'
