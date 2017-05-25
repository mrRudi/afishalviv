from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404, get_list_or_404,redirect, Http404
from .models import Post
from .forms import PostForms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.utils.http import urlquote, urlquote_plus
from django.utils import timezone
from django.db.models import Q
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from pprint import pprint


CATEGORY = {
    "ART": "МИСТЕЦТВО",
    "CINEMA": "КІНО",
    "THEATER": "ТЕАТР",
    "LITERATURE": "ЛІТЕРАТУРА",
    "SPORT": "СПОРТ",
    "NIGHTLIFE": "НІЧНЕ&#160;ЖИТТЯ",
    "FESTIVALS": "ФЕСТИВАЛІ",
    "TEACHING": "НАВЧАННЯ",
    "BUSINESS": "БІЗНЕС",
    "EXCURSIONS": "ЕКСКУРСІЇ",
    "OTHER": "ІНШЕ",
}


def lists(request):

    pprint(request.POST)
    pprint(request.GET)
    pprint(request)

    queryset_list = Post.objects.active()
    query = request.GET.get('q')
    rating = request.GET.get('rating')
    category_active = request.GET.get('category')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
        ).distinct()
    if rating:
        queryset_list = queryset_list.filter(rating__lte=rating).order_by('-rating')
    if category_active:
        if category_active in CATEGORY.keys():
            sql = "SELECT * FROM posts_post WHERE {} = {}".format(category_active,1)
            row = Post.objects.raw(sql)
            queryset_list = queryset_list.filter(id__in=[i.id for i in row])
    paginator = Paginator(queryset_list, 4)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "queryset": queryset,
        "page_request_var":page_request_var,
        "category_active":category_active,
        "category": CATEGORY
    }
    return render(request,'posts/list.html',context)


@login_required
def create(request):

    if not request.user.is_authenticated():
        raise Http404

    if request.method == 'POST':
        form = PostForms(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request,'успішно створено')
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            messages.error(request,'невдалося створити')

    context = {
        'form': PostForms()
    }
    return render(request, 'posts/create.html', context)


def detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        raise Http404
    initial_data = {
        'content_type': instance.get_content_type,
        'object_id': instance.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type= form.cleaned_data['content_type'] # form вертає str
        try:
            content_type = ContentType.objects.get(app_label='comments', model=c_type)
        except ContentType.DoesNotExist:
            content_type = ContentType.objects.get(app_label='posts', model=c_type)
        object_id = form.cleaned_data['object_id']
        content_data = form.cleaned_data['content']
        parent_object = None

        if instance.get_content_type != content_type: # якщо тип не рівний post значить батько - коментар
            parent_object = get_object_or_404(Comment, id=object_id)

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = object_id,
            content = content_data,
            parent = parent_object,
        )
        return HttpResponseRedirect(instance.get_absolute_url())
    comments = instance.comments
    context = {
        'instance': instance,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'posts/detail.html', context)


@login_required
def update(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForms(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'успішно змінено')
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            messages.error(request, 'невдалося змінити')
    context = {
        'form': PostForms(instance=instance)
    }
    return render(request, 'posts/create.html', context)


@login_required
def delete(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'успішно видалено')
    return redirect('posts:list')