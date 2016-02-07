from rest_framework import serializers
from profil.models import Profil, Phone

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('nomor','tipe')


class ProfilSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer(many=True,  source='phone_set')

    class Meta:
        model = Profil
        fields = ("nama", "tagline", "deskripsi","alamat", "phone")