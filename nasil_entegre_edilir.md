# IYZICO ENTEGRASYONU

## PYTHON DJANGO

### Adımlar

1. **Iyzico Üyeliği Oluşturun**
   - [Iyzico](https://www.iyzico.com/isim-icin/hesap-olustur) veya [Iyzico Sandbox](https://sandbox-merchant.iyzipay.com/auth/register) (Iyzico'nun bir test ortamıdır) üzerinden üyelik oluşturun.

2. **Projenize Iyzico'yu Yükleyin**
   - **Mac**: `pip3 install iyzipay`
   - **Windows**: `pip install iyzipay`

3. **Projenize Iyzico'yu Import Edin**
   - `import iyzipay`

3. **API Anahtarı ve Güvenlik Anahtarını Kopyalayıp settings.py Kodlarınıza Entegre Edin**

4. **Entegrasyon Aşaması Kodlarda Mevcut (sepet/views.py, magaza/settings.py, template/sepet.html)**
### JSON Yapısı

Aşağıdaki JSON yapısı, Iyzico API yanıtını gösterir:

```json
    buyer={
        'id': 'BY789',  // Alıcının benzersiz kimlik numarası.
        'name': 'John',  // Alıcının adı.
        'surname': 'Doe',  // Alıcının soyadı.
        'gsmNumber': '+905350000000',  // Alıcının GSM numarası (telefon numarası).
        'email': 'email@email.com',  // Alıcının e-posta adresi.
        'identityNumber': '74300864791',  // Alıcının kimlik numarası (TC kimlik numarası gibi).
        'lastLoginDate': '2015-10-05 12:43:35',  // Alıcının son giriş tarihi ve saati.
        'registrationDate': '2013-04-21 15:12:09',  // Alıcının kayıt tarihi ve saati.
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',  // Alıcının kayıtlı adresi.
        'ip': '85.34.78.112',  // Alıcının IP adresi.
        'city': 'Istanbul',  // Alıcının yaşadığı şehir.
        'country': 'Turkey',  // Alıcının yaşadığı ülke.
        'zipCode': '34732'  // Alıcının posta kodu.
    }

    address={
        'contactName': 'Jane Doe',  // Teslimat adresindeki kişinin adı.
        'city': 'Istanbul',  // Teslimat adresinin şehir bilgisi.
        'country': 'Turkey',  // Teslimat adresinin ülke bilgisi.
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',  // Teslimat adresi.
        'zipCode': '34732'  // Teslimat adresinin posta kodu.
    }

    basket_items=[ //Birden fazla ürün varsa for ile döndürülmesi lazım (sepet/views.py kodlarında mevcut)
        {
            'id': 'BI101',  // Ürünün benzersiz kimlik numarası.
            'name': 'Binocular',  // Ürünün adı.
            'category1': 'Collectibles',  // Ürünün birincil kategorisi.
            'category2': 'Accessories',  // Ürünün ikincil kategorisi.
            'itemType': 'PHYSICAL',  // Ürün tipi: fiziksel ya da sanal.
            'price': '0.3'  // Ürünün fiyatı (kuruş cinsinden).
        },
    ]

    request={
        'locale': 'tr',  // Talebin dili: Türkçe.
        'conversationId': '123456789',  // Talebin benzersiz kimlik numarası (konuşma ID'si).
        'price': '1',  // Toplam ürün fiyatı (kuruş cinsinden).
        'paidPrice': '1.2',  // Ödenecek toplam fiyat (kuruş cinsinden).
        'currency': 'TRY',  // Para birimi: Türk Lirası (TRY).
        'basketId': 'B67832',  // Sepet kimlik numarası.
        'paymentGroup': 'PRODUCT',  // Ödeme grubu: Ürün ödemesi.
        "callbackUrl": "http://localhost:8008/result/",  // Ödeme tamamlandığında Iyzico'nun çağıracağı URL.
        "enabledInstallments": ['2', '3', '6', '9'],  // Desteklenen taksit seçenekleri.
        'buyer': buyer,  // Alıcı bilgileri (önceden tanımlanan 'buyer' nesnesi).
        'shippingAddress': address,  // Teslimat adresi (önceden tanımlanan 'address' nesnesi).
        'billingAddress': address,  // Fatura adresi (önceden tanımlanan 'address' nesnesi).
        'basketItems': basket_items,  // Sepet ürünleri (önceden tanımlanan 'basket_items' listesi).
        # 'debitCardAllowed': True  // Kredi kartı kullanımına izin verilip verilmeyeceği. (Bu örnekte yorum satırı olarak bırakılmış.)
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)
    // Iyzico'nun CheckoutFormInitialize sınıfının 'create' metodunu kullanarak bir ödeme formu başlatılıyor. 'request' ve 'options' parametreleri ile birlikte.

