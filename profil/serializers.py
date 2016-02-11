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
    
    def validating_nested_data_and_save(self, model, validated_data, instance, kwargs={}):
        """
        model : used for query set
        validated_data : used for validated_data stored after .is_valid() called
        instance : for profil 
        kwargs : keyword argument for {field : error}
        """
        for data in validated_data:
            query = model.objects.all()
            objects_id = [s.id for s in query]
            if not data.__contains__('id'):
                raise serializers.ValidationError(kwargs.get('id'))
                
            elif data.__contains__('id') and data.get('id') not in objects_id:
                for key in kwargs.keys():
                    if not data.__contains__(key):
                        raise serializers.ValidationError(kwargs.get(key))
            object , created = model.objects.get_or_create(id = data.get('id'), profil=instance)
            data_dict =object.__dict__
            for key in data.keys():
                if key is not 'id':
                    setattr(object, key, data.get(key, data_dict.get(key)))
            object.save()
    
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

        email_errors = {'id':"Tidak dapat menentukan 'id' yang akan diubah",
                        'alamat':'Alamat field harus ada ketika membuat field baru',
                        'tipe':'Tipe field harus ada ketika membuat field baru'}
        self.validating_nested_data_and_save(Email, email_data, instance, email_errors)
        

        social_errors = {'id':'Tidak bisa menentukan "id" socialmedia yang akan diubah',
                         'provider':"Provider field harus ada ketika membuat field baru.",
                         'url':"Url field harus ada ketika membuat field baru."}
        self.validating_nested_data_and_save(SocialMedia, socialmedia_data, instance, social_errors)

        return instance