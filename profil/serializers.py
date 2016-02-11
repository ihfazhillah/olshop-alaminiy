from rest_framework import serializers
from profil.models import Profil, Phone, Email, SocialMedia


class SocialSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialMedia
        exclude = ['profil']
        extra_kwargs = {'id':{'read_only':False},} 

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
    
    def processing_nested_data(self, model, validated_data, instance):
        for socialmedia in validated_data:
            socials = model.objects.all()
            socials_id = [s.id for s in socials]
            if socialmedia.get('id', '') not in socials_id:
                if not socialmedia.__contains__('provider') :
                    raise serializers.ValidationError("Provider field harus ada ketika membuat field baru.")
                elif not socialmedia.__contains__('url'):
                    raise serializers.ValidationError("Url field harus ada ketika membuat field baru.")    
                elif not socialmedia.__contains__('id'):
                    raise serializers.ValidationError('Tidak bisa menentukan "id" socialmedia yang akan diubah')
            social , created = model.objects.get_or_create(id = socialmedia.get('id'), profil=instance)
            social.provider = socialmedia.get('provider', social.provider)
            social.url = socialmedia.get('url', social.url)
            social.save()
    
    def update(self, instance, validated_data):
        phones_data = validated_data.pop('phone', [])
        email_data = validated_data.pop('email', [])
        socialmedia_data = validated_data.pop('socialmedia', [])

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
            email_query = Email.objects.all()
            emails_id = [x.id for x in email_query]
            if email.__contains__('id') and email.get('id') not in emails_id:
                if not email.__contains__('alamat'):
                    raise serializers.ValidationError('Alamat field harus ada ketika membuat field baru')
                if not email.__contains__('tipe'):
                    raise serializers.ValidationError('Tipe field harus ada ketika membuat field baru')
            elif not email.__contains__('id'):
                raise serializers.ValidationError("Tidak dapat menentukan 'id' yang akan diubah")
            e, c = Email.objects.get_or_create(id = email['id'], profil = instance)
            e.alamat = email.get('alamat', e.alamat)
            e.tipe = email.get('tipe', e.tipe)
            e.save()


        self.processing_nested_data(SocialMedia, socialmedia_data, instance)

        return instance