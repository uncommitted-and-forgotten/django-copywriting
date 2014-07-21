# -*- coding: utf-8 -*-
from django import template
from copywriting.helperFunctions import getLatestArticles
from copywriting.helperFunctions import getLatestArticlesByTag
from copywriting.helperFunctions import getTags

register = template.Library()


@register.filter
def get_latest_slug(request):
    latest = getLatestArticles(1)
    return latest.slug


@register.assignment_tag
def get_latest_articles_by_tag( *args, **kwargs):
    """
    Usage:
    
    {% get_latest_articles_by_tag tagString="Technology,Biology,Match" amount=5 as articles %}
    
    {% for article in articles %}
        {{ article.title }}
    {% endfor %}
    
    Notes: If tagString is not defined or an empty string, 'getLatestArticles' will be called.
    """
    amount = kwargs.get('amount',5)
    tagString = kwargs.get('tagString', None)
    if tagString is None or tagString == '':
        return getLatestArticles(amount)
    return getLatestArticlesByTag(amount, tagString=tagString)
 

@register.filter
def get_latest_articles(request):
    return getLatestArticles(5)


@register.filter
def get_tags(request):
    return getTags()


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
