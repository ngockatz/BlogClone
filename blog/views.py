from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView \
    , CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class AllPostsView(ListView):
    model = Post

    def get_queryset(self):
        # SELECT * FROM Post WHERE date_published <= now
        return Post.objects.filter(date_publish__lte=timezone.now()) \
            .order_by('-date_publish')  # newest to oldest


class PostContentView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):  # required login to create
    login_url = '/login'
    redirect_field_name = 'blog/post_content.html'
    form_class = PostForm  # entry form
    model = Post


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'blog/post_content.html'
    form_class = PostForm
    model = Post


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('all_posts')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'blog/all_posts.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(date_publish__isnull=True).order_by('date_create')
