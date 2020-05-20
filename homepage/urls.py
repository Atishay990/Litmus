from django.conf.urls import url
from . import views

app_name = 'homepagedemo'

urlpatterns = [
    # /homepagedemo/user_id/
    url(r'^(?P<user_id>[0-9]+)/$', views.index, name = 'index'),
    # /homepagedemo/user_id/addnotes/
    url(r'^(?P<user_id>[0-9]+)/addnotes/$', views.add, name = 'add'),
    #/homepagedemo/Errors/error_code/
    url(r'^errors/(?P<error_code>[0-9]+)/$', views.errors, name = 'errors'),
]