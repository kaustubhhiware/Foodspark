from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^home/?$',views.home, name='home'),
    url(r'^signup/?$', views.signup, name='signup'),
    url(r'^search/?$',views.search,name='search'),
    url(r'^details/?$',views.details,name='details'),
    url(r'^savedetails/?$',views.editDetails,name='editDetails'),
    url(r'^cart/?$',views.cart,name='cart'),
    url(r'^history/?$',views.history,name='history'),
    url(r'^addtocart/?$',views.saveToCart,name='saveToCart'),
    url(r'^restprofile/?$',views.restprofile,name='restprofile'),
    url(r'^resthistory/?$',views.restaurantOrderHistory,name='resthistory'),
    url(r'^delivered/?$',views.delivered,name='delivered'),
    url(r'^addfooditem/?$',views.addfooditem,name='addfooditem'),
    url(r'^removefooditem/?$',views.removefooditem,name='removefooditem'),

    # url(r'^makepaymenet/?$'.views.makepaymenet,name='makepaymenet'),
    url(r'^restaurant/(?P<restname>[a-zA-Z0-9\s]+)/?$',views.restview,name='restview'),
    url(r'^about/?$',views.about,name='about'),
]
