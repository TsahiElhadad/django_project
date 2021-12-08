from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # when user deleted, the post delete also
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # for display the post by his title
    def __str__(self):
        return self.title

    # tell django the direction of post model that been created
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})