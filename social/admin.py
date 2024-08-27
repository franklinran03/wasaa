from django.contrib import admin
from .models import Post

# Register your models here.
class postsAdmin(admin.ModelAdmin):
    readonly_fields = ("pub_date",)

admin.site.register(Post, postsAdmin)