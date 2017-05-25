from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.http import urlquote
from django.utils.encoding import iri_to_uri,uri_to_iri
from django.conf import settings
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time


def upload_location(instance, filename):
    filedase, extension = filename.split('.')
    return "%s/%s.%s"%(instance.slug, instance.slug, extension)


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title = models.CharField(verbose_name='Заголовок',max_length=120)
    slug = models.SlugField(unique=True, allow_unicode=True)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field",
        default='default.jpg'
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField(verbose_name='Контент',max_length=3000)
    # myfield = MarkdownxField(max_length=3000)
    draft = models.BooleanField(verbose_name='Чорновик', default=False)      #чорновик
    publish = models.DateField(verbose_name='Дата публікації', auto_now=False, auto_now_add=False)
    read_time = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    rating = models.IntegerField(default=0, verbose_name=u'Рейтинг')

    #Category
    ART = models.BooleanField(verbose_name='МИСТЕЦТВО', default=False)
    MUSIC = models.BooleanField(verbose_name='МУЗИКА', default=False)
    CINEMA = models.BooleanField(verbose_name='КІНО', default=False)
    THEATER = models.BooleanField(verbose_name='ТЕАТР', default=False)
    LITERATURE = models.BooleanField(verbose_name='ЛІТЕРАТУРА', default=False)
    SPORT = models.BooleanField(verbose_name='СПОРТ', default=False)
    NIGHTLIFE = models.BooleanField(verbose_name='НІЧНЕ ЖИТТЯ', default=False)
    FESTIVALS = models.BooleanField(verbose_name='ФЕСТИВАЛІ', default=False)
    TEACHING = models.BooleanField(verbose_name='НАВЧАННЯ', default=False)
    BUSINESS = models.BooleanField(verbose_name='БІЗНЕС', default=False)
    EXCURSIONS = models.BooleanField(verbose_name='ЕКСКУРСІЇ', default=False)
    OTHER = models.BooleanField(verbose_name='ІНШЕ', default=False)

    objects = PostManager()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def get_markdown_safe(self):
        return mark_safe(markdown(self.content))

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance=instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    class Meta:
        ordering = ['-timestamp','-updated']


def create_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title,allow_unicode=True)
    qs = Post.objects.filter(slug=slug).order_by("-pk")
    exists =qs.exists()
    if exists:
        new_slug = "%s-%s"%(slug, qs.first().pk)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if instance.content:
        html_string = instance.get_markdown_safe()
        read_time = get_read_time(html_string)
        instance.read_time = read_time


pre_save.connect(pre_save_post_receiver, sender=Post)