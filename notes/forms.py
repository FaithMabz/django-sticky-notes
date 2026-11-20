from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """Validate the title and content when creating or editing notes."""
    class Meta:
        """Configure the fields and input widgets for the Note model."""
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter note title'}),
            'content': forms.Textarea(
                attrs={'placeholder': 'Write your note', 'rows': 5}
                ),
        }
