from django.db import models

# Create your models here.
# models.py

from django.db import models

class Akun(models.Model):
    nama_lengkap = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    gender = models.BooleanField()
    email = models.EmailField()
    jabatan = models.CharField(max_length=20)
    password = models.CharField(max_length=16)
    no_hp = models.CharField(max_length=16)

    # def __str__(self):
    #     return self.name

class Barang(models.Model):
    nama_barang = models.CharField(max_length=20)
    status_barang = models.CharField(max_length=20)
    # qr_code = models
    jenis_barang = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=20)

    # def __str__(self):
    #     return self.title

class Peminjaman(models.Model):
    tanggal_peminjaman = models.DateField()
    tanggal_pengembalian = models.DateField()
    status_peminjaman = models.CharField(max_length=20)
    # id_akun = models
    # durasi_peminjaman = models

    # def __str__(self):
    #     return f"{self.book.title} - {self.borrower_name}"
    
class Stock(models.Model):
    # id_barang = models
    jumlah_barang = models.IntegerField()
    # nama_barang = models.CharField()

    # def __str__(self):
    #     return f"{self.book.title} - {self.borrower_name}"    
