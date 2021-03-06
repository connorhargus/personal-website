from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

# This is no longer used, since adding class-based version below
# def home(request):
#     context = {
#         'posts': Post.objects.all(),
#     }
#     return render(request, 'blog/home.html', context)


# Class based views below use defaults for views, saving lines of code if naming conventions followed.
class PostListView(ListView):
    model = Post  # Only line you really need if you follow naming conventions below
    template_name = 'blog/home.html'  # Default location of template for this view <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # Default name is different
    ordering = ['-date_posted']
    paginate_by = 5
    extra_context = {'title': 'blog'}


class UserPostListView(ListView):
    model = Post  # Only line you really need if you follow naming conventions below
    template_name = 'blog/user_posts.html'  # Default location of template for this view <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # Default name is different
    paginate_by = 5
    extra_context = {'title': 'user posts'}

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


# Inheriting from LoginRequiredMixin is similar to decorator @login_required but for class-based views.
class PostCreateView(PermissionRequiredMixin, CreateView):

    # Restrict access for creating posts to staff
    permission_required = 'is_staff'

    model = Post
    fields = ['title', 'content']

    # Override form_valid in order to give author_id for new post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Inheriting from UserPassesTestMixin allows for test_func, checking user updating post is author.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # Override form_valid in order to give author_id for new post
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

    # URL to redirect to after successful deletion
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def teaching(request):
    context = {'title': 'teaching',
               'calculus': [('Syllabus', 'Syllabus'),
                            ('Exam 1', 'Exam_1'),
                            ('Exam 2', 'Exam_2'),
                            ('Exam 3', 'Exam_3'),
                            ('Quiz 1', 'Quiz_1'),
                            ('Quiz 2', 'Quiz_2'),
                            ('Quiz 3', 'Quiz_3'),
                            ('Quiz 4', 'Quiz_4'),
                            ('Quiz 5', 'Quiz_5')],
               'precalculus': [('Syllabus', 'Syllabus'),
                            ('Exam 1', 'Exam_1'),
                            ('Exam 2', 'Exam_2'),
                            ('Exam 3', 'Exam_3'),
                            ('Quiz 1', 'Quiz_1'),
                            ('Quiz 2', 'Quiz_2'),
                            ('Quiz 3', 'Quiz_3'),
                            ('Quiz 4', 'Quiz_4'),
                            ('Quiz 5', 'Quiz_5'),
                            ('Quiz 6', 'Quiz_6'),
                            ('Quiz 7', 'Quiz_7')]}

    return render(request, 'blog/teaching.html', context)

