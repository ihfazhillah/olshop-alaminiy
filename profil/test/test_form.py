from profil.models import Phone, Profil
from django.test import TestCase
from profil.forms import PhoneForm, EmailForm, SocialForm

def make_profile(nama, tagline='', deskripsi='', alamat=''):
    return Profil.objects.create(nama=nama, tagline=tagline,
                                 deskripsi=deskripsi, alamat=alamat)

class PhoneModelTest(TestCase):
    def setUp(self):
        self.profil = make_profile('ihfazh')

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            PhoneForm()

    def test_valid_data(self):
        data = {'nomor':'12345', 'tipe':'p'}
        form = PhoneForm(data, profil=self.profil)
        self.assertTrue(form.is_valid())
        phone = form.save()
        self.assertEqual(phone.nomor, '12345')
        self.assertEqual(phone.tipe, 'p')
        self.assertEqual(phone.profil, self.profil)

    def test_invalid_data(self):
        data = {}
        form = PhoneForm(data, profil=self.profil)
        self.assertFalse(form.is_valid())


class EmailFormTest(TestCase):
    def setUp(self):
        self.profil = make_profile('ihfazh')

    def test_ini_without_entry(self):
        with self.assertRaises(KeyError):
            EmailForm()

    def test_valid_data(self):
        data = {'alamat':'email@me.com', 'tipe':'p'}
        form = EmailForm(data, profil=self.profil)
        self.assertTrue(form.is_valid())
        email = form.save()
        self.assertEqual(email.alamat, 'email@me.com')
        self.assertEqual(email.tipe, 'p')
        self.assertEqual(email.profil, self.profil)

    def test_invalid_data(self):
        data = {}
        form = EmailForm(data, profil=self.profil)
        self.assertFalse(form.is_valid())

class SocialFormTest(TestCase):
    def setUp(self):
        self.profil = make_profile('ihfazh')

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            SocialForm()

    def test_with_valid_data(self):
        data = {'provider':'aku', 'url':'http://aku.com'}
        form = SocialForm(data, profil = self.profil)
        self.assertTrue(form.is_valid())
        social = form.save()
        self.assertEqual(social.provider, 'aku')
        self.assertEqual(social.url , 'http://aku.com')

    def test_with_invalid_data(self):
        data = {}
        form = SocialForm(data, profil=self.profil)
        self.assertFalse(form.is_valid())

