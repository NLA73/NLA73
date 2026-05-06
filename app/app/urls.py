from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.dashboard_view,                name='dashboard'),
    path('form/',               views.home_view,                     name='home'),
    path('login/',              views.login_view,                    name='login'),
    path('logout/',             views.logout_view,                   name='logout'),
    
    # Save Endpoints
    path('save-resume/',        views.SaveResumeView.as_view(),      name='save_resume'),
    path('save-biaya-muat/',    views.SaveBiayaMuatView.as_view(),    name='save_biaya_muat'),
    path('save-biaya-bongkar/', views.SaveBiayaBongkarView.as_view(), name='save_biaya_bongkar'),
    
    # Delete Row Endpoints
    path('delete-resume/',        views.DeleteResumeView.as_view(),      name='delete_resume'),
    path('delete-biaya-muat/',    views.DeleteBiayaMuatView.as_view(),    name='delete_biaya_muat'),
    path('delete-biaya-bongkar/', views.DeleteBiayaBongkarView.as_view(), name='delete_biaya_bongkar'),
    
    # Batch Action Endpoints (Dashboard)
    path('delete-sales-data/',    views.DeleteSalesDataView.as_view(),   name='delete_sales_data'),
    path('copy-sales-data/',      views.CopySalesDataView.as_view(),     name='copy_sales_data'),
    
    # Utils
    path('update-customer/',        views.UpdateCustomerView.as_view(),   name='update_customer'),
    path('get-customers-by-sales/', views.get_customers_by_sales,         name='get_customers_by_sales'),
    path('batch-delete-rows/', views.BatchDeleteRowsView.as_view(), name='batch_delete_rows'),
    path('print-invoice/', views.print_view, name='print_invoice'),
]
