from django import forms
from django.shortcuts import get_list_or_404
from .models import Topic, ForumThread, Comment
from django.forms import ModelForm


# Creating a ModelForm selecting fields in ForumThread model
class ThreadForm(ModelForm):
    # title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = ForumThread
        fields = ['topic', 'title', 'question']
        # topics = get_list_or_404(Topic)
        widgets = {
            # 'topic': forms.ModelChoiceField(queryset=topics),
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Add css
            'question': forms.Textarea(attrs={'class': 'form-control'})  # Add css
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }