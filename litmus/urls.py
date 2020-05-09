from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.conf import settings

urlpatterns= [
 # path('',views.index, name='index'),
  path('',views.home_view,name='home'),
  #path('',views.index,name='index'),
  path('signup/',views.signup_view,name='signup'),
  #path('',views.login_view,name='login'),
  path('sent/',views.activation_sent_view,name='activation_sent'),
  path('activate/<slug:uidb64>/<slug:token>/',views.activate,name='activate'),
  path('logout/',views.logout_view,name='logout'),
  path('send_request/',views.send_friend_request,name='friend_request_sent'),
  path('friend_requests/',views.incoming_friend_request,name='incoming_friend_request'),
  path('friend_requests/accept/',views.accept_friend_request,name='friend_request'),
  path('show_friends',views.show_friends,name='show_friends'),
  path('add/',views.add,name='add'),
  path('notes_list/',views.show_notes,name ='show_notes')
]

urlpatterns += static((settings.STATIC_URL), document_root=(settings.STATIC_ROOT))
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static((settings.MEDIA_URL), document_root=(settings.MEDIA_ROOT))
