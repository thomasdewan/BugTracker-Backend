from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^issue/$', views.IssueList.as_view()),
    url(r'^issue/(?P<pk>[0-9]+)$', views.IssueDetail.as_view()),
    url(r'^comment/$', views.CommentList.as_view()),
    url(r'^comment/(?P<pk>[0-9]+)$', views.CommentDetail.as_view()),
    url(r'^state/$', views.StateList.as_view()),
    url(r'^user/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)$', views.UserDetail.as_view()),
    url(r'^commentForIssue/(?P<pk>[0-9]+)$', views.CommentForIssueList.as_view()),
    url(r'^register/$', views.UserRegister.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)