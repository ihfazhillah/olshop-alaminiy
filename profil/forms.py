from django.forms import ModelForm, inlineformset_factory
from profil.models import Profil, Phone, Email, SocialMedia

class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        fields = ('nomor', 'tipe')

    def __init__(self, *args, **kwargs):
        self.profil = kwargs.pop('profil')
        super().__init__(*args, **kwargs)

    def save(self):
        phone = super().save(commit=False)
        phone.profil = self.profil
        phone.save()
        return phone

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ('alamat', 'tipe')

    def __init__(self, *args, **kwargs):
        self.profil = kwargs.pop("profil")
        super().__init__(*args, **kwargs)

    def save(self):
        email = super().save(commit=False)
        email.profil = self.profil
        email.save()
        return email

class SocialForm(ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['provider', 'url']

    def __init__(self, *args, **kwargs):
        self.profil = kwargs.pop('profil')
        super().__init__(*args, **kwargs)

    def save(self):
        social = super().save(commit=False)
        social.profil = self.profil
        social.save()
        return social

PhoneFormSet = inlineformset_factory(Profil, Phone, can_delete=False, fields='__all__',
                extra=1 )

class ProfilForm(ModelForm):
    class Meta:
        model = Profil
        exclude = ('slug',)

# class ProfilForm(forms.Form):
#     nama = forms.CharField(label="Nama", max_length=100)
#     tagline = forms.CharField(label="Tagline", max_length=250)
#     deskripsi = forms.CharField(label="Deskripsi", widget=forms.Textarea)
#     alamat = forms.CharField(label="Alamat", max_length=500)