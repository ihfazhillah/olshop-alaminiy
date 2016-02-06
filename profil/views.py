from django.shortcuts import render,redirect
from profil.models import Profil
from profil.forms import ProfilForm, PhoneFormSet
# Create your views here.
def profil(request):
    profil = Profil.objects.first()
    return render(request, "profil/profil.html", {"profil":profil,
                  "profpage":True})

def profil_edit(request):
    profilfirst = Profil.objects.first()

    if request.method == 'POST':
        form = ProfilForm(request.POST)
        if form.is_valid():
            profil = form.save(commit=False)
            phone_formset = PhoneFormSet(request.POST, instance=profilfirst) 
            if phone_formset.is_valid():
                profil.save()
                phone_formset.save()
                return redirect('profil_view')
    else:
        form = ProfilForm(instance=profilfirst)
        phone_formset = PhoneFormSet(instance=profilfirst)
    context = {"form":form, 'phone':phone_formset}
    return render(request, "profil/profil_edit.html", context )        