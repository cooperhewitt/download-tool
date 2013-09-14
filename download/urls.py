from django.conf.urls import patterns, url

from download import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
	url(r'^search/$', views.search, name='search'),
	url(r'^thanks/$', views.thanks, name='thanks'),
	
	url(r'^login/$', views.login_page, name='login'),
	url(r'^logout/$', views.logout_page, name='logout'),
	url(r'^account/$', views.account, name='account'),
)