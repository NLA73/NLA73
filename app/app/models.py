from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nomor_sales = models.CharField(max_length=20, unique=True, null=True, blank=True)
    REQUIRED_FIELDS = ['nomor_sales']

    class Meta:
        db_table = 'auth_user' # PAKSA PAKAI NAMA INI

class resume(models.Model):
    # Nama variabel (kiri) disamakan dengan nama kolom MySQL (kanan)
    consignee = models.CharField(max_length=100)
    alamat_bongkar = models.TextField()
    tarif_jasa_kirim = models.IntegerField() # Sesuai foto MySQL
    ppn = models.IntegerField(default=0)
    pph = models.IntegerField(default=0)
    pph23 = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    total_biaya = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)

    class Meta:
        db_table = 'resume' # Memastikan Django lari ke tabel 'resume'

class BiayaMuat(models.Model):
    job_no        = models.CharField(max_length=20)
    inc           = models.BooleanField(default=True)       # checkbox
    tertanggung   = models.CharField(max_length=100)
    persen        = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    premi         = models.IntegerField(default=0)
    bl_fee        = models.IntegerField(default=0)
    seal          = models.IntegerField(default=0)
    freight       = models.IntegerField(default=0)
    lss           = models.IntegerField(default=0)
    toeslag       = models.IntegerField(default=0)
    alur          = models.IntegerField(default=0)
    thc_muat      = models.IntegerField(default=0)
    lolo_muat     = models.IntegerField(default=0)
    stuffing      = models.IntegerField(default=0)
    damage        = models.IntegerField(default=0)
    trucking      = models.IntegerField(default=0)
    ops           = models.IntegerField(default=0)
    tally         = models.IntegerField(default=0)
    lain_1        = models.IntegerField(default=0)
    lain_2        = models.IntegerField(default=0)
    total_biaya   = models.IntegerField(default=0)

    class Meta:
        db_table = 'biaya_muat'

class BiayaBongkar(models.Model):
    job_no          = models.CharField(max_length=20)
    doc_fee         = models.IntegerField(default=0)
    cleaning        = models.IntegerField(default=0)
    thc_bongkar     = models.IntegerField(default=0)
    lolo_bongkar    = models.IntegerField(default=0)
    stripping_dalam = models.IntegerField(default=0)
    trucking        = models.IntegerField(default=0)
    buruh           = models.IntegerField(default=0)
    materai         = models.IntegerField(default=0)
    ops             = models.IntegerField(default=0)
    tally_bongkar   = models.IntegerField(default=0)
    alat            = models.IntegerField(default=0)
    fee             = models.IntegerField(default=0)
    door_service    = models.IntegerField(default=0)
    by_lain         = models.IntegerField(default=0)
    by_lain_2       = models.IntegerField(default=0)
    by_lain_3       = models.IntegerField(default=0)
    tot_by_bongkar  = models.IntegerField(default=0)
    vendor_muat     = models.CharField(max_length=100, blank=True)
    panduan_muat    = models.CharField(max_length=100, blank=True)
    vendor_bongkar  = models.CharField(max_length=100, blank=True)
    panduan_bongkar = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'biaya_bongkar'