from compat import patterns, url


urlpatterns = patterns('copywriting',
    url(r'^author/(?P<author>\w[^/]+)$', 'views.listArticlesByAuthor'),
    url(r'^author/(?P<author>\w[^/]+)/$', 'views.listArticlesByAuthor', name='copywriting_by_author'),
    url(r'^tag/(?P<in_tag>\w[^/]+)$', 'views.withTag'),
    url(r'^tag/(?P<in_tag>\w[^/]+)/$', 'views.withTag', name='copywriting_by_tag'),
    # (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'views.listBlogEntriesByYearMonthDay'),
    url(r'^(?P<requestYear>\d+)/(?P<requestMonth>\d+)/$', 'views.listArticlesByYearMonth', name='copywriting_by_month'),
    url(r'^(?P<requestYear>\d+)/$', 'views.listArticlesByYear', name='copywriting_by_year'),
    url(r'^(?P<slug>[^\.]+)/$', 'views.showArticle', name='copywriting_article'),
    url('^$', 'views.listArticles', name='copywriting_index'),
)

try:
    from .feed import blogFeed
    urlpatterns += patterns('copywriting',
        url(r'^feed\.rss$', blogFeed()),
        url(r'^feed/$', blogFeed()),
    )
except Exception, ex:
    print ex
    pass
