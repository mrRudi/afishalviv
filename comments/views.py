from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, Http404, HttpResponse, redirect
from .models import Comment
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def comment_thread(request, id=None):
    obj = get_object_or_404(Comment, id=id)

    initial_data = {
        'content_type': obj.get_content_type,
        'object_id': obj.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data['content_type']  # form вертає str
        try:
            content_type = ContentType.objects.get(app_label='comments', model=c_type)
        except ContentType.DoesNotExist:
            content_type = ContentType.objects.get(app_label='posts', model=c_type)

        object_id = form.cleaned_data['object_id']
        content_data = form.cleaned_data['content']

        parent_object = get_object_or_404(Comment, id=object_id)

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data,
            parent=parent_object,
        )
        return HttpResponseRedirect(obj.get_absolute_url())

    context = {
        'object': obj,
        'form': form,
    }
    return render(request, 'comments/comment_thread.html', context)

@login_required
def delete(request, id):
    obj = get_object_or_404(Comment, id=id)

    if obj.user != request.user:
        # messages.success(request, 'нема доступу')
        response = HttpResponse('нема доступу')
        response.status_code = 403
        return response

    if request.method == 'POST':
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, 'видалено')
        return  HttpResponseRedirect(parent_obj_url)

    context = {
        'object': obj,
    }
    return render(request, 'comments/confirm_delete.html', context)
