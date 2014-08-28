# -*- coding: utf-8 -*-
from django import template
from copywriting.helperFunctions import getLatestArticles
from copywriting.helperFunctions import getLatestArticlesByTag
from copywriting.helperFunctions import getTags
from copywriting.helperFunctions import getArticles

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



@register.assignment_tag
def next(current_Articel):
    articles = getArticles()
    newer_articles = []

    for article in articles:
        if article.pubDate > current_Articel.pubDate:
            newer_articles.append(article)

    if newer_articles == []:
        return False
        #return False

    else:
        next = newer_articles[0]

    for article in newer_articles:
        if article.pubDate < next.pubDate:
            next = article

    return next

@register.assignment_tag
def prev(current_Articel):
    articles = getArticles()
    older_articles = []

    for article in articles:
        if article.pubDate < current_Articel.pubDate:
            older_articles.append(article)

    if older_articles == []:
        return False
        #return False

    else:
        prev = older_articles[0]

    for article in older_articles:
        if article.pubDate > prev.pubDate:
            prev = article

    return prev

@register.assignment_tag
def getNewest(count=1):
    return getLatestArticles(count)
