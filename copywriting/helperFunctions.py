# -*- coding: utf-8 -*-
from datetime import datetime
from .models import Article


def getLatestArticles(amount=5):
    """returs the latest n published Articles
    """
    try:
        articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now()).order_by('-pubDate')[:amount]
    except:
        articles = None

    if amount == 1 and articles:
        articles = articles[0]

    return articles

def getLatestArticlesByAuthor(authorModel, authorId, amount=5, toExclude=None):
    """
    """
    articles = Article.objects.filter(status=Article.PUBLISHED, pubDate__lte=datetime.now(), authorProfileModel=authorModel, authorProfileId=authorId).exclude(slug=toExclude).order_by('-pubDate')[:amount]
    return articles


def getYearCount():
    """return a list of years an count of Articles for this year
    like:
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
