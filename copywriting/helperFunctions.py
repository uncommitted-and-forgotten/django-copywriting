# -*- coding: utf-8 -*-
from datetime import datetime
from .models import Article, Tag
from django.utils import timezone


def getLatestArticlesByTag(amount=5, tagString=None):
    """
    Returns the latest n (=amount) published Articles that have all tags.
    Tags is tagString exploded using ",".
    
    """
    articles = getArticles()
    tags = []
    
    if articles:
        tags = tagString.split(",")
    
    for tag in tags:
        articles = articles.filter(tags__name=tag)
 
    return articles[:amount]
    

def getArticles():
    """
    Returns all published Articles
    """
    try:
        articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=timezone.now()).order_by('-pubDate')
    except:
        articles = None

    return articles


def getLatestArticles(amount=5):
    """
    Returns the latest n (=amount) published Articles
    """
    articles = getArticles()
    
    if amount == 1 and articles:
        return articles[0]
    
    return articles[:amount]


def getArticlesByAuthor(authorModel, authorId, toExclude=None):
    """
    Returns all published Articles for an author
    """
    articles = getArticles().filter(authorProfileModel=authorModel, authorProfileId=authorId).exclude(slug=toExclude)
    
    return articles


def getLatestArticlesByAuthor(authorModel, authorId, amount=5, toExclude=None):
    """
    Returns the latest n (=amount) published Articles for an author
    """
    articles = getArticlesByAuthor(authorModel, authorId, toExclude=toExclude)
    
    return articles[:amount]


def getTags():
    """
    Returns all Tags that are used, Tags not linked to published Articles are excluded
    """
    tags_ids = []

    articles = getArticles()
    
    for article in articles:
        for tag in article.tags.all():
            tags_ids.append(tag.id)

    return Tag.objects.filter(id__in=tags_ids).order_by('name')


def getTagsByAuthor(authorModel, authorId):
    """
    Returns all Tags that an author has used in this articles
    """
    tags_ids = []

    author_articles = getArticlesByAuthor(authorModel, authorId)
    
    for article in author_articles:
        for tag in article.tags.all():
            tags_ids.append(tag.id)

    return Tag.objects.filter(id__in=tags_ids).order_by('name')


def getYearCount():
    """
    Return a list of years an count of Articles for this year like:
    yearCount = [[2012, 3],[2011, 43],[2010, 74]]"""
    try:    
        years = Article.objects.datetimes('pubDate', 'year')
    except AttributeError:
        years = Article.objects.dates('pubDate', 'year')
    
    yearCount = []

    for year in years:
        year = int(year.year)
        count = getArticles().filter(pubDate__year=year).count()
        yearCount.append([year, count])

    return sorted(yearCount, reverse=True)


def getArticlesByYear(year):
    try:
        articles = getArticles().filter(pubDate__year=year)
    except Exception:
        articles = None
    return articles


def getArticlesByYearMonth(year, month):
    try:
        articles = getArticles().filter(pubDate__year=year, pubDate__month=month)
    except Exception:
        articles = None
    return articles


def getArticlesByYearMonthDay(year, month, day):
    try:
        articles = getArticles().filter(pubDate__year=year, pubDate__month=month, pubDate__day=day).order_by('-pubDate')
    except Exception:
        articles = None
    return articles


def getArticlesByDate(**kwargs):
    """based on the keywords retuns a list of Articles for a specific date
    keywords can be: year, month and day"""
    if 'year' in kwargs and 'month' in kwargs and 'day' in kwargs:
        articles = getArticlesByYearMonthDay(kwargs['year'], kwargs['month'], kwargs['day'])
    elif 'year' in kwargs and 'month' in kwargs:
        articles = getArticlesByYearMonth(kwargs['year'], kwargs['month'])
    elif 'year' in kwargs:
        articles = getArticlesByYear(kwargs['year'])
    else:
        articles = None

    return articles
