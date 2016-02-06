from django.db import models
from django.template.defaultfilters import slugify
from versatileimagefield.fields import VersatileImageField
# Create your models here.

class Kategori(models.Model):
    nama = models.CharField(max_length = 150,
                            unique = True)
    slug = models.SlugField(max_length = 200,
                            allow_unicode = True)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.slug = slugify(self.nama)
        super(Kategori,self).save(*args, **kwargs)

    def __str__(self):
        return self.nama

class Barang(models.Model):
    kategori = models.ManyToManyField(Kategori, blank=True)
    judul = models.CharField(max_length = 250)
    ikhtisar = models.TextField()
    harga = models.IntegerField(default=0)
    slug = models.SlugField(max_length = 300,
                            allow_unicode = True)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.slug = slugify(self.judul)
        super(Barang,self).save(*args, **kwargs)

    def __str__(self):
        return self.judul

class Atribut(models.Model):
    nama = models.CharField(max_length = 150)
    isi = models.CharField(max_length = 150)
    barang = models.ForeignKey(Barang)

    def __str__(self):
        return "%s : %s" %(self.nama, self.isi)

class Gambar(models.Model):
    image = VersatileImageField(upload_to = 'gambar_produk')
    barang = models.ForeignKey(Barang)

    # def __str__(self):
    #     return self.url

    
