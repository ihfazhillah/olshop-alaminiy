from django.db import models

# Create your models here.

class Profil(models.Model):
    nama = models.CharField(max_length=100)
    tagline = models.CharField(max_length=250)
    deskripsi = models.TextField()
    alamat = models.CharField(max_length=500)
    slug = models.SlugField(default="")

    def __str__(self):
        return self.nama

class Kontak(models.Model):
    pass

class SocialMedia(models.Model):
    profil = models.ForeignKey(Profil, default="", related_name="socialmedia")
    provider = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.provider

   



class Phone(models.Model):
    profil = models.ForeignKey(Profil, related_name="phone")
    nomor = models.CharField(max_length=20)
    TIPE_CHOICE = (
                   ("p", "primary"),
                   ("s", "secondary")
                   )
    tipe = models.CharField(max_length=1, choices=TIPE_CHOICE)

    def __str__(self):
        return str(self.nomor)

    def save(self, *args, **kwargs):
        phones = Phone.objects.all()
        phone_tipe = [p.tipe for p in phones]
        if self.tipe in phone_tipe:
            self.tipe = "s"
        super(Phone, self).save(*args, **kwargs)	

class Email(models.Model):
    TIPE_CHOICE = (
                   ("p", "primary"),
                   ("s", "secondary")
                   )
    profil = models.ForeignKey(Profil, related_name='email')
    alamat = models.EmailField()
    tipe = models.CharField(max_length=1, choices=TIPE_CHOICE)

    def __str__(self):
        return self.alamat

    def save(self, *args, **kwargs):
        emails = Email.objects.all()
        email_tipe = [e.tipe for e in emails]
        if 'p' in email_tipe:
            self.tipe = 's'
        super(Email, self).save(*args, **kwargs)

