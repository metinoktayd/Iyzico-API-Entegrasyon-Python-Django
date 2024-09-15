# sepet/forms.py

from django import forms


class OdemeFormu(forms.Form):
    ad = forms.CharField(max_length=100, label='Ad')
    soyad = forms.CharField(max_length=100, label='Soyad')
    adres = forms.CharField(widget=forms.Textarea, label='Adres')
    ulke = forms.CharField(max_length=100, label='Ülke')
    sehir = forms.CharField(max_length=100, label='Şehir')
    ilce = forms.CharField(max_length=100, label='İlçe')
    posta_kodu = forms.CharField(max_length=10, label='Posta Kodu')
    email = forms.EmailField(label='E-posta')
    telefon = forms.CharField(max_length=20, label='Telefon Numarası')

    #kart_sahibi_adi = forms.CharField(max_length=100, label='Kart Sahibi Adı')
    #kart_numarasi = forms.CharField(max_length=16, label='Kart Numarası')
    #son_kullanma_yili = forms.CharField(max_length=4, label='Son Kullanma Yılı')
    #son_kullanma_ayi = forms.CharField(max_length=2, label='Son Kullanma Ayı')
    #cvc = forms.CharField(max_length=3, label='CVC')
    #karti_kaydet = forms.BooleanField(required=False, label='Kartı Kaydet')
