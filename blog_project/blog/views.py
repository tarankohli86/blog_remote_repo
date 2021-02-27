from django.shortcuts import render,get_object_or_404
from blog.models import POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from blog.forms import EmailSendForm
from blog.models import Comment
from blog.forms import CommentForm
# Create your views here.


def mail_send_view(request,id):
    post=get_object_or_404(POST,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read post at : \n {}\n\n{}\'s Comments :\n{}'.format(post_url,cd['name'],cd['comments'])
            
            send_mail(subject,message,'pythontesting86@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()
    return render(request,"blog/sharebymail.html",{'form':form,'post':post,'sent':sent})



from taggit.models import Tag
def post_list_view(request,tag_slug=None):
    post_list=POST.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag}) 




def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(POST,slug=post,status='published',
            publish__year=year,
            publish__month=month,
            publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    form=CommentForm()
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
        else:
            form=CommentForm()
    return render(request,"blog/post_detail.html",{'post':post,'comments':comments,'csubmit':csubmit,'form':form})