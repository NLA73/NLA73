from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    nomor_sales = models.CharField(max_length=20, unique=True, null=True, blank=True)
    REQUIRED_FIELDS = ['nomor_sales']

    class Meta:
        db_table = 'auth_user'


class Customer(models.Model):
    kode_customer = models.CharField(max_length=20, unique=True)
    nama_customer = models.CharField(max_length=200)
    pol           = models.CharField(max_length=150, blank=True, null=True)
    pod           = models.CharField(max_length=150, blank=True, null=True)
    created_at    = models.DateTimeField(default=timezone.now)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kode_customer} - {self.nama_customer}"

    class Meta:
        db_table = 'customer'


class Resume(models.Model):
    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    customer         = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name='resumes')
    bulan            = models.IntegerField(default=1)
    tahun            = models.IntegerField(default=2024)
    pol              = models.CharField(max_length=150, blank=True, null=True)
    pod              = models.CharField(max_length=150, blank=True, null=True)
    consignee        = models.CharField(max_length=100, blank=True)
    alamat_bongkar   = models.TextField(blank=True)
    tarif_jasa_kirim = models.BigIntegerField(default=0)
    ppn_pct          = models.DecimalField(max_digits=5, decimal_places=2, default=11)
    ppn              = models.BigIntegerField(default=0)
    pph              = models.BigIntegerField(default=0)
    pph23            = models.BigIntegerField(default=0)
    total            = models.BigIntegerField(default=0)
    total_biaya      = models.BigIntegerField(default=0)
    profit           = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'resume'


class BiayaMuat(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name='biaya_muats')
    bulan       = models.IntegerField(default=1)
    tahun       = models.IntegerField(default=2024)
    pol         = models.CharField(max_length=150, blank=True, null=True)
    pod         = models.CharField(max_length=150, blank=True, null=True)
    job_no      = models.CharField(max_length=20, blank=True)
    inc         = models.BooleanField(default=True)
    tertanggung = models.CharField(max_length=100, blank=True)
    persen      = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    premi       = models.BigIntegerField(default=0)
    bl_fee      = models.BigIntegerField(default=0)
    seal        = models.BigIntegerField(default=0)
    freight     = models.BigIntegerField(default=0)
    lss         = models.BigIntegerField(default=0)
    toeslag     = models.BigIntegerField(default=0)
    alur        = models.BigIntegerField(default=0)
    thc_muat    = models.BigIntegerField(default=0)
    lolo_muat   = models.BigIntegerField(default=0)
    stuffing    = models.BigIntegerField(default=0)
    damage      = models.BigIntegerField(default=0)
    trucking    = models.BigIntegerField(default=0)
    ops         = models.BigIntegerField(default=0)
    tally       = models.BigIntegerField(default=0)
    lain_1      = models.BigIntegerField(default=0)
    lain_2      = models.BigIntegerField(default=0)
    total_biaya = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'biaya_muat'


class BiayaBongkar(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name='biaya_bongkars')
    bulan           = models.IntegerField(default=1)
    tahun           = models.IntegerField(default=2024)
    pol             = models.CharField(max_length=150, blank=True, null=True)
    pod             = models.CharField(max_length=150, blank=True, null=True)
    job_no          = models.CharField(max_length=20, blank=True)
    doc_fee         = models.BigIntegerField(default=0)
    cleaning        = models.BigIntegerField(default=0)
    thc_bongkar     = models.BigIntegerField(default=0)
    lolo_bongkar    = models.BigIntegerField(default=0)
    stripping_dalam = models.BigIntegerField(default=0)
    trucking        = models.BigIntegerField(default=0)
    buruh           = models.BigIntegerField(default=0)
    materai         = models.BigIntegerField(default=0)
    ops             = models.BigIntegerField(default=0)
    tally_bongkar   = models.BigIntegerField(default=0)
    alat            = models.BigIntegerField(default=0)
    fee             = models.BigIntegerField(default=0)
    door_service    = models.BigIntegerField(default=0)
    by_lain         = models.BigIntegerField(default=0)
    by_lain_2       = models.BigIntegerField(default=0)
    by_lain_3       = models.BigIntegerField(default=0)
    tot_by_bongkar  = models.BigIntegerField(default=0)
    vendor_muat     = models.CharField(max_length=100, blank=True)
    panduan_muat    = models.CharField(max_length=100, blank=True)
    vendor_bongkar  = models.CharField(max_length=100, blank=True)
    panduan_bongkar = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'biaya_bongkar'