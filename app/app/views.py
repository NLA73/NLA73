import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q

def _pol_pod_filter(pol, pod):
    """Build Q filter that handles None vs empty string for pol/pod."""
    q = Q()
    if pol:
        q &= Q(pol=pol)
    else:
        q &= (Q(pol__isnull=True) | Q(pol=''))
    if pod:
        q &= Q(pod=pod)
    else:
        q &= (Q(pod__isnull=True) | Q(pod=''))
    return q

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator
from django.utils import timezone
from .models import Resume, BiayaBongkar, BiayaMuat, User, Customer
from .serializers import ResumeSerializer, BiayaMuatSerializer, BiayaBongkarSerializer


# 1. LOGIN
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        u    = request.POST.get('username')
        p    = request.POST.get('password')
        user = authenticate(request, username=u, password=p)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username atau Password salah!")

    return render(request, 'login.html')


# 2. DASHBOARD (MODE SELECTION)
@login_required(login_url='login')
def dashboard_view(request):
    mode      = request.GET.get('mode', 'edit')
    sales_id  = request.GET.get('sales_id')
    page_num  = request.GET.get('page', 1)
    search_q  = request.GET.get('q', '').strip()
    
    now = timezone.now()
    bulan_param = request.GET.get('bulan')
    tahun_param = request.GET.get('tahun')
    
    selected_bulan = int(bulan_param) if bulan_param else now.month
    selected_tahun = int(tahun_param) if tahun_param else now.year

    target_sales = request.user
    if mode == 'view':
        if sales_id:
            target_sales = get_object_or_404(User, id=sales_id)
    else:
        mode = 'edit'

    # Retrieve unique shipment sets (Customer + Ports) for the targeted user and period
    # We check all three tables to ensure no shipment is missed
    shipment_sets = set()
    
    res_sets = Resume.objects.filter(user=target_sales, bulan=selected_bulan, tahun=selected_tahun).values_list('customer_id', 'pol', 'pod')
    muat_sets = BiayaMuat.objects.filter(user=target_sales, bulan=selected_bulan, tahun=selected_tahun).values_list('customer_id', 'pol', 'pod')
    bong_sets = BiayaBongkar.objects.filter(user=target_sales, bulan=selected_bulan, tahun=selected_tahun).values_list('customer_id', 'pol', 'pod')
    
    shipment_sets.update(res_sets)
    shipment_sets.update(muat_sets)
    shipment_sets.update(bong_sets)

    display_list = []
    for cust_id, pol, pod in shipment_sets:
        cust = Customer.objects.get(id=cust_id)
        
        # Normalize ports to empty string for consistent UI comparison
        pol_norm = pol or ''
        pod_norm = pod or ''

        # Simple search filter
        if search_q:
            q = search_q.lower()
            if not (q in cust.nama_customer.lower() or q in cust.kode_customer.lower() or 
                    (pol_norm and q in pol_norm.lower()) or (pod_norm and q in pod_norm.lower())):
                continue

        display_list.append({
            'customer': cust,
            'pol': pol_norm,
            'pod': pod_norm,
        })
    
    display_list.sort(key=lambda x: x['customer'].nama_customer)

    # Pagination
    paginator = Paginator(display_list, 10)
    page_obj  = paginator.get_page(page_num)

    all_mst_customers = Customer.objects.all().order_by('nama_customer')
    all_sales = User.objects.exclude(id=request.user.id)
    
    # Info Waktu
    months = [
        (1, "JANUARI"), (2, "FEBRUARI"), (3, "MARET"), (4, "APRIL"),
        (5, "MEI"), (6, "JUNI"), (7, "JULI"), (8, "AGUSTUS"),
        (9, "SEPTEMBER"), (10, "OKTOBER"), (11, "NOVEMBER"), (12, "DESEMBER")
    ]
    years = range(2023, now.year + 3)
    
    return render(request, 'dashboard.html', {
        'page_obj'          : page_obj,
        'all_sales'         : all_sales,
        'all_mst_customers' : all_mst_customers,
        'target_sales'      : target_sales,
        'mode'              : mode,
        'months'            : months,
        'years'             : years,
        'selected_bulan'    : selected_bulan,
        'selected_tahun'    : selected_tahun,
        'search_q'          : search_q,
    })


# AJAX endpoint for View Mode
@login_required
def get_customers_by_sales(request):
    sales_id = request.GET.get('sales_id')
    customers = Customer.objects.filter(sales_id=sales_id).values('id', 'kode_customer', 'nama_customer')
    data = [{'id': c['id'], 'kode': c['kode_customer'], 'nama': c['nama_customer']} for c in customers]
    return JsonResponse({'customers': data})


# 3. HOME (FORM / INPUT)
@login_required(login_url='login')
def home_view(request):
    customer_id = request.GET.get('customer_id')
    mode        = request.GET.get('mode', 'edit') # 'edit' or 'view'
    target_id   = request.GET.get('user_id') # original owner if in view mode
    bulan       = request.GET.get('bulan')
    tahun       = request.GET.get('tahun')
    pol         = request.GET.get('pol', '') or ''
    pod         = request.GET.get('pod', '') or ''

    if not (customer_id and bulan and tahun):
        return redirect('dashboard')

    customer = get_object_or_404(Customer, id=customer_id)

    if mode == 'view' and target_id:
        target_user = get_object_or_404(User, id=target_id)
        is_readonly = True
    else:
        target_user = request.user
        is_readonly = False

    pp = _pol_pod_filter(pol, pod)
    resumes  = Resume.objects.filter(pp, user=target_user, customer=customer, bulan=bulan, tahun=tahun).order_by('-id')
    muats    = BiayaMuat.objects.filter(pp, user=target_user, customer=customer, bulan=bulan, tahun=tahun).order_by('-id')
    bongkars = BiayaBongkar.objects.filter(pp, user=target_user, customer=customer, bulan=bulan, tahun=tahun).order_by('-id')

    try:
        bulan_int = int(bulan)
    except (ValueError, TypeError):
        bulan_int = 1
        
    months_dict = {
        1: "JANUARI", 2: "FEBRUARI", 3: "MARET", 4: "APRIL",
        5: "MEI", 6: "JUNI", 7: "JULI", 8: "AGUSTUS",
        9: "SEPTEMBER", 10: "OKTOBER", 11: "NOVEMBER", 12: "DESEMBER"
    }
    bulan_name = months_dict.get(bulan_int, "")

    return render(request, 'index.html', {
        'customer'    : customer,
        'resumes'     : resumes,
        'muats'       : muats,
        'bongkars'    : bongkars,
        'is_readonly' : is_readonly,
        'target_user' : target_user,
        'bulan'       : bulan,
        'tahun'       : tahun,
        'bulan_name'  : bulan_name,
        'pol'         : pol,
        'pod'         : pod,
    })


# 3. SAVE RESUME
class SaveResumeView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        row_id = request.data.get('id')
        
        if row_id:
            # Using select_for_update to handle concurrent edits safely inside the transaction
            obj = get_object_or_404(Resume.objects.select_for_update(), id=row_id)
            if obj.user != request.user:
                return Response({'status': 'error', 'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
            serializer = ResumeSerializer(obj, data=request.data, partial=True)
        else:
            serializer = ResumeSerializer(data=request.data)
            
        if serializer.is_valid():
            customer_id = request.data.get('customer_id')
            bulan = request.data.get('bulan')
            tahun = request.data.get('tahun')
            pol = request.data.get('pol')
            pod = request.data.get('pod')
            serializer.save(user=request.user, customer_id=customer_id, bulan=bulan, tahun=tahun, pol=pol, pod=pod)
            return Response({'status': 'success', 'id': serializer.instance.id})
            
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# 4. SAVE BIAYA MUAT
class SaveBiayaMuatView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        row_id = request.data.get('id')
        
        if row_id:
            obj = get_object_or_404(BiayaMuat.objects.select_for_update(), id=row_id)
            if obj.user != request.user:
                return Response({'status': 'error', 'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
            serializer = BiayaMuatSerializer(obj, data=request.data, partial=True)
        else:
            serializer = BiayaMuatSerializer(data=request.data)
            
        if serializer.is_valid():
            customer_id = request.data.get('customer_id')
            bulan = request.data.get('bulan')
            tahun = request.data.get('tahun')
            pol = request.data.get('pol')
            pod = request.data.get('pod')
            serializer.save(user=request.user, customer_id=customer_id, bulan=bulan, tahun=tahun, pol=pol, pod=pod)
            return Response({'status': 'success', 'id': serializer.instance.id})
            
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# 5. SAVE BIAYA BONGKAR
class SaveBiayaBongkarView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        row_id = request.data.get('id')
        
        if row_id:
            obj = get_object_or_404(BiayaBongkar.objects.select_for_update(), id=row_id)
            if obj.user != request.user:
                return Response({'status': 'error', 'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
            serializer = BiayaBongkarSerializer(obj, data=request.data, partial=True)
        else:
            serializer = BiayaBongkarSerializer(data=request.data)
            
        if serializer.is_valid():
            customer_id = request.data.get('customer_id')
            bulan = request.data.get('bulan')
            tahun = request.data.get('tahun')
            pol = request.data.get('pol')
            pod = request.data.get('pod')
            serializer.save(user=request.user, customer_id=customer_id, bulan=bulan, tahun=tahun, pol=pol, pod=pod)
            return Response({'status': 'success', 'id': serializer.instance.id})
            
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# 6. LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 7. UPDATE CUSTOMER
class UpdateCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customer_id = request.data.get('customer_id')
        pol = request.data.get('pol')
        pod = request.data.get('pod')
        
        customer = get_object_or_404(Customer, id=customer_id)
        
        if pol is not None:
            customer.pol = pol
        if pod is not None:
            customer.pod = pod
        
        customer.save()
        return Response({'status': 'success'})
            

# 8. DELETE ENDPOINTS
class DeleteResumeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        row_id = request.data.get('id')
        obj = get_object_or_404(Resume, id=row_id)
        if obj.user != request.user:
            return Response({'status': 'error', 'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response({'status': 'success'})

class DeleteBiayaMuatView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        row_id = request.data.get('id')
        obj = get_object_or_404(BiayaMuat, id=row_id)
        if obj.user != request.user:
            return Response({'status': 'error', 'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response({'status': 'success'})

class DeleteBiayaBongkarView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        row_id = request.data.get('id')
        obj = get_object_or_404(BiayaBongkar, id=row_id)
        if obj.user != request.user:
            return Response({'status': 'error', 'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response({'status': 'success'})

# 9. BATCH ACTIONS & PER-SHIPMENT DATA
class BatchDeleteRowsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        table = request.data.get('table') # 'resume', 'muat', 'bongkar'
        
        if table == 'resume':
            Resume.objects.filter(id__in=ids, user=request.user).delete()
        elif table == 'muat':
            BiayaMuat.objects.filter(id__in=ids, user=request.user).delete()
        elif table == 'bongkar':
            BiayaBongkar.objects.filter(id__in=ids, user=request.user).delete()
            
        return Response({'status': 'success'})

class DeleteSalesDataView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customer_id = request.data.get('customer_id')
        try:
            bulan = int(request.data.get('bulan', 0))
            tahun = int(request.data.get('tahun', 0))
        except (ValueError, TypeError):
            return Response({'status': 'error', 'message': 'Invalid period'}, status=400)
            
        pol = request.data.get('pol', '') or ''
        pod = request.data.get('pod', '') or ''
        
        pp = _pol_pod_filter(pol, pod)
        Resume.objects.filter(pp, user=request.user, customer_id=customer_id, bulan=bulan, tahun=tahun).delete()
        BiayaMuat.objects.filter(pp, user=request.user, customer_id=customer_id, bulan=bulan, tahun=tahun).delete()
        BiayaBongkar.objects.filter(pp, user=request.user, customer_id=customer_id, bulan=bulan, tahun=tahun).delete()
        
        return Response({'status': 'success'})

class CopySalesDataView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customer_id = request.data.get('customer_id')
        src_bulan = int(request.data.get('src_bulan'))
        src_tahun = int(request.data.get('src_tahun'))
        tgt_bulan = int(request.data.get('tgt_bulan'))
        tgt_tahun = int(request.data.get('tgt_tahun'))
        target_pol = request.data.get('tgt_pol', '')
        target_pod = request.data.get('tgt_pod', '')
        src_pol = request.data.get('src_pol', '')
        src_pod = request.data.get('src_pod', '')

        # 1. Fetch Source Data
        src_pp = _pol_pod_filter(src_pol, src_pod)
        resumes  = list(Resume.objects.filter(src_pp, user=request.user, customer_id=customer_id, bulan=src_bulan, tahun=src_tahun))
        muats    = list(BiayaMuat.objects.filter(src_pp, user=request.user, customer_id=customer_id, bulan=src_bulan, tahun=src_tahun))
        bongkars = list(BiayaBongkar.objects.filter(src_pp, user=request.user, customer_id=customer_id, bulan=src_bulan, tahun=src_tahun))

        if not (resumes or muats or bongkars):
            return Response({'status': 'error', 'message': 'Tidak ada data sumber di periode terpilih.'}, status=400)

        # 2. Duplicate Records — always create NEW rows
        for r in resumes:
            r.pk = None
            r.bulan = tgt_bulan
            r.tahun = tgt_tahun
            r.pol = target_pol or ''
            r.pod = target_pod or ''
            r.save()
        for m in muats:
            m.pk = None
            m.bulan = tgt_bulan
            m.tahun = tgt_tahun
            m.pol = target_pol or ''
            m.pod = target_pod or ''
            m.save()
        for b in bongkars:
            b.pk = None
            b.bulan = tgt_bulan
            b.tahun = tgt_tahun
            b.pol = target_pol or ''
            b.pod = target_pod or ''
            b.save()

        return Response({'status': 'success'})

@login_required(login_url='login')
def print_view(request):
    customer_id = request.GET.get('customer_id')
    bulan       = request.GET.get('bulan')
    tahun       = request.GET.get('tahun')
    pol         = request.GET.get('pol', '') or ''
    pod         = request.GET.get('pod', '') or ''
    
    res_ids  = [x for x in request.GET.get('res_ids', '').split(',') if x]
    muat_ids = [x for x in request.GET.get('muat_ids', '').split(',') if x]
    bong_ids = [x for x in request.GET.get('bong_ids', '').split(',') if x]
    row_nums = [x for x in request.GET.get('row_nums', '').split(',') if x]
    
    customer = get_object_or_404(Customer, id=customer_id)
    
    # Fetch objects and maintain order based on selected lists
    res_objs = {obj.id: obj for obj in Resume.objects.filter(id__in=res_ids)}
    muat_objs = {obj.id: obj for obj in BiayaMuat.objects.filter(id__in=muat_ids)}
    bong_objs = {obj.id: obj for obj in BiayaBongkar.objects.filter(id__in=bong_ids)}
    
    data_list = []
    total_tarif = 0
    total_ppn = 0
    total_all = 0
    
    for i in range(len(res_ids)):
        r_id = int(res_ids[i]) if res_ids[i] else None
        m_id = int(muat_ids[i]) if i < len(muat_ids) and muat_ids[i] else None
        b_id = int(bong_ids[i]) if i < len(bong_ids) and bong_ids[i] else None
        
        res = res_objs.get(r_id)
        if res:
            total_tarif += (res.tarif_jasa_kirim or 0)
            total_ppn += (res.ppn or 0)
            total_all += (res.total or 0)
            
        data_list.append({
            'resume': res,
            'muat': muat_objs.get(m_id),
            'bongkar': bong_objs.get(b_id),
            'job_no': row_nums[i] if i < len(row_nums) else ''
        })
    
    # Info Waktu
    months_dict = {
        1: "JANUARI", 2: "FEBRUARI", 3: "MARET", 4: "APRIL",
        5: "MEI", 6: "JUNI", 7: "JULI", 8: "AGUSTUS",
        9: "SEPTEMBER", 10: "OKTOBER", 11: "NOVEMBER", 12: "DESEMBER"
    }
    bulan_name = months_dict.get(int(bulan or 1), "")

    return render(request, 'print_invoice.html', {
        'customer': customer,
        'data_list': data_list,
        'bulan_name': bulan_name,
        'tahun': tahun,
        'pol': pol,
        'pod': pod,
        'total_tarif': total_tarif,
        'total_ppn': total_ppn,
        'total_all': total_all,
    })
