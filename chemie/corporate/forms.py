from .models import (
    Interview,
    JobAdvertisement,
    Specialization,
    SurveyQuestion,
    Survey,
    AnswerKeyValuePair,
)
from django import forms


class InterviewForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Aktuelle retninger",
    )

    class Meta:
        model = Interview
        fields = ["title", "text", "picture", "specializations"]


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = JobAdvertisement
        fields = ["title", "description"]


class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = "__all__"


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = "__all__"


class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerKeyValuePair
        fields = "__all__"
