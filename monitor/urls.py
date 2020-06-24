from django.conf.urls import url

from monitor import views

urlpatterns = [
    url(r'^$', views.MainPage.as_view())
]
