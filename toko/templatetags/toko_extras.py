from django import template
from toko.models import Kategori
from profil.models import Profil

register = template.Library()

@register.inclusion_tag("toko/cat.html")
def dapatkan_semua_kategori():
    return {"cats":Kategori.objects.all()}

@register.inclusion_tag("profil/head.html")
def dapatkan_profil():
    return {"profil":Profil.objects.first()}

@register.filter
def currency(value):
    import locale
    locale.setlocale(locale.LC_ALL, '')
    if value:
        return locale.currency(value, grouping=True, international=True)
    else:
        return ''