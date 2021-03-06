from django.test import TestCase

# Create your tests here.
from profil.models import Profil, SocialMedia, Phone, Email

class ProfilModelTest(TestCase):

    def test_can_create_object_and_retrieve_it(self):
        Profil.objects.create(nama="alaminiy",
                              tagline="ini tagline",
                              deskripsi="ini deskripsi",
                              alamat="ini alamat",
                              slug="alaminiy")
        profil = Profil.objects.first()
        self.assertEqual(profil.slug, "alaminiy")
        self.assertEqual(profil.nama, "alaminiy")
        self.assertEqual(profil.tagline, "ini tagline")
        self.assertEqual(profil.deskripsi, "ini deskripsi")
        self.assertEqual(profil.alamat, "ini alamat")

class SocialMediaModelTest(TestCase):

    def test_can_create_object_and_retrieve_it(self):
        profil = Profil.objects.create(nama="alaminiy",
                              tagline="ini tagline",
                              deskripsi="ini deskripsi",
                              alamat="ini alamat")
        social = SocialMedia.objects.create(profil=profil,
                                   provider="provider1",
                                   url="http://provider.com")
        self.assertEqual(social.profil.nama, "alaminiy")
        self.assertEqual(social.profil.tagline, "ini tagline")
        self.assertEqual(social.profil.deskripsi , "ini deskripsi")
        self.assertEqual(social.profil.alamat, "ini alamat")
        self.assertEqual(social.provider, "provider1")
        self.assertEqual(social.url, "http://provider.com")

class PhoneModelTest(TestCase):

    def test_can_create_object_and_retrieve_it(self):
        profil = Profil.objects.create(nama="alaminiy",
                              tagline="ini tagline",
                              deskripsi="ini deskripsi",
                              alamat="ini alamat")

        phone_s = Phone.objects.create(profil = profil,
                                     nomor = 1234,
                                     tipe="s")
        phone_p = Phone.objects.create(profil= profil,
                                       nomor=3241,
                                       tipe="p")

        self.assertEqual(profil.phone.count(), 2)
        self.assertEqual(profil.phone.first().nomor, "1234")
        self.assertEqual(profil.phone.first().get_tipe_display(), "secondary")
        self.assertEqual(profil.phone.all()[1].nomor, "3241")
        self.assertEqual(profil.phone.all()[1].get_tipe_display(), "primary")

    def test_primer_phone_tipe_must_be_one_else_change_it_to_secondary(self):
        profil = Profil.objects.create(nama="alaminiy",
                                       tagline="ini tagline",
                                       deskripsi = "ini deskripsi",
                                       alamat = "ini alamat"
                                       )
        Phone.objects.create(profil=profil, nomor='1346555', tipe='p')
        Phone.objects.create(profil=profil, nomor='145454555', tipe='p')
        self.assertEqual(profil.phone.count(), 2)
        self.assertNotEqual(profil.phone.first().tipe, profil.phone.last().tipe)
        self.assertEqual(profil.phone.all()[1].tipe , 's')

class EmailModelTest(TestCase):

    def setUp(self):
        

        self.profil = Profil.objects.create(nama="alaminiy",
                              tagline="ini tagline",
                              deskripsi="ini deskripsi",
                              alamat="ini alamat")

        self.email = Email.objects.create(alamat="alamat1@coba.com",
                                     tipe="p",
                                     profil=self.profil)
    
        self.email_s = Email.objects.create(profil=self.profil,
                                       alamat="alamat2@coba.com",
                                       tipe="s",
                                       )


    def test_can_create_object_and_retrieve_it(self):
        
        self.assertEqual(self.profil.email.count(), 2)
        self.assertEqual(self.email.profil.nama, self.profil.nama)
        self.assertEqual(self.email.alamat, "alamat1@coba.com")
        self.assertEqual(self.email.get_tipe_display(), "primary")
        self.assertEqual(self.email_s.profil.nama, self.profil.nama)
        self.assertEqual(self.email_s.alamat, "alamat2@coba.com")
        self.assertEqual(self.email_s.get_tipe_display(), "secondary")

    def test_override_tipe_input_if_it_primary_twice(self):
        self.email_s.tipe = "p"
        self.email_s.save()
        self.assertEqual(self.profil.email.count(), 2)
        self.assertEqual(self.email_s.tipe, 's')
        

