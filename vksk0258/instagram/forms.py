from django import forms
from .models import Post


class PostForm(forms.ModelsForm):
    class Meta:
        model = Post
        fields = '__all__'