# -*- coding: utf-8 -*-
from datetime import datetime
from .models import Article, Tag


def getLatestArticlesByTag(amount=5, tagString=None):
    """
    Returns the latest n (=amount) published Articles that has all tags.
    Tags is tagString exploded using ",".
    
    """
    try:
        articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now()).order_by('-pubDate')
    except:
        articles = None
    tags = []
    if articles:
        tags = tagString.split(",")
    for tag in tags:
        articles = articles.filter(tags__name=tag)
 
    return articles[:amount]
    

def getLatestArticles(amount=5):
    """
    Returns the latest n (=amount) published Articles
    """
    try:
        articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now()).order_by('-pubDate')[:amount]
    except:
        articles = None

    if amount == 1 and articles:
        articles = articles[0]
    return articles


def getArticlesByAuthor(authorModel, authorId, toExclude=None):
    """
    Returns all published Articles for an author
    """
    articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now(), authorProfileModel=authorModel, authorProfileId=authorId).exclude(slug=toExclude).order_by('-pubDate')
    return articles


def getLatestArticlesByAuthor(authorModel, authorId, amount=5, toExclude=None):
    """
    Returns the latest n (=amount) published Articles for an author
    """
    articles = getArticlesByAuthor(authorModel, authorId, toExclude=toExclude)
    return articles[:amount]


def getTagsByAuthor(authorModel, authorId):
    """
    Returns all Tags that an author has used in this articles
    """
    tags_ids = []

    author_articles = getArticlesByAuthor(authorModel, authorId)
    
    for article in author_articles:
        for tag in article.tags.all():
            tags_ids.append(tag.id)

    return Tag.objects.filter(id__in=tags_ids)


def getYearCount():
    """
    Return a list of years an count of Articles for this year like:
    yearCount = [[2012, 3],[2011, 43],[2010, 74]]"""
    years = Article.objects.dates('pubDate', 'year')
    yearCount = []

    for year in years:
        year = int(year.year)
        count = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now(), pubDate__year=year).count()
        yearCount.append([year, count])

    return sorted(yearCount, reverse=True)


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


def getArticlesByYear(year):
    try:
        articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now(), pubDate__year=year).order_by('-pubDate')
    except Exception:
        articles = None
    return articles


def getArticlesByYearMonth(year, month):
    try:
        articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now(), pubDate__year=year, pubDate__month=month).order_by('-pubDate')
    except Exception:
        articles = None
    return articles


def getArticlesByYearMonthDay(year, month, day):
    try:
        articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now(), pubDate__year=year, pubDate__month=month, pubDate__day=day).order_by('-pubDate')
    except Exception:
        articles = None
    return articles
