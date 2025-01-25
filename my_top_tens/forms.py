from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'description']
        labels = {
            'text': 'Topic', 
            'description': 'Description (Optional)', 
        }
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Enter topic title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional description', 'cols': 80, 'rows': 4}),
        }

class MultiRankForm(forms.Form):
    """Form for submitting/editing ranks 1-10."""
    text = forms.CharField(
        required = False, 
        max_length =150, 
        widget = forms.TextInput(attrs = {'placeholder': 'Enter item name'}),
        label = "Text" 
    )
    description = forms.CharField(
        required = False, 
        widget = forms.Textarea(attrs={'placeholder': 'Optional comments', 'cols': 80, 'rows': 2}),
        label = "Comments"  # Change "Description" to "Comments"
    )