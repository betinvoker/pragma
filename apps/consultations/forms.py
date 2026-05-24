from django import forms
from .models import Consultation


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Задайте вопрос AI...'}),
        }
        labels = {
            'question': 'Ваш вопрос',
        }