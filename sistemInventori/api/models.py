from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
# Create your models here.
# models.py

from django.db import models

class Akun(AbstractBaseUser):
    nama_lengkap = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    gender = models.BooleanField()
    email = models.EmailField()
    jabatan = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=16)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    @property
    def is_anonymous(self):
        return False
    @property
    def is_authenticated(self):
        return True
    
    def __unicode__(self):
        return self.nama_lengkap
    

class Barang(models.Model):
    nama_barang = models.CharField(max_length=20)
    status_barang = models.CharField(max_length=20)
    qr_code = models.TextField(blank=True, null=True)
    jenis_barang = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=20, unique=True)

class Peminjaman(models.Model):
    tanggal_peminjaman = models.DateField()
    tanggal_pengembalian = models.DateField()
    status_peminjaman = models.CharField(max_length=20, null=True)
    id_akun = models.ForeignKey(Akun, on_delete=models.CASCADE, null=True)
    durasi_peminjaman = models.IntegerField(null=True, blank=True) 
    id_barang = models.ForeignKey(Barang, on_delete=models.CASCADE, null=True)
    
class Stock(models.Model):
    nama_barang = models.CharField(max_length=100, blank=True, editable=False, primary_key=True) 
    id_barang = models.CharField(max_length=100, blank=True, editable=False, null=True) 
    jumlah_barang = models.IntegerField(default=0, null=True)