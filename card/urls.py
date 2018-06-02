from django.conf.urls import url

from . import views

urlpatterns = {
    url('', views.BusinessCard.as_view(), name='card'),
    url('^delete/$', views.Delete.as_view(), name='delete'),
}
