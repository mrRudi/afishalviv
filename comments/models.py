from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self)
        return qs

    def filter_by_instance(self,instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=object_id)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  #не може використовувати filter() в запитах API бази даних

    parent = models.ForeignKey('self', null=True, blank=True)   #використовує filter()

    content = models.TextField()
    timespamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['timespamp']

    def __str__(self):
        return self.user.username

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def get_absolute_url(self):
        return reverse('comments:detail', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('comments:delete', kwargs={'id': self.id})

    def delete(self, using=None, keep_parents=False, *args, **kwargs):

        if self.children():
            for child in self.children():
                child.delete()
        super(Comment, self).delete(*args, **kwargs)