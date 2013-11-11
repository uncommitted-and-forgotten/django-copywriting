from django.conf.urls.defaults import *
from .feed import blogFeed

urlpatterns = patterns('copywriting',
    (r'^feed\.rss$',                                    blogFeed()),
    (r'^feed/$',                                        blogFeed()),
    (r'^tag/(?P<in_tag>\w+)/$',	                        'views.withTag'),
    # (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'views.listBlogEntriesByYearMonthDay'),
    (r'^(?P<requestYear>\d+)/(?P<requestMonth>\d+)/$',	'views.listArticlesByYearMonth'),
    (r'^(?P<requestYear>\d+)/$',                        'views.listArticlesByYear'),
    (r'^(?P<slug>[^\.]+)/$',                            'views.showArticle'),
    (r'^$',                                             'views.listArticles'),
)
