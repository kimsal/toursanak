"""toursanak URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import *
from django.conf.urls import include, url
#import css js image ...
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()
urlpatterns = [
    # url(r'^search-form/$',"toursanak.views.search",name="search"),
    url(r'^search/$', "toursanak.views.search", name="search"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "toursanak.views.index", name='index'),
    url(r'^(\d+)/(\d+)/booking/', "toursanak.views.booking", name='booking'),
    

    url(r'^contact/', "toursanak.views.contact", name='contact'),
    url(r'^cat/(?P<slug>[-\w\d]+)/$', 'toursanak.views.category', name='category'),
    url(r'^createContact/', "toursanak.views.createContact", name='createContact'),
    url(r'^(\d+)/(\d+)/createbooking/', "toursanak.views.createBooking", name='createBooking'),
    url(r'^(?P<slug>[-\w\d]+)/$', 'toursanak.views.single', name='single'),
    url(r'^scroll/(\d+)/$', "toursanak.views.PostScroll", name='scroll'),
    url(r'^scrollCategory/(\w+)/(\d+)/$', "toursanak.views.scrollCategory", name='scrollcategory'),

]


if settings.DEBUG:	
	urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
