from rest_framework import serializers
from profil.models import Profil, Phone, Email, SocialMedia

class SocialSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialMedia
        exclude = ['profil']
        extra_kwargs = {'id':{'read_only':False},
                        }

   


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        exclude = ('profil',)
        extra_kwargs = {'id':{'read_only':False},
                        }

class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        exclude = ('profil',)
        extra_kwargs = {
        'id':{'read_only':False}
        }

class ProfilSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer(many=True, required=False)
    email = EmailSerializer(many=True, required=False)
    socialmedia = SocialSerializer(many=True, required=False)

    class Meta:
        model = Profil
        
        fields = ("id", "nama", "tagline", "deskripsi","alamat",
         "phone", "email", 'socialmedia')
    
    
    def update(self, instance, validated_data):
        phones_data = validated_data.pop('phone')
        email_data = validated_data.pop('email')

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

        for email in email_data:
            e, c = Email.objects.get_or_create(id = email['id'], profil = instance)
            e.alamat = email['alamat']
            e.tipe = email['tipe']
            e.save()

        return instance