from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Resume, BiayaMuat, BiayaBongkar, Customer

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('nomor_sales',)}),
    )
    list_display = ('username', 'email', 'nomor_sales', 'is_staff')
    search_fields = ('username', 'email', 'nomor_sales')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'consignee', 'total', 'profit')
    list_filter = ('user',)
    search_fields = ('consignee',)

@admin.register(BiayaMuat)
class BiayaMuatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job_no', 'total_biaya')
    list_filter = ('user',)
    search_fields = ('job_no', 'tertanggung')

@admin.register(BiayaBongkar)
class BiayaBongkarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job_no', 'tot_by_bongkar')
    list_filter = ('user',)
    search_fields = ('job_no', 'vendor_muat', 'vendor_bongkar')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'kode_customer', 'nama_customer')
    list_filter = ('kode_customer',)
    search_fields = ('kode_customer', 'nama_customer')
