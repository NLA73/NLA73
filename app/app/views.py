from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import resume # Pastikan ini huruf kecil 'r' sesuai error tadi

# 1. FUNGSI LOGIN (Yang tadi hilang/error)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username atau Password salah!")
            
    return render(request, 'login.html')

# 2. FUNGSI HALAMAN UTAMA (JOA)
@login_required(login_url='login')
def home_view(request):
    # Ambil semua data dari database untuk ditampilkan di tabel
    semua_data = resume.objects.all()
    return render(request, 'index.html', {'semua_data': semua_data})

# 3. FUNGSI SIMPAN DATA KE MYSQL
def simpan_resume_view(request):
    if request.method == 'POST':
        c = request.POST.get('consignee')
        a = request.POST.get('alamat_bongkar')
        t = request.POST.get('tarif')
        p = request.POST.get('profit')

        resume.objects.create(
            consignee=c,
            alamat_bongkar=a,
            tarif=t,
            profit=p
        )
        return redirect('home')
    return redirect('home')

# 4. FUNGSI KELUAR
def logout_view(request):
    logout(request)
    return redirect('login')