from django.contrib import admin
from toko.models import Kategori, Barang, Atribut, Gambar
# from sorl.thumbnail.admin import AdminImageMixin 
# Register your models here.
from profil.models import Profil, Phone, SocialMedia, Email

class AtributInline(admin.TabularInline):
    model = Atribut

class GambarInline(admin.TabularInline):
    model = Gambar 

class BarangAdmin(admin.ModelAdmin):
    inlines = [
        AtributInline,
        GambarInline,
    ]
admin.site.register(Kategori)
admin.site.register(Barang, BarangAdmin)

class PhoneInline(admin.StackedInline):
    model = Phone
class SocialMediaInline(admin.StackedInline):
    model = SocialMedia
class EmailInline(admin.TabularInline):
    model = Email
class ProfilAdmin(admin.ModelAdmin):
    inlines=[PhoneInline,
    SocialMediaInline,
    EmailInline]
admin.site.register(Profil, ProfilAdmin)
