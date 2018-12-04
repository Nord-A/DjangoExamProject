from django import forms
from django.shortcuts import get_list_or_404
from .models import Topic, ForumThread
from django.forms import ModelForm

# class ThreadForm(forms.Form):
#     topics_db = get_list_or_404(Topic)
#     # This is because choices= expects list/tuple of tuples.
#     # Example: [('1', 'Django'), ('2', 'C#'), ('3', 'Angular')]
#     topics = []
#     for i in range(len(topics_db)):
#         topics.append(('i', topics_db[i].name))
#
#     Topic = forms.ChoiceField(
#         required=True,
#         # widget=forms.ModelChoiceField(list(topics)),
#         widget=forms.Select,
#         choices=topics
#     )
#
#     # Question = forms.CharField(widget=forms.Textarea)
#     Question = forms.CharField(widget=forms.Textarea(attrs={'class': 'codetextarea'}))


#Creating a ModelForm selecting fields in ForumThread model
class ThreadForm(ModelForm):
    # title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = ForumThread
        fields = ['topic', 'title', 'question']
        # topics = get_list_or_404(Topic)
        #Try to add css
        widgets = {
            # 'topic': forms.ModelChoiceField(queryset=topics),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'question': forms.Textarea(attrs={'class': 'form-control'})
        }


class CommentForm(forms.Form):
    Comment = forms.Textarea(attrs={'class': 'form-control'}) #add widget?