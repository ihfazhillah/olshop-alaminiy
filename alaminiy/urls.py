"""alaminiy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^toko/', include('toko.urls')),
    url(r'^profil/' ,include('profil.urls')),
] 
# if settings.DEBUG:
#     urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += patterns(
    #     'django.views.static',
    #     (r'^media/(?P<path>.*)',
    #     'serve',
    #     {'document_root': settings.MEDIA_ROOT}),
    #      )

    # urlpatterns += patterns('',
    #     url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  {
    #         'document_root': settings.MEDIA_ROOT,
    #     }, name ="mediaupload",),
    # )

