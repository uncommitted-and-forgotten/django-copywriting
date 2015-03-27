# -*- coding: utf-8 -*-
import datetime
import traceback 
import sys

from django.db import models
from django.contrib.sitemaps import ping_google
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from compat import GenericForeignKey
from django.utils.html import strip_tags 
from django.core.urlresolvers import reverse
# from django.contrib.comments.models import Comment

from transmeta import TransMeta
# from tagging.models import Tag

from arimagebucket.models import *
from django.dispatch import receiver
from .signals import ready_to_publish, ready_to_review


from django.utils import timezone
 
class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    """
    """
    __metaclass__ = TransMeta
    
    PUBLISHED = 1 # Compatibility mode
    READY_TO_PUBLISH = 2
    READY_TO_REVIEW = 3
    DRAFT = 0
    
    STATE_OPTIONS = ((DRAFT, _('Draft')),
                     (READY_TO_REVIEW, _('Ready To Review')),
                     (READY_TO_PUBLISH, _('Ready To Publish')),
                     (PUBLISHED, _('Published')),
                    )
                    
    # Overview
    title = models.CharField(verbose_name="Title", max_length=250, help_text="Short title (<250 chars)", default="")
    status = models.IntegerField('Visibility', default=0, choices=STATE_OPTIONS)
    slug = models.SlugField(max_length=80, unique=True, help_text="Eg.: 'swiss-drink-promo' (link to news page whould be '/articles/cool-new-feature/' if fullContent !='')", default="")
    desc = models.CharField('Description', max_length=250, help_text="Short desc (<250 chars)", default="")
    authorProfileModel = models.ForeignKey(ContentType)
    authorProfileId = models.PositiveIntegerField()
    author = GenericForeignKey('authorProfileModel', 'authorProfileId')
    pubDate = models.DateTimeField('Date To publish the Article', default=timezone.now, help_text="specify article date")
    addedDate = models.DateTimeField('Date created', auto_now_add=True)
    updatedDate = models.DateTimeField('Date last Modified', auto_now=True)

    # Content
    title_image = models.ForeignKey(ImageBucketObject, help_text="Image for Facebook & Co.",  null=True, blank=True)
    content = models.TextField(verbose_name="Content", blank=True, null=True, help_text="Content with double rendering.", default="")
    
    # Meta
    seoKeyWords = models.CharField(verbose_name='Keywords for meta tags', max_length=250, help_text="SEO: Keywords, separated with ', '", default="arteria")
    seoDesc = models.CharField(verbose_name='Desc for meta tags', max_length=250, help_text="SEO: Description, leave empty for post's description", default="arteria")
    tags = models.ManyToManyField(Tag, blank=True)
    # tags = TagField(help_text="Tags, getrennt durch 'spaces' (aktuell), siehe auch https://arteria.jira.com/wiki/display/ART/Blog+Tags")

    # Comments
    comments_enabled = models.BooleanField(default=True, help_text="Activate Comments")

    class Meta:
        translate = ('title', 'desc', 'content', 'seoKeyWords', 'seoDesc', )

    # def set_tags(self, tags):
    #     Tag.objects.update_tags(self, tags)

    # def get_tags(self):
    #     return Tag.objects.get_for_object(self)

    
    def number_of_words(self):
        ''' 
        '''
        plain = strip_tags(self.content) 
        return len(plain.split(' '))
        
        
    def __unicode__(self):
        """
        """
        return "%s (%i words)" % (self.slug, self.number_of_words())


    def get_absolute_url(self):
        """
        """
        return reverse('copywriting.views.showArticle', None, [str(self.slug)])


    def save(self, force_insert=False, force_update=False):
        isFirstSave = False
        if self.pk is not None:
            orig = Article.objects.get(pk=self.pk)
            if orig.status != self.status:
                if self.status == self.READY_TO_REVIEW:
                    ready_to_review.send(sender=None, articleID = self.id)
                if self.status == self.READY_TO_PUBLISH:
                    ready_to_publish.send(sender=None, articleID = self.id)
                     
        else:
            isFirstSave = True
                 
        super(Article, self).save(force_insert, force_update)
        if isFirstSave is True:
            if self.status == self.READY_TO_REVIEW:
                ready_to_review.send(sender=None, articleID = self.id)
            if self.status == self.READY_TO_PUBLISH:
                ready_to_publish.send(sender=None, articleID = self.id)  
        try:
            if getattr(settings, 'DEBUG', False) is False:
                ping_google()
        except Exception:
            pass
    

class AuthorProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(help_text="Steckbrief", 
        null=True, 
        blank=True)
    shortBio = models.TextField(help_text="Steckbrief (Teaser)",
        null=True, 
        blank=True)
    twitter = models.CharField(max_length=100, 
        null=True, 
        blank=True,
        help_text="twitter benutzername ohne '@' - z.B. arteria_ch")
    linkedin = models.CharField(max_length=100, null=True, blank=True,
        help_text="link zum linkedin Profil - z.B. http://www.linkedin.com/profile/view?id=209942560")
    facebook = models.CharField(max_length=100,
        null=True,
        blank=True,
        help_text="link zum facebook Profil - z.B. https://www.facebook.com/arteria.ch")
    xing = models.CharField(max_length=100, null=True, blank=True,
        help_text="link zum xing Profil - z.B. https://www.xing.com/profile/Walter_Renner5")
    google_plus = models.CharField(max_length=100, null=True, blank=True,
        help_text="link to googple Plus Profile")
    sex = models.IntegerField('Sex', choices=((0, "neutral"), (1, "weiblich"), (2, "maennlich"), ), default=0)

    def __unicode__(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_google_plus_url(self):
        return self.google_plus


class Comment(models.Model):
    author = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return self.article.title

# class Comment(Comment):
#     article = models.ForeignKey(Article, blank=False, )
#     content = models.CharField(max_length=300)

#     def get_comment_model(self):
#         # Use our custom comment model instead of the built-in one.
#         return Comment

if 'watson' in settings.INSTALLED_APPS:
    import watson
    watson.register(Article)
