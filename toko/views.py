from django.shortcuts import render

from toko.models import Barang, Kategori
from profil.models import Profil
# Create your views here.
def home_page(request):
    barang = Barang.objects.all().order_by("-id")[:4]
    profil = Profil.objects.get(slug="toko-al-aminiy")
    return render(request, "toko/home_page.html", {"barang" : barang,
                  "index":True, "profil":profil})

def produk_detail(request, barang_slug ):
    profil = Profil.objects.get(slug="toko-al-aminiy")
    produk = Barang.objects.get(slug=barang_slug)
    return render(request, "toko/produk_detail.html", {"barang" : produk,
                  "profil":profil})

def kategori(request, kategori_slug):
    profil = Profil.objects.get(slug="toko-al-aminiy")
    kategori = Kategori.objects.get(slug=kategori_slug)
    
    return render(request, "toko/kategori.html", {"kategori":kategori,
                  "profil":profil})