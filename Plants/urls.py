from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index' ),
    url(r'^retrieve/$',views.retrieve,name="retrieve"),
    url(r'^add/$',views.addplant,name="addplant"),
    url(r'^register/$',views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^dashboard/$', views.profile, name='profile'),
]
