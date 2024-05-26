import re
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_no_special_characters(value):
    if re.search(r'[<>]', value):
        raise ValidationError('Title should not contain special characters or HTML tags.')

class Post(models.Model):
    title = models.CharField(max_length=200, validators=[validate_no_special_characters])
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.pub_date > timezone.now():
            raise ValidationError('Publication date cannot be in the future.')
        if not self.title:
            raise ValidationError('Title cannot be empty.')
        if len(self.content) > 5000:
            raise ValidationError('Content cannot exceed 5000 characters.')
        if re.search(r'[<>]', self.content):
            raise ValidationError('Content should not contain special characters or HTML tags.')
        if not self.content:
            raise ValidationError('Content cannot be empty.')

    def __str__(self):
        return self.title
