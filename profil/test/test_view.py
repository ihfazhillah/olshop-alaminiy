from django.test import TestCase
from django.core.urlresolvers import reverse
from profil.models import Profil
class ProfilViewTest(TestCase):

    def test_view_can_display_profil(self):
        profil = Profil.objects.create(nama="nama",
                                       slug="nama",
                                       tagline="tagline",
                                       deskripsi="deskripsi",
                                       alamat="alamat")
        profil.socialmedia_set.create(provider="facebook",
                                      url="http://facebook.com")
        profil.phone_set.create(nomor=12345,
                                tipe="p")
        email = profil.email_set.create(alamat="coba@coba.com",
                                        tipe="p")
       

        resp = self.client.get(reverse('profil_view'))

        self.assertContains(resp, "nama")
        self.assertContains(resp, "1234")
        self.assertContains(resp, "facebook")
        self.assertContains(resp, "coba@coba.com")
        self.assertContains(resp, "coba")
