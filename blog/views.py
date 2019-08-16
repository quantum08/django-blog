from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

#To display Blog Using Class View
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)




# Create your views here.
'''

# Dummy Data for just check
posts = [
    {
        'author':'vaibhav',
        'title' : 'Blog post 1',
        'content':'just random',
        'date_posted':'August 27 ,2018'
    },
    {
        'author': 'jon',
        'title': 'Blog post 2',
        'content': 'just  second random',
        'date_posted': 'August 28 ,2018'
    }
]
'''
# function View  to display Blog start here
def home(request):

    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html' , context)


def about(request):
    return render(request, 'blog/about.html' , {'title':'About'})

# function View  to display Blog end here


# Class View  to display Blog start here
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
