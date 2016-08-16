from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^about/$', views.about, name='about'),
  url(r'^contact/$', views.contact, name='contact'),
  url(r'permalink/(?P<slug>[-\w\d\_]+)/$', views.singlepost, name='post_permalink'),
  url(r'categories/(?P<word>[-\w\d\_]+)$', views.categories, name='category_permalink')
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
