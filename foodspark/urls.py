from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/$',views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^search/$',views.search,name='search'),
    url(r'^(?P<restname>[a-zA-Z0-9\s]+)$',views.restview,name='restview'),
]