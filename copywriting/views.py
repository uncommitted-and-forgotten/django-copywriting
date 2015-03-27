# -*- coding: utf-8 -*-
import datetime
import urllib

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import *

from .helperFunctions import getLatestArticles
from .helperFunctions import getArticlesByDate 
from .helperFunctions import getYearCount
from .helperFunctions import getLatestArticlesByAuthor




def listArticles(request):
    """
    """
    articles = getLatestArticles(100)
    return render_to_response('copywriting/copywritingIndex.html', {'articles': articles,
                                                                    'yearCount': getYearCount(),
                                                                   }, context_instance=RequestContext(request))

def listArticlesByAuthor(request, author):
    """
    author is the username of the user in the author model.
    """
    authorProfile = AuthorProfile.objects.get(user__username=author)
    articles = getLatestArticlesByAuthor(ContentType.objects.get_for_model(authorProfile), authorProfile.id, 100)
    return render_to_response('copywriting/copywritingIndex.html', {'articles': articles,
                                                                    'yearCount': getYearCount(),
                                                                    'authorProfile': authorProfile,
                                                                   }, context_instance=RequestContext(request))

    
def listArticlesByYear(request, requestYear):
    """
    """
    articles = getArticlesByDate(year=requestYear)
    return render_to_response('copywriting/copywritingIndex.html', {'articles': articles,
                                                                    'yearCount': getYearCount(),
                                                                   }, context_instance=RequestContext(request))


def listArticlesByYearMonth(request, requestYear, requestMonth):
    """
    """
    articles = getArticlesByDate(year=requestYear, month=requestMonth)
    return render_to_response('copywriting/copywritingIndex.html', {'articles': articles,
                                                                    'yearCount': getYearCount(),
                                                                   }, context_instance=RequestContext(request))


def listArticlesByYearMonthDay(request, requestYear, requestMonth, requestDay):
    """
    """
    articles = getArticlesByDate(year=requestYear, month=requestMonth, day=requestDay)
    return render_to_response('copywriting/copywritingIndex.html', {'articles': articles,
                                                                    'yearCount': getYearCount(),
                                                                   }, context_instance=RequestContext(request))


def withTag(request, in_tag):
    lTag = urllib.unquote(in_tag)
    tags = Tag.objects.filter(name=lTag)
    articles = Article.objects.filter(tags__in=tags, status=Article.PUBLISHED, pubDate__lte=timezone.now()).order_by('-pubDate')

    return render_to_response("copywriting/copywritingIndex.html", {'tag': in_tag,
                                                                    'articles': articles,
                                                                    'yearCount': getYearCount(),
                                                                   }, context_instance=RequestContext(request))


def showArticle(request, slug):
    """
    """
    if request.user.is_staff or request.user.is_superuser:
        article = get_object_or_404(Article, slug=slug)
    else:
        article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)

    if article:
        latestArticlesList = getLatestArticlesByAuthor(article.authorProfileModel, article.authorProfileId, 5, slug)

    return render_to_response('copywriting/copywritingArticle.html', {'article': article,
                                                                      'latestArticlesList': latestArticlesList,
                                                                     }, context_instance=RequestContext(request))
