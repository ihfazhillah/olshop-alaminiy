from django.forms import ModelForm, inlineformset_factory
from profil.models import Profil, Phone

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