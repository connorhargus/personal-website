from django.contrib import admin
from .models import Post

# Allows us to view Posts on the admin page
admin.site.register(Post)
