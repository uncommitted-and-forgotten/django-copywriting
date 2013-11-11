# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import *
from transmeta import canonical_fieldname


class ArticleAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        db_fieldname = canonical_fieldname(db_field)
        return field


    fieldsets = [
        # ('Overview', {'fields': ['title', 'slug', 'status', 'desc', 'pubDate']}),
        # ('Author', {'fields': ['authorProfileModel', 'authorProfileId']}),
        # ('Content', {'fields': ['content', 'title_image']}),
        # ('Meta', {'fields': ['seoKeyWords_de', 'seoDesc', 'tags']}),
        # ('Options', {'fields': ['comments_enabled']})
    ]

    date_hierarchy = 'pubDate'
    
    def number_of_words(self, obj):
        return u'%s' %  obj.countWords()
        
    # prepopulated_fields = {'slug':('title',),}

    list_display = ('title', 'number_of_words', 'status', 'pubDate', 'addedDate', 'updatedDate')
    readonly_fields = ('addedDate', 'updatedDate', 'pubDate')

    search_fields = ['title', 'slug', 'desc']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(AuthorProfile)

class ProfileAdmin(admin.ModelAdmin):

    def make_mailing_list(self, request, queryset):
        from emencia.django.newsletter.models import Contact
        from emencia.django.newsletter.models import MailingList

        subscribers = []
        for profile in queryset:
            contact, created = Contact.objects.get_or_create(email=profile.mail,
                                                             defaults={'first_name': profile.first_name,
                                                                       'last_name': profile.last_name,
                                                                       'content_object': profile})
            subscribers.append(contact)
        new_mailing = MailingList(name='New mailing list',
                                  description='New mailing list created from admin/profile')
        new_mailing.save()
        new_mailing.subscribers.add(*subscribers)
        new_mailing.save()
        self.message_user(request, '%s succesfully created.' % new_mailing)
    make_mailing_list.short_description = 'Create a mailing list'

    actions = ['make_mailing_list']
