from django.conf.urls import url
from profil import views

urlpatterns = [url(r"^$", views.profil, name="profil_view" ),
                url(r'^edit/$', views.profil_edit, name='profil_edit'),
                url(r'^api/$', views.profil_api, name='profil-api')
                ]