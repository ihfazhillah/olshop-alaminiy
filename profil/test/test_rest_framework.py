from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from profil.models import Profil, Phone, Email
from profil.serializers import ProfilSerializer
from django.contrib.auth.models import User

class APIViewTest(APITestCase):

    def setUp(self):
        #> Making a super user
        User.objects.create_superuser(username='sakkuun', password='sakkuun1234',
                                      email='sakkuun@ni.aja')
        #> Making an initial data
        self.profil = Profil.objects.create(nama='fake',
                              tagline='a fake person',
                              deskripsi = 'a fake descriptions',
                              alamat = 'a fake address')

    def test_retrieving_first_object(self):
        expected = {'id':1,
        'nama':'fake',
        'tagline':'a fake person',
        'deskripsi':'a fake descriptions',
        'alamat':'a fake address',
        'phone':[],
        'email':[],
        'socialmedia':[]}
        response = self.client.get(reverse('profil-api'))
        self.assertEqual(response.data, expected)

    def test_putting_phone_data(self):
        data = {'phone':[{'id':1,'nomor':'12345', 'tipe':'p'}]}
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('phone'), data['phone'])

    def test_edit_phone_data_already_exist_and_add_one(self):
        Phone.objects.create(profil=self.profil, nomor='23456', tipe='p')
        data = {'phone':[{'id':1, 'nomor':'44444', 'tipe':'s'},
                          {'id':2, 'nomor':'12345', 'tipe':'p'}]}
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('phone'), data.get('phone'))

    def test_edit_phone_with_empty_list(self):
        Phone.objects.create(profil=self.profil, nomor='12345', tipe='p')
        data = {'phone':[]}
        expected = {'phone':[{'id':'1', 'nomor':'12345', 'tipe':'p'}]}
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        print(response.data)
        self.assertIn(expected.get('phone'), response.data)


