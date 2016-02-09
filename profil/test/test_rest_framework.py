from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from profil.models import Profil, Phone, Email
from profil.serializers import ProfilSerializer
from django.contrib.auth.models import User

class ProfilDRFTest(APITestCase):
    def setUp(self):
        profil = Profil.objects.create(nama="nama",
                              tagline="tagline",
                              deskripsi="deskripsi",
                              alamat="alamat")
        Phone.objects.create(profil=profil, nomor='9087', tipe='p')
        Email.objects.create(profil=profil, alamat='email@ku.com', tipe='p')
        User.objects.create_superuser(username='sakkuun', password='sakkuun1234',
                                      email='')
        self.data_without_phone = {'nama':'nama','id':1,
                                    'alamat':'alamat', 'deskripsi':'deskripsi',
                                    'tagline':'tagline'}

    def test_can_retrieve_first_object_and_return_200_status_code(self):
        response = self.client.get(reverse('profil-api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_retrieve_first_object_as_expected(self):
        expected = {'id':1,'nama':'nama', 'tagline':'tagline', 'deskripsi':'deskripsi',
        'alamat':'alamat',
        'phone':[{
        'id':1, 'nomor':'9087', 'tipe':'p'}],
        'email': [{'id': 1,'alamat': 'email@ku.com','tipe': 'p'}]}
        response = self.client.get(reverse('profil-api'))
        # print(dict(response.data))
        self.assertEqual(dict(response.data), expected)

    def test_cant_create_new_profil_with_login(self):
        self.client.login(username='sakkuun', password='sakkuun1234')
        response = self.client.post(reverse('profil-api'), self.data_without_phone)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cant_create_new_profil_without_login_and_return_404_forbiden(self):
        response = self.client.post(reverse('profil-api'), self.data_without_phone)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_cant_edit_profil_if_not_user(self):
        response = self.client.put(reverse('profil-api'), self.data_without_phone)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_put_wrong_data_it_return_bad_request_status(self):
        self.client.login(username='sakkuun', password='sakkuun1234')
        response = self.client.put(reverse('profil-api'), {'nama':'nama'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_profil_with_number_phone(self):
        
        self.client.login(username='sakkuun', password='sakkuun1234')
        data = {'nama':'nama','id':1,
                    'alamat':'alamat', 'deskripsi':'deskripsi',
                    'tagline':'tagline',
                    'phone':[
                    {'id':1, 'nomor':'1234', 'tipe':'s'},
                     {'id':3, 'nomor':'1234', 'tipe':'s'}
                    ],
                    'email': [{'id': 1,'alamat': 'email@ku.com','tipe': 'p'}]
                    }
        
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(dict(response.data), data)

