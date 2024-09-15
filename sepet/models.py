from django.db import models

# Create your models here.

class Urun(models.Model):
    ad = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    resim = models.ImageField(upload_to='urunler/', blank=True, null=True)
    kategori1 = models.CharField(max_length=255, blank=True, null=True)
    kategori2 = models.CharField(max_length=255, blank=True, null=True)
    urun_tipi = models.CharField(max_length=50, choices=[('FIZIKSEL', 'Fiziksel'), ('Dijital', 'Dijital')], default='FIZIKSEL')

    def __str__(self):
        return self.ad