from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from profil.models import Profil
from profil.forms import ProfilForm, PhoneFormSet
from profil.serializers import  ProfilSerializer
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

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def profil_api(request):
    profil = Profil.objects.first()
    if request.method == "GET":
        serializer = ProfilSerializer(profil)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProfilSerializer(instance=profil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)