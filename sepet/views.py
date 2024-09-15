from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import iyzipay
import json
from .forms import OdemeFormu
from .models import Urun


def sepet(request):
    if request.method == 'POST':
        form = OdemeFormu(request.POST)
        if form.is_valid():
            ad = form.cleaned_data['ad']  # Kullanıcının adı
            soyad = form.cleaned_data['soyad']  # Kullanıcının soyadı
            adres = form.cleaned_data['adres']  # Kullanıcının adresi
            sehir = form.cleaned_data['sehir']  # Kullanıcının yaşadığı şehir
            ulke = form.cleaned_data['ulke']  # Kullanıcının ülkesi
            posta_kodu = form.cleaned_data['posta_kodu']  # Posta kodu
            email = form.cleaned_data['email']  # Kullanıcının e-posta adresi
            telefon = form.cleaned_data['telefon']  # Kullanıcının telefon numarası

            # Aşağıdaki kart bilgileri opsiyonel çünkü İyzico iframe olarak bir ödeme formu sağlıyor
            #kart_sahibi_adi = form.cleaned_data.get('kart_sahibi_adi', '')  # Kart sahibi adı (opsiyonel)
            #kart_numarasi = form.cleaned_data.get('kart_numarasi', '')  # Kart numarası (opsiyonel)
            #son_kullanma_yili = form.cleaned_data.get('son_kullanma_yili', '')  # Son kullanma yılı (opsiyonel)
            #son_kullanma_ayi = form.cleaned_data.get('son_kullanma_ayi', '')  # Son kullanma ayı (opsiyonel)
            #cvc = form.cleaned_data.get('cvc', '')  # CVC güvenlik kodu (opsiyonel)

            # Sepetteki ürünleri çekiyoruz
            urunler = Urun.objects.all()
            toplam_fiyat = sum(urun.fiyat for urun in urunler)  # Toplam fiyat hesaplama

            # İyzico API ayarları
            options = {
                'api_key': settings.IYZI_API_KEY,  # İyzico API anahtarı
                'secret_key': settings.IYZI_SECRET_KEY,  # İyzico gizli anahtarı
                'base_url': settings.IYZI_BASE_URL  # İyzico API base URL
            }

            # Kart bilgileri, opsiyonel. Eğer iframe ile ödeme yapılacaksa bu bilgiler doldurulmak zorunda değil.
            payment_card = {
                'cardHolderName': 'kart_sahibi_adi',  # Kart sahibinin adı (eğer girildiyse)
                'cardNumber': 'kart_numarasi',  # Kart numarası (eğer girildiyse)
                'expireMonth': 'son_kullanma_ayi',  # Kartın son kullanma ayı (eğer girildiyse)
                'expireYear': 'son_kullanma_yili',  # Kartın son kullanma yılı (eğer girildiyse)
                'cvc': 'cvc',  # Kartın CVC kodu (eğer girildiyse)
                'registerCard': '0'  # Kartı kaydetme (0: Kaydetme, 1: Kaydet)
            }

            # Alıcı bilgileri
            buyer = {
                'id': 'BY789',  # Alıcının benzersiz ID'si
                'name': ad,  # Alıcının adı
                'surname': soyad,  # Alıcının soyadı
                'gsmNumber': telefon,  # Alıcının telefon numarası
                'email': email,  # Alıcının e-posta adresi
                'identityNumber': '74300864791',  # Alıcının T.C. kimlik numarası
                'lastLoginDate': '2015-10-05 12:43:35',  # Alıcının son giriş tarihi (örnek veri)
                'registrationDate': '2013-04-21 15:12:09',  # Alıcının kayıt tarihi (örnek veri)
                'registrationAddress': adres,  # Alıcının kayıtlı adresi
                'ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),  # Kullanıcının IP adresi
                'city': sehir,  # Kullanıcının şehri
                'country': ulke,  # Kullanıcının ülkesi
                'zipCode': posta_kodu  # Kullanıcının posta kodu
            }

            # Teslimat ve fatura adresi bilgileri
            address = {
                'contactName': f"{ad} {soyad}",  # İletişim adı
                'city': sehir,  # Şehir
                'country': ulke,  # Ülke
                'address': adres,  # Adres
                'zipCode': posta_kodu  # Posta kodu
            }

            # Sepetteki ürünleri sepet öğeleri listesine ekliyoruz
            basket_items = []
            for urun in urunler:
                item = {
                    'id': f'BI{urun.id}',  # Ürünün benzersiz ID'si
                    'name': urun.ad,  # Ürün adı
                    'category1': urun.kategori1,  # Ürün ana kategorisi
                    'category2': urun.kategori2,  # Ürün alt kategorisi
                    'itemType': 'PHYSICAL',  # Ürün türü (Fiziksel/Dijital)
                    'price': str(urun.fiyat)  # Ürün fiyatı
                }
                basket_items.append(item)

            # İyzico ödeme formu için istek verileri
            request_data = {
                'locale': 'tr',  # Dil seçimi
                'conversationId': '123456789',  # Sipariş ID'si (örnek veri)
                'price': str(toplam_fiyat),  # Sepet toplam fiyatı
                'paidPrice': str(toplam_fiyat),  # Ödenen toplam fiyat
                'currency': 'TRY',  # Para birimi (TRY: Türk Lirası)
                'basketId': 'B67832',  # Sepet ID'si (örnek veri)
                'paymentGroup': 'PRODUCT',  # Ödeme grubu (ÜRÜN)
                'paymentCard': payment_card,  # Kart bilgileri (opsiyonel, iframe ile doldurulacaksa boş kalabilir)
                'buyer': buyer,  # Alıcı bilgileri
                'shippingAddress': address,  # Teslimat adresi
                'billingAddress': address,  # Fatura adresi
                'basketItems': basket_items,  # Sepet öğeleri
                'callbackUrl': "http://localhost:8000/result/",  # Ödeme sonrası yönlendirilecek URL
                "enabledInstallments": ['2', '3', '6', '9']  # Taksit seçenekleri (Opsiyonel)
            }

            # İyzico ödeme formu başlatma
            checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request_data, options)

            # API'den dönen yanıtı okuyoruz
            content = checkout_form_initialize.read().decode('utf-8')
            json_content = json.loads(content)

            # Eğer ödeme formu başarıyla oluşturulduysa, formu HTML olarak döndür
            if 'checkoutFormContent' in json_content:
                return render(request, 'sepet.html', {'iframe_content': json_content["checkoutFormContent"]})
            else:
                # Eğer hata varsa, hata mesajını JSON olarak döndür
                return JsonResponse({
                    'error_code': json_content.get('errorCode', 'Bilinmeyen Hata'),  # Hata kodu
                    'error_message': json_content.get('errorMessage', 'Hata mesajı belirtilmedi')  # Hata mesajı
                }, status=400)
    else:
        form = OdemeFormu()  # Formu boş olarak yüklüyoruz

    # Sepetteki ürünleri ve toplam fiyatı template'e gönderiyoruz
    urunler = Urun.objects.all()
    toplam_fiyat = sum(urun.fiyat for urun in urunler)
    return render(request, 'sepet.html', {'form': form, 'urunler': urunler, 'toplam_fiyat': toplam_fiyat})


# Ödeme işlemi tamamlandığında çağrılacak sonuç sayfası
def result(request):
    return render(request, 'result.html')
