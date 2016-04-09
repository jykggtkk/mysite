"""mysite URL Configuration

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
from django.conf import settings
from django.conf.urls import patterns, include, url 
from django.contrib import admin
urlpatterns = [
<<<<<<< HEAD
    url(r'^admin/', admin.site.urls),  
=======
    url(r'^admin/', admin.site.urls),
    url(r'^polls/', include('polls.urls')),
>>>>>>> 0bc82bfefe2474741781d112d46fce14eec86088
    url(r'^tango/', include('tango.urls')), 
    url(r'^polls/', include('polls.urls',namespace="polls")), 
    ]
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
