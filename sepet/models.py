from django.db import models

# Create your models here.

class Kategori(models.Model):
    isim=models.CharField(max_length=255)

class Urun(models.Model):
    isim=models.CharField(max_length=255)
    fiyat=models.DecimalField(max_digits=10, decimal_places=2)
    kategori=models.ForeignKey(Kategori)
