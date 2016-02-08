from rest_framework import serializers
from profil.models import Profil, Phone

class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = ('id', 'nomor', 'tipe')
        extra_kwargs = {
        'id':{'read_only':False}
        }

class ProfilSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer(many=True)

    class Meta:
        model = Profil
        
        fields = ("id", "nama", "tagline", "deskripsi","alamat", "phone")
    
    
    def update(self, instance, validated_data):
        print(validated_data)
        phones_data = validated_data.pop('phone')
        instance.nama = validated_data.get('nama', instance.nama)
        instance.tagline = validated_data.get('tagline', instance.tagline)
        instance.deskripsi = validated_data.get('deskripsi', instance.deskripsi)
        instance.alamat = validated_data.get('alamat', instance.alamat)

        for phone_data in phones_data:
            phone, created = Phone.objects.get_or_create(id = phone_data['id'],
                                                         profil= instance)
            phone.nomor = phone_data.get('nomor', phone.nomor)
            phone.tipe = phone_data.get('tipe', phone.tipe)
            phone.save()
        instance.save()
        return instance