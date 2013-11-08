# -*- coding: utf-8 -*-
from django import template
from copywriting.helperFunctions import getLatestArticles
from copywriting.models import Tag

register = template.Library()


@register.filter
def get_latest_slug(request):
    latest = getLatestArticles(1)
    return latest.slug


@register.filter
def get_latest_articles(request):
    return getLatestArticles(5)


@register.filter
def get_tags(request):
	return Tag.objects.all()


@register.simple_tag
def get_gravatar_url_by_email(email, size=48):
    """
    Simply gets the Gravatar Url for the a email Adress. There is no rating or
    custom "not found" icon yet. Used with the Django comments.

    If no size is given, the default is 48 pixels by 48 pixels.

    Template Syntax::

        {% gravatarUrl comment.user_email [size] %}

    Example usage::

        {% gravatarUrl comment.user_email 48 %}
    """
    import urllib
    import hashlib

    url = "https://secure.gravatar.com/avatar.php?"
    url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(),
        'size': str(size)
    })

    return url