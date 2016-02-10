from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from profil.models import Profil, Phone, Email
from profil.serializers import ProfilSerializer
from django.contrib.auth.models import User

class APIViewTest(APITestCase):
    def login_as_sakkuun(self):
        self.client.login(username='sakkuun',password='sakkuun1234')

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
    
    #-----------
    # Authenticating Test...
    #-----------

    def test_read_only_for_non_user(self):
        data = {'nama':'name'}
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_editing_nama_field_with_logged_user(self):
        self.login_as_sakkuun()
        data = {'nama':'aku ihfazh'}
        expected = {'id':1,
        'nama': 'aku ihfazh',
        'tagline':'a fake person',
        'deskripsi':'a fake descriptions',
        'alamat':'a fake address',
        'phone':[],
        'email':[],
        'socialmedia':[]}
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected)

    #------------
    # Testing phone field
    #------------

    def test_putting_phone_data(self):
        self.login_as_sakkuun()
        data = {'phone':[{'id':1,'nomor':'12345', 'tipe':'p'}]}
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('phone'), data['phone'])

    def test_edit_phone_data_already_exist_and_add_one(self):
        self.login_as_sakkuun()
        Phone.objects.create(profil=self.profil, nomor='23456', tipe='p')
        data = {'phone':[{'id':1, 'nomor':'44444', 'tipe':'s'},
                          {'id':2, 'nomor':'12345', 'tipe':'p'}]}
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('phone'), data.get('phone'))

    def test_edit_phone_with_empty_list(self):
        self.login_as_sakkuun()
        Phone.objects.create(profil=self.profil, nomor='12345', tipe='p')
        data = {'phone':[]}
        expected = {'id':1,
        'nama':'fake',
        'tagline':'a fake person',
        'deskripsi':'a fake descriptions',
        'alamat':'a fake address',
        'phone':[{'id':1,'nomor':'12345','tipe':'p'}],
        'email':[],
        'socialmedia':[]}
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected)

    #--------
    # Testing email field
    #--------

    def test_adding_email_field(self):
        data = {'email':[{'id':1, 'alamat':'email@ku.ini', 'tipe':'p'}]}
        expected = {'id':1,
        'nama':'fake',
        'tagline':'a fake person',
        'deskripsi':'a fake descriptions',
        'alamat':'a fake address',
        'phone':[],
        'email':[{'id':1, 'alamat':'email@ku.ini', 'tipe':'p'}],
        'socialmedia':[]}
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected)

    def test_editing_existing_email(self):
        Email.objects.create(profil=self.profil, alamat='email@ku.ini', tipe='p')
        Email.objects.create(profil=self.profil, alamat='email@mu.ini', tipe='s')
        data = {'email':[{'alamat':'email@dia.ini', 'id':2},
                          {'tipe':'s', 'id':1}]}
        expected = {'id':1,
        'nama':'fake',
        'tagline':'a fake person',
        'deskripsi':'a fake descriptions',
        'alamat':'a fake address',
        'phone':[],
        'email':[{'id':1, 'alamat':'email@ku.ini', 'tipe':'s'},
                  {'id':2, 'alamat':'email@dia.ini', 'tipe':'s'}],
        'socialmedia':[]}
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected)



