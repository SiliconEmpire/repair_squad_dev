from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views as repairsquad_home_app_views

urlpatterns = [
    path('', repairsquad_home_app_views.home_page_view, name='home'),
    path('quick-repair-order', repairsquad_home_app_views.quickRepairOrderView, name='quick_repair_order'),
    path('repair-order', repairsquad_home_app_views.RepairOrderView, name='repair_order'),
]