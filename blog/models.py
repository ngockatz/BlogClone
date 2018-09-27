from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User')  # superuser
    title = models.CharField(max_length=160)
    text = models.TextField()
    date_create = models.DateTimeField(default=timezone.now())
    date_publish = models.DateTimeField(blank=True, null=True)

    def set_publish_date(self):
        self.date_publish = timezone.now()
        self.save()

    def approve_comment(self):
        # list of approved comments
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_content', kwargs={'pk': self.pk})  # redirect

    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
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
