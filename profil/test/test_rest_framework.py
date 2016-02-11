from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from profil.models import Profil, Phone, Email, SocialMedia
from profil.serializers import ProfilSerializer
from django.contrib.auth.models import User

class APIViewTest(APITestCase):
    def login_as_sakkuun(self):
        self.client.login(username='sakkuun',password='sakkuun1234')

    def assert_add_field_with_missing_key(self, field, msg, args):
        data = { field : args}
        expected = [msg]
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected)

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

    def test_adding_email_with_missing_id(self):
        self.assert_add_field_with_missing_key('email',
                                               "Tidak dapat menentukan 'id' yang akan diubah",
                                               [{'alamat':'dia@email.aku', 'tipe':'p'}])
        

    def test_adding_email_with_missing_alamat(self):
        self.assert_add_field_with_missing_key('email',
                                               'Alamat field harus ada ketika membuat field baru',
                                               [{'id':1, 'tipe':'p'}])

    def test_adding_email_with_missing_tipe(self):
        self.assert_add_field_with_missing_key('email',
                                               'Tipe field harus ada ketika membuat field baru',
                                               [{'id':1, 'alamat':'dia@email.aku'}])

    def test_adding_two_email_with_invalid_one(self):
        data = {'email':[{'id':1, 'alamat': 'email@ku.loh', 'tipe':'p'},
                        {'id':2, 'tipe':'s'}]}
        expected = ['Alamat field harus ada ketika membuat field baru']
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected)

    def test_editting_email(self):
        Email.objects.create(profil=self.profil, alamat='email@ku.loh', tipe='p')
        data = {'email':[{'id':1, 'alamat':'email@mu.loh'}]}
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_editing_email_with_invalid_id(self):
        Email.objects.create(profil=self.profil, alamat='email@ku.loh', tipe='p')
        data = {'email':[{'alamat':'email@mu.it', 'tipe':'s'}]}
        expected = ["Tidak dapat menentukan 'id' yang akan diubah"]
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected)

    def test_editing_email_with_add_valid(self):
        Email.objects.create(profil=self.profil, alamat='email@ku.loh', tipe='p')
        data = {'email':[{'id':1, 'alamat':'email@mu.ini'},
                        {'id':4, 'alamat':'email@email.email', 'tipe':'s'}]}
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)


    #--------------
    # Testing social media field
    #--------------

    def test_adding_social_media(self):
        data = {'socialmedia':[{'id':1, 'provider':'fake', 'url':'http://fake.url'}]}
        expected = {'id':1,
        'nama': 'fake',
        'tagline':'a fake person',
        'deskripsi':'a fake descriptions',
        'alamat':'a fake address',
        'phone':[],
        'email':[],
        'socialmedia':[{'id':1, 'provider':'fake', 'url':'http://fake.url'}]}
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected)

    def test_adding_social_media_with_missing_provider(self):
        self.assert_add_field_with_missing_key('socialmedia',
                                               'Provider field harus ada ketika membuat field baru.',
                                               [{'id':1, 'url':'http://fake.url'}])

    def test_adding_social_media_with_missing_url(self):
        self.assert_add_field_with_missing_key('socialmedia',
                                               'Url field harus ada ketika membuat field baru.',
                                               [{'id':1, 'provider':'fake'}])

    def test_adding_social_media_with_missing_id(self):
        self.assert_add_field_with_missing_key('socialmedia',
                                               'Tidak bisa menentukan "id" socialmedia yang akan diubah',
                                               [{'url':'http://url.ku', 'provider':'fake'}])

    def test_editing_social_media_with_missing_id(self):
        SocialMedia.objects.create(profil=self.profil, provider='fakeprovider', url='http://fakeprovider.net')
        data = {'socialmedia':[{'url':'http://my.url', 'provider':'fake'}]}
        expected = ['Tidak bisa menentukan "id" socialmedia yang akan diubah']
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected)

    def test_editing_social_media_with_missing_provider_return_201(self):
        SocialMedia.objects.create(profil=self.profil, provider='fakeprovider', url='http://fakeprovider.net')
        data = {'socialmedia':[{'id':1, 'provider':'fake'}]}
        # expected = ['Tidak bisa menentukan "id" socialmedia yang akan diubah']
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.data, expected)

    def test_editing_social_media_with_missing_id_in_second(self):
        SocialMedia.objects.create(profil=self.profil, provider='fakeprovider', url='http://fakeprovider.net')
        data = {'socialmedia':[{'id':1,'url':'http://my.url', 'provider':'fake'},
                                {'url':'http://urlk.uu', 'provider':'pass'}]}
        expected = ['Tidak bisa menentukan "id" socialmedia yang akan diubah']
        self.login_as_sakkuun()
        response = self.client.put(reverse('profil-api'), data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected)





