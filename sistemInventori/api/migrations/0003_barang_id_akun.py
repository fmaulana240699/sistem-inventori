# Generated by Django 4.2.7 on 2024-01-15 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_barang_nama_barang'),
    ]

    operations = [
        migrations.AddField(
            model_name='barang',
            name='id_akun',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]