from django.contrib import admin

# from .models import Profile
from .models import Post, Tag

admin.site.register(Post)
# admin.site.register(Comment)
admin.site.register(Tag)
