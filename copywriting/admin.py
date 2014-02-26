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
        return u'%s' %  obj.number_of_words()
    #number_of_words.admin_order_field = 'number_of_words'
        
    # prepopulated_fields = {'slug':('title',),}

    list_display = ('title', 'number_of_words', 'status', 'pubDate', 'addedDate', 'updatedDate')
    readonly_fields = ('addedDate', 'updatedDate',)
    list_filter = ('status', 'authorProfileId', )
    search_fields = ['title', 'slug', 'desc']
    
    if "redactormedia" in settings.INSTALLED_APPS:
        from redactormedia.widgets import RedactorWithMediaEditor, AdminRedactorWithMediaEditor
        from django.db import models
    
        formfield_overrides = {
            models.TextField: {'widget': AdminRedactorWithMediaEditor},
        }
        
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(AuthorProfile)
