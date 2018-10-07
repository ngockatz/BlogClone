from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):  # render post_form.html by default
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'inputStyle'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postStyle'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'inputStyle'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
