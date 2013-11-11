# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.conf import settings
from .helperFunctions import getLatestArticles
import logging

logger = logging.getLogger(__name__)


class blogFeed(Feed):
    if hasattr(settings, 'FEED_SETTINGS'):
        title = settings.FEED_SETTINGS.get('title', "")
        link = settings.FEED_SETTINGS.get('link', "")
        description = settings.FEED_SETTINGS.get('description', "")
        author_email = settings.FEED_SETTINGS.get('author_email', "")
        author_name = settings.FEED_SETTINGS.get('author_name', "")
        author_link = settings.FEED_SETTINGS.get('author_link', "")
        feed_url = settings.FEED_SETTINGS.get('feed_url', "")
        categories = settings.FEED_SETTINGS.get('categories', "")
    else:
        logger.error('settings has no attribute FEED_SETTINGS that are required for the Feed')

    def items(self):
        return getLatestArticles(5)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
