from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

# from blog.sitemaps import PostSitemap
# from meduzer.meduzer.views import redirect_blog

# sitemaps = {
#     "posts": PostSitemap,
# }

urlpatterns = [
    # path('', redirect_blog),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("blog/", include("blog.urls")),
    # path(
    #     "sitemap.xml",
    #     sitemap,
    #     {"sitemaps": sitemaps},
    #     name="django.contrib.sitemaps.views.sitemap",
    # ),
    path("social-auth/", include("social_django.urls", namespace="social")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
