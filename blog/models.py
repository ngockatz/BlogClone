from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # superuser
    title = models.CharField(max_length=160)
    text = models.TextField()
    date_create = models.DateTimeField(default=timezone.now)
    date_publish = models.DateTimeField(blank=True, null=True)

    def set_publish_date(self):
        self.date_publish = timezone.now()
        self.save()

    def show_approved_comments(self):
        # list of approved comments
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_content', kwargs={'pk': self.pk})  # redirect

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')  # associated with a post
    author = models.CharField(max_length=100)
    text = models.TextField()
    date_create = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('all_posts')

    def __str__(self):
        return self.text
