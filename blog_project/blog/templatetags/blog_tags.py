from blog.models import POST
from django import template

register=template.Library()


@register.simple_tag
def total_posts():
    return POST.objects.count()

@register.inclusion_tag('blog/latest_posts123.html')
def show_latest_posts(count=4):
    latest_posts=POST.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}



    return POST.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
