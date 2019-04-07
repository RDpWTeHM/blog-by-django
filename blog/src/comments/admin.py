from django.contrib import admin

# Register your models here.
from .models import Comment


# class CommentModelAdmin(admin.ModelAdmin):
#     list_display = ["user", "post", "timestamp", ]
#     # list_display_links = ["updated"]
#     list_filter = ["user", "timestamp"]
#     search_fields = ["user", "post"]

#     class Meta:
#         model = Comment


# admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Comment)
