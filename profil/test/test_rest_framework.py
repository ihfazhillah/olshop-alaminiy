from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from profil.models import Profil
from profil.serializers import ProfilSerializer

class ProfilDRFTest(APITestCase):
    def test_can_retrieve_first_object_and_return_200_status_code(self):
        Profil.objects.create(nama="nama",
                              tagline="tagline",
                              deskripsi="deskripsi")
        response = self.client.get(reverse('profil-api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfilSerializerClass(APITestCase):

    def test_can_serializer_the_input(self):
        profil = Profil(nama="nama", tagline="tagline", 
                                      deskripsi="deskripsi", alamat="alamat")
        serializer = ProfilSerializer(profil)
        expected = {'nama':'nama', 'tagline':'tagline', 'deskripsi':'deskripsi',
                    'alamat':'alamat'}
        self.assertEqual(dict(serializer.data), expected)