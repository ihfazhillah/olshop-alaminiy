from rest_framework import serializers
from profil.models import Profil


class ProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profil
        fields = ("nama", "tagline", "deskripsi","alamat")