from django.conf.urls import url 
from toko import views

urlpatterns = ( url(r'^$', views.home_page, name="home_page" ),
                url(r'^barang/(?P<barang_slug>.+)/$', views.produk_detail, name="produk_detail"),
                url(r'^kategori/(?P<kategori_slug>.+)/$', views.kategori, name="kategori_barang"),
               )