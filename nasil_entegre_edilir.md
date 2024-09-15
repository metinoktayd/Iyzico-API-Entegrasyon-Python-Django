# IYZICO ENTEGRASYONU

## PYTHON DJANGO

### Adımlar

1. **Iyzico Üyeliği Oluşturun**
   - [Iyzico](https://www.iyzico.com/isim-icin/hesap-olustur) veya [Iyzico Sandbox](https://sandbox-merchant.iyzipay.com/auth/register) (Iyzico'nun bir test ortamıdır) üzerinden üyelik oluşturun.

2. **Projenize Iyzico'yu Yükleyin**
   - **Mac**: `pip3 install iyzipay`
   - **Windows**: `pip install iyzipay`

3. **API Anahtarı ve Güvenlik Anahtarını Kopyalayıp Kodlarınıza Entegre Edin**

### JSON Yapısı

Aşağıdaki JSON yapısı, Iyzico API yanıtını gösterir:

```json
{
   "locale": "tr",  // Dil ayarı. Bu, API'nin yanıtının hangi dilde döneceğini belirtir. "tr" Türkçe anlamına gelir.
   "conversationId": "deviyzico",  // İşlem için benzersiz bir kimlik. Bu ID, bir işlemle ilgili tüm verileri takip etmek için kullanılır.
   "price": "10.01",  // Ödenecek toplam tutar. Bu, kullanıcı tarafından ödenmesi gereken miktarı temsil eder.
   "paidPrice": "10.01",  // Kullanıcının ödediği toplam tutar. Genellikle bu, 'price' ile aynı değerdir.
   "currency": "TRY",  // Para birimi. Ödemede kullanılan para birimini belirtir; burada "TRY" Türk Lirası anlamına gelir.
   "installment": 1,  // Taksit sayısı. Bu, ödemenin kaç taksitte yapılacağını belirtir. Örneğin, "1" tek seferde ödeme anlamına gelir.
   "paymentChannel": "WEB",  // Ödeme kanalı. Burada "WEB", ödemelerin web üzerinden yapıldığını belirtir. Diğer olası değerler arasında mobil, POS vb. olabilir.
   "basketId": "B67832",  // Sepet kimliği. Bu, ödeme yapılan sepetin benzersiz tanımlayıcısıdır ve genellikle sepetin veritabanındaki ID'sini ifade eder.
   "paymentGroup": "PRODUCT",  // Ödeme grubu. Bu, ödemenin hangi türde olduğunu belirtir; "PRODUCT" ürün ödemesi anlamına gelir. Diğer gruplar servis ödemeleri vs. olabilir.
   "paymentCard": {  // Ödeme kartı bilgileri
      "cardHolderName": "Mehmet Test",  // Kart sahibinin adı. Kartın üzerindeki ismi belirtir.
      "cardNumber": "5526080000000006",  // Kart numarası. Bu, kartın 16 haneli numarasını temsil eder.
      "expireYear": "2028",  // Kartın son kullanım yılı. Kartın geçerlilik süresinin bittiği yıl.
      "expireMonth": "11",  // Kartın son kullanım ayı. Kartın geçerlilik süresinin bittiği ay.
      "cvc": "245",  // Kartın güvenlik kodu. Kartın arkasındaki 3 haneli kodu ifade eder.
      "registerCard": 0  // Kartın kaydedilip kaydedilmediği. 0: Hayır, kart kaydedilmemiştir. 1: Evet, kart kaydedilmiştir.
   },
   "buyer": {  // Alıcı bilgileri
      "id": "BY789",  // Alıcının benzersiz kimliği. Alıcıyı tanımlamak için kullanılan bir ID.
      "name": "John",  // Alıcının adı.
      "surname": "Doe",  // Alıcının soyadı.
      "identityNumber": "11111111111",  // Alıcının kimlik numarası. Bu, alıcının resmi kimliğini belirtir.
      "email": "test@testtt.com",  // Alıcının e-posta adresi. İletişim için kullanılır.
      "gsmNumber": "+905393623333",  // Alıcının GSM numarası. Mobil iletişim için kullanılır.
      "registrationDate": "2013-04-21 15:12:09",  // Alıcının kayıt tarihi. Alıcının sistemdeki kayıt tarihi ve saati.
      "lastLoginDate": "2015-10-05 12:43:35",  // Alıcının son giriş tarihi. Sisteme son giriş yaptığı tarih ve saat.
      "registrationAddress": "Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1",  // Alıcının kayıt adresi. Alıcının sistemde kayıtlı adresi.
      "city": "Istanbul",  // Şehir. Alıcının yaşadığı şehir.
      "country": "Turkey",  // Ülke. Alıcının yaşadığı ülke.
      "zipCode": "34732",  // Posta kodu. Alıcının adresinin posta kodu.
      "ip": "85.34.78.112"  // IP adresi. Alıcının işlem yaptığı IP adresi. Güvenlik ve doğrulama için kullanılır.
   },
   "shippingAddress": {  // Gönderim adresi
      "address": "Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1",  // Gönderim adresi. Ürünün gönderileceği tam adres.
      "zipCode": "34742",  // Gönderim adresinin posta kodu.
      "contactName": "Jane Doe",  // İletişim adı. Gönderim adresindeki kişi.
      "city": "Istanbul",  // Şehir. Gönderim adresinin şehir bilgisi.
      "country": "Turkey"  // Ülke. Gönderim adresinin ülke bilgisi.
   },
   "billingAddress": {  // Fatura adresi
      "address": "Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1",  // Fatura adresi. Faturanın gönderileceği tam adres.
      "zipCode": "34742",  // Fatura adresinin posta kodu.
      "contactName": "Jane Doe",  // İletişim adı. Fatura adresindeki kişi.
      "city": "Istanbul",  // Şehir. Fatura adresinin şehir bilgisi.
      "country": "Turkey"  // Ülke. Fatura adresinin ülke bilgisi.
   },
   "basketItems": [  // Sepet içeriği // Birden fazla ürün için for döngüsü ile ürün ekle. (sepet/views.py kodlarında mevcut)
      {
         "id": "BI101",  // Ürün kimliği. Sepetteki ürünün benzersiz tanımlayıcısı.
         "price": "10.01",  // Ürün fiyatı. Ürünün birim fiyatı.
         "name": "Binocular",  // Ürün adı. Sepetteki ürünün ismi.
         "category1": "Collectibles",  // Birinci kategori. Ürünün ait olduğu birincil kategori.
         "category2": "Accessories",  // İkinci kategori. Ürünün ait olduğu ikincil kategori.
         "itemType": "PHYSICAL"  // Ürün tipi. Ürünün fiziksel mi yoksa dijital mi olduğunu belirtir; burada "PHYSICAL" fiziksel ürün anlamına gelir.
      }
   ]
}

