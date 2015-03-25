from compat import patterns, url
from .feed import blogFeed

urlpatterns = patterns('copywriting',
    url(r'^feed\.rss$', blogFeed()),
    url(r'^feed/$', blogFeed()),
    url(r'^author/(?P<author>\w[^/]+)$', 'views.listArticlesByAuthor'),
    url(r'^author/(?P<author>\w[^/]+)/$', 'views.listArticlesByAuthor'),
    url(r'^tag/(?P<in_tag>\w[^/]+)$', 'views.withTag'),
    url(r'^tag/(?P<in_tag>\w[^/]+)/$', 'views.withTag'),
    # (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'views.listBlogEntriesByYearMonthDay'),
    url(r'^(?P<requestYear>\d+)/(?P<requestMonth>\d+)/$', 'views.listArticlesByYearMonth'),
    url(r'^(?P<requestYear>\d+)/$', 'views.listArticlesByYear'),
    url(r'^(?P<slug>[^\.]+)/$', 'views.showArticle'),
    url('^$', 'views.listArticles'),
)
