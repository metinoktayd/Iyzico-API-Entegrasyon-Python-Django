from django.shortcuts import render

# Create your views here.

def siparis_onay(request):
    return render(request, 'index.html')
