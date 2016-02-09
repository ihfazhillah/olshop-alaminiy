from rest_framework.test import APITestCase
from profil.serializers import ProfilSerializer
from profil.serializers import PhoneSerializer

def assert_serializer_with_missing_key(serializerclass, basedata, key):
    basedata.pop(key)
    serializer = serializerclass(data=basedata)
    assert serializer.is_valid() == False
    assert serializer.validated_data == {}
    assert dict(serializer.errors) == {key:['This field is required.']}

class PhoneSerializerTest(APITestCase):

    def setUp(self):
        self.valid_data = {'id':1, 'nomor':'1234', 'tipe':'p'}

    def test_with_valid_data(self):
        serializer = PhoneSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), self.valid_data)
        self.assertEqual(dict(serializer.errors), {})

    def test_with_missing_id(self):
        assert_serializer_with_missing_key(PhoneSerializer, self.valid_data, 'id')

    def test_with_missing_nomor(self):
        self.valid_data.pop('nomor')
        serializer = PhoneSerializer(data=self.valid_data)
        # print(serializer.is_valid())
        # self.assertFalse(serializer.is_valid())
        serializer.is_valid()
        print(serializer.validated_data)
        print(serializer.errors)

    

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
                          ]}

    def test_with_valid_data(self):
        serializer = ProfilSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data) , self.valid_data)

    def test_with_missing_phone(self):
        self.assert_with_missing_key('phone')

    def test_with_missing_nama(self):
        self.assert_with_missing_key('nama')

    def test_with_missing_tagline(self):
        self.assert_with_missing_key('tagline')

    def test_with_missing_deskripsi(self):
        self.assert_with_missing_key('deskripsi')

    def test_with_missing_alamat(self):
        self.assert_with_missing_key('alamat')

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
