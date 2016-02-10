from rest_framework.test import APITestCase
from profil.serializers import ProfilSerializer
from profil.serializers import PhoneSerializer
from profil.serializers import EmailSerializer
from profil.serializers import SocialSerializer



class PhoneSerializerTest(APITestCase):

    def setUp(self):
        self.valid_data = {'id':1, 'nomor':'1234', 'tipe':'p'}

    def test_with_valid_data(self):
        serializer = PhoneSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), self.valid_data)
        self.assertEqual(dict(serializer.errors), {})

    def test_with_missing_id(self):
        self.valid_data.pop('id')
        serializer = PhoneSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())

    def test_with_missing_nomor(self):
        self.valid_data.pop('nomor')
        serializer = PhoneSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())

    def test_with_missing_tipe(self):
        self.valid_data.pop('tipe')
        serializer = PhoneSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
    
class EmailSerializerTest(APITestCase):

    def test_with_valid_data(self):
        data = {'id':1, 'alamat':'email@email.com', 'tipe':'p'}
        serializer = EmailSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), data)
        self.assertEqual(dict(serializer.errors), {})

    def test_with_missing_alamat(self):
        data = {'id':1, 'tipe':'p'}
        serializer = EmailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(dict(serializer.errors), {'alamat':['This field is required.']})

    def test_with_missing_tipe(self):
        data = {'id':1, 'alamat':'alamat@email.ku'}
        serializer = EmailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(dict(serializer.errors), {'tipe' : ['This field is required.']})

class SocialSerializerTest(APITestCase):
    def test_with_valid_data(self):
        data = {'id':1, 'provider':'facebook', 'url':'http://facebook.com'}
        serializer = SocialSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), data)

    def test_with_missing_id(self):
        data = {'provider':'facebook', 'url':'http://facebook.com'}
        serializer = SocialSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_with_missing_provider(self):
        data = {'id':1, 'url':'http://facebook.com'}
        serializer = SocialSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_with_missing_url(self):
        data = {'id':1, 'provider':'facebook'}
        serializer = SocialSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class ProfilSerializerClass(APITestCase):

    def assert_with_missing_key(self, key):
        data = self.valid_data
        data.pop(key)
        serializer = ProfilSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.errors, {key:['This field is required.']})

    def setUp(self):
        self.valid_data = {'nama':'nama', 'tagline':'tagline', 
                           'deskripsi':'deskripsi','alamat':'alamat',
                           'phone':[
                           {'id':1, 'nomor':'123456', 'tipe':'p'},
                          ],
                          'email':[{'id':1,'alamat':'email@ku.it', 'tipe':'p'}],
                          'socialmedia':[]}

    def test_with_valid_data(self):
        serializer = ProfilSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data) , self.valid_data)

    def test_with_missing_nama(self):
        self.assert_with_missing_key('nama')

    def test_with_missing_tagline(self):
        self.assert_with_missing_key('tagline')

    def test_with_missing_deskripsi(self):
        self.assert_with_missing_key('deskripsi')

    def test_with_missing_alamat(self):
        self.assert_with_missing_key('alamat')

    def test_with_missing_phone(self):
        self.valid_data.pop('phone')
        serializer = ProfilSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), self.valid_data)


    def test_with_missing_email(self):
        self.valid_data.pop('email')
        serializer = ProfilSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), self.valid_data)

    def test_with_missing_socialmedia(self):
        self.valid_data.pop('socialmedia')
        serializer = ProfilSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), self.valid_data)

    def test_with_partial_update(self):
        self.valid_data.pop('deskripsi')
        serializer = ProfilSerializer(data=self.valid_data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), self.valid_data)
        self.assertEqual(dict(serializer.errors), {})

    def test_phone_data_type_is_list(self):
        serializer = ProfilSerializer(self.valid_data)
        phone_data = dict(serializer.data).pop('phone')
        self.assertTrue(isinstance(phone_data, list))

    def test_email_data_type_is_list(self):
        serializer = ProfilSerializer(self.valid_data)
        email_data = dict(serializer.data).pop('email')
        self.assertTrue(isinstance(email_data, list))
