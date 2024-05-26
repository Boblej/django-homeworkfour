import re
from django import forms
from .models import Post
from django.utils import timezone

class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])

    class Meta:
        model = Post
        fields = ['title', 'content', 'pub_date']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title cannot be empty.')
        if len(title) > 200:
            raise forms.ValidationError('Title cannot exceed 200 characters.')
        if re.search(r'[<>]', title):
            raise forms.ValidationError('Title should not contain special characters or HTML tags.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Content cannot be empty.')
        if len(content) > 5000:
            raise forms.ValidationError('Content cannot exceed 5000 characters.')
        if re.search(r'[<>]', content):
            raise forms.ValidationError('Content should not contain special characters or HTML tags.')
        return content

    def clean_pub_date(self):
        pub_date = self.cleaned_data.get('pub_date')
        if pub_date > timezone.now():
            raise forms.ValidationError('Publication date cannot be in the future.')
        return pub_date
