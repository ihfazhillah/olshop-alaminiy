from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from profil.models import Profil
from profil.serializers import ProfilSerializer
from django.contrib.auth.models import User

class ProfilDRFTest(APITestCase):
    def setUp(self):
        Profil.objects.create(nama="nama",
                              tagline="tagline",
                              deskripsi="deskripsi",
                              alamat="alamat")
        User.objects.create_superuser(username='sakkuun', password='sakkuun1234',
                                      email='')
    def test_can_retrieve_first_object_and_return_200_status_code(self):
        response = self.client.get(reverse('profil-api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_retrieve_first_object_as_expected(self):
        expected = {'nama':'nama', 'tagline':'tagline', 'deskripsi':'deskripsi',
        'alamat':'alamat'}
        response = self.client.get(reverse('profil-api'))
        self.assertEqual(dict(response.data), expected)

    def test_cant_create_new_profil_with_login(self):
        self.client.login(username='sakkuun', password='sakkuun1234')
        response = self.client.post(reverse('profil-api'), {'nama':'nama',
                                    'alamat':'alamat', 'deskripsi':'deskripsi',
                                    'tagline':'tagline'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cant_create_new_profil_without_login_and_return_404_forbiden(self):
        response = self.client.post(reverse('profil-api'), {'nama':'nama',
                                    'alamat':'alamat', 'deskripsi':'deskripsi',
                                    'tagline':'tagline'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_cant_edit_profil_if_not_user(self):
        response = self.client.put(reverse('profil-api'), {'nama':'nama',
                                    'alamat':'alamat', 'deskripsi':'deskripsi',
                                    'tagline':'tagline'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_put_wrong_data_it_return_bad_request_status(self):
        self.client.login(username='sakkuun', password='sakkuun1234')
        response = self.client.put(reverse('profil-api'), {'nama':'nama'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProfilSerializerClass(APITestCase):

    def test_can_serializer_the_input(self):
        profil = Profil(nama="nama", tagline="tagline", 
                                      deskripsi="deskripsi", alamat="alamat")
        serializer = ProfilSerializer(profil)
        expected = {'nama':'nama', 'tagline':'tagline', 'deskripsi':'deskripsi',
                    'alamat':'alamat'}
        self.assertEqual(dict(serializer.data), expected)