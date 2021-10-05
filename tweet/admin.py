from django.contrib import admin
from .models import Client,Post,Like,Comment


admin.site.register(Client)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)