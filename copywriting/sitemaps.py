# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import Article


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.objects.filter(status=Article.PUBLISHED).order_by('-pubDate')

    def lastmod(self, obj):
        return obj.pubDate
