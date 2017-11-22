from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index' ),
    url(r'^retrieve/$',views.retrieve,name="retrieve"),
    url(r'^addws/$',views.addws,name="addws"),
    url(r'^remove/$',views.remove,name="remove"),
    url(r'^editws/$',views.editws,name="editws"),
     url(r'^edittank/$',views.edittank,name="edittank"),
    url(r'^editplant/$',views.editplant,name="editplant"),
    url(r'^update/$',views.updateprofile,name="updateprofile"),
    url(r'^addtank/$',views.addtank,name="addtank"),
    url(r'^add/$',views.addplant,name="addplant"),
    url(r'^register/$',views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^dashboard/$', views.profile, name='profile'),
]
