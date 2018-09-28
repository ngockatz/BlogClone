from django.urls import path
from blog import views

urlpatterns = [
    path('',views.AllPostsView.as_view(),name='all_posts'),
    path('about',views.AboutView.as_view(),name='about'),
    path('posts/<int:pk>',views.PostContentView.as_view(),name='post_content'),
    path('new_post', views.CreatePostView.as_view(),name='post_new'),
    path('posts/<int:pk>/edit', views.UpdatePostView.as_view(),name='post_edit'),
    path('posts/<int:pk>/delete',views.DeletePostView.as_view(),name='post_delete'),
    path('drafts',views.DraftListView.as_view(),name='drafts')
]