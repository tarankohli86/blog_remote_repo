from django.contrib import admin
from blog.models import POST,Comment
# Register your models here.

class POSTAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','created','updated','status']
    prepopulated_fields={'slug':('title',)}
    list_filter=('status','author','created','publish')
    search_fields=('title','body')
    raw_id_fields=('author',)
    date_hierarchy='publish'
    odereding=['status','publish']
admin.site.register(POST,POSTAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','body','created','update','active')
    list_filter=('active','created','update')
    list_search=('name','email','body')

admin.site.register(Comment,CommentAdmin)
