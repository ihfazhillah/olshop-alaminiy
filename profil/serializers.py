from rest_framework import serializers
from profil.models import Profil, Phone

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'nomor','tipe')
        # extra_kwargs = {'id':
        # { 'read_only':False}}

    # def to_representation(self, value):
    #     return {'id':value.id,
    #             'nomor':value.nomor,
    #             'tipe':value.tipe}


class ProfilSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer(many=True,)

    class Meta:
        model = Profil
        # exclude = ( 'slug',)
        fields = ("nama", "tagline", "deskripsi","alamat", "phone")
    
    # def create(self, validated_data):
    #     phones_data = validated_data.pop('phone_set')
    #     print(validated_data)
    def update(self, instance, validated_data):
        # print(validated_data)
        print(validated_data)
        print(instance)
        phones_data = validated_data.pop('phone')
        print(phones_data)
        phone = instance.phone
        instance.nama = validated_data['nama']
        instance.tagline = validated_data['tagline']
        instance.deskripsi = validated_data['deskripsi']
        instance.alamat = validated_data['alamat']
        for phone_data in phones_data:
            phone_object = Phone(profil=instance, **phone_data)
            phone_object.save()
        instance.save()
        return instance



# {'id': 1, 'phone': [{'id': 1, 'tipe': 'p', 'nomor': '12345'}, {'id': 2, 'tipe': 's', 'nomor': '455666'}], 'nama': 'namaaaaa', 'tagline': 'tegiiiiin', 'deskripsi': 'deskripsiii'}
