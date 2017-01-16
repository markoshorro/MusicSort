from django.conf.urls import include, patterns, url
from web import views

urlpatterns=patterns('',
	url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^dragdrop/$', views.dragdrop, name='dragdrop'),
    url(r'^del_file/$', views.del_file, name='del_file'),
    url(r'^process_songs/$', views.process_songs, name='process_songs'),
    url(r'^register/', views.register, name='register'),
	url(r'^delete_user_file/', views.delete_user_file, name='delete_user_file'),
)
