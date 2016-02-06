from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from profil.models import Profil

class ProfilDRFTest(APITestCase):
    def test_can_retrieve_first_object_of_profil(self):
        Profil.objects.create(nama="nama",
                              tagline="tagline",
                              deskripsi="deskripsi")
        response = self.client.get(reverse('profil-api'))
        self.assertEqual(response.status_code, 200)