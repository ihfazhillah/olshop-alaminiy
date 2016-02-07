from rest_framework import serializers
from profil.models import Profil, Phone

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('nomor','tipe')


class ProfilSerializer(serializers.ModelSerializer):
    phone_set = PhoneSerializer(many=True)

    class Meta:
        model = Profil
        exclude = ( 'slug','id')
        # fields = ("nama", "tagline", "deskripsi","alamat", "phone_set")
    
    # def create(self, validated_data):
    #     phones_data = validated_data.pop('phone_set')
    #     print(validated_data)
    def update(self, instance, validated_data):
        print(validated_data)
        phones_data = validated_data.pop('phone_set')
        profil = Profil(**validated_data)
        profil.save()
        for phone_data in phones_data:
            phone = Phone(**phone_data)
            phone.save()
        return profil