from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from.models import Post

def home(request):
   context = {
        # Post from the database table.
        'posts': Post.objects.all()
    }
   return render(request, 'blog/home.html', context)

# list view of the posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # change the ordering post from new to old
    paginate_by = 5 # 5 pages in page
    
# detail view of single post
class PostDetailView(DetailView):
    model = Post

# delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # redirect to home page

    # function that check if the author of the post is the person who log in to web 
    def test_func(self):
        # get the post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# create a post
# using 'LoginRequiredMixin' when user that not log in try open that page
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    # for setting the author as the poster
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# update a post
# using 'LoginRequiredMixin' when user that not log in try open that page
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    # for setting the author as the poster
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # function that check if the author of the post is the person who log in to web 
    def test_func(self):
        # get the post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# display user posts
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5 # 5 pages in page

    # overloide function
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def about(request):
    return render(request, 'blog/about.html', {'title':'About'})