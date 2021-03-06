from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
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
    template_name = 'blog/all_posts.html'  # override default post_list.html template

    def get_queryset(self):
        # SELECT * FROM Post WHERE date_publish <= now
        return Post.objects.filter(date_publish__lte=timezone.now()) \
            .order_by('-date_publish')  # newest to oldest


class PostContentView(DetailView):
    model = Post
    template_name = 'blog/post_content.html'  # override default post_detail.html template


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
    template_name = 'blog/drafts.html'

    def get_queryset(self):  # filter records
        return Post.objects.filter(date_publish__isnull=True).order_by('date_create')


# @login_required
def add_comment_to_post(request, pk):  # pk from request call/link
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_content', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_content', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_content', pk=post_pk)


@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.set_publish_date()
    return redirect('post_content', pk=pk)
