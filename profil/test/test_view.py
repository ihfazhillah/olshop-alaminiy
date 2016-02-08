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
        profil.socialmedia.create(provider="facebook",
                                      url="http://facebook.com")
        profil.phone.create(nomor='12345',
                                tipe="p")

        profil.email.create(alamat="coba@coba.com",
                                        tipe="p")
       

        resp = self.client.get(reverse('profil_view'))

        # print(resp.content)
        self.assertContains(resp, "nama")
        self.assertContains(resp, '12345')
        self.assertContains(resp, "facebook")
        self.assertContains(resp, "coba@coba.com")
        self.assertContains(resp, "coba")
