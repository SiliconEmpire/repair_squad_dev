from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import (
    QuickRepairOrderModel,
    RepairOrderModel
)
from .forms import (
    QuickRepairOrderForm,
    RepairOrderForm
)


def home_page_view(request):
    page_tittle = 'Welcome To Repair Squad'
    context = {
        'page_tittle': page_tittle
    }
    return render(request, 'repairsquad_home_app/homepage.html', context)


def quickRepairOrderView(request):
    page_tittle = "Quick Repair Order"

    if request.method == 'POST':
        quick_repair_order_form = QuickRepairOrderForm(request.POST)

        if quick_repair_order_form.is_valid():
            # check if the phone_number already exist in the database, if yes dont save just increase the request count by 1
            # qs_exists= Klass.objects.filter(serviceReq_id = serviceReq_new_id).exists()
            name = quick_repair_order_form.cleaned_data.get('name')
            phoneNumber = quick_repair_order_form.cleaned_data.get(
                'phone_number')
            print(f' *****name is :{name} phonenumber is: {phoneNumber}')
            qs_exists = QuickRepairOrderModel.objects.filter(
                phone_number=phoneNumber).exists()
            if qs_exists:
                quick_repair_order_qs = QuickRepairOrderModel.objects.get(
                    phone_number=phoneNumber)
                quick_repair_order_qs.req_count = quick_repair_order_qs.req_count + 1
                quick_repair_order_qs.save()

                if(quick_repair_order_qs.req_count > 0 and quick_repair_order_qs.request_status == 'PENDING'):
                    print(
                        f' Thanks {name} we got your initial request we will call you soon')
                    messages.info(
                        request, f' Thanks {name} we got your initial request we will call you soon')
                    return redirect('quick_repair_order')

                elif (quick_repair_order_qs.request_status == 'CALLED'):
                    print(
                        f' Hi, {name} This quick repair order service is meant for first time visitors'
                        ' only, our system detects that you\'ve'
                        ' used this service before, you may not get a call'
                        ' back, we recommend that you place your repair order here'
                        ' thanks. the Repair Squad Team'
                    )
                    messages.warning(request, f' Hi, {name} This quick repair order service is meant for first time visitors'
                                     ' only, our system detects that you\'ve'
                                     ' used this service before, you may not get a call'
                                     ' back, we recommend that you place your repair order here '
                                     ' thanks. the Repair Squad Team')
                    return redirect('quick_repair_order')

            else:
                quick_repair_order_form.save()
                print(
                    f'Hi, {name} thanks for choosing to use Repair Squad, we will call you as soon as possible ')
                messages.success(
                    request, f'Hi, {name} thanks for choosing to use Repair Squad, our customer care will contact you soon ')
                return redirect('quick_repair_order')

        return redirect('quick_repair_order')
    else:
        quick_repair_order_form = QuickRepairOrderForm()

    context = {
        'page_tittle': page_tittle,
        'quick_repair_order_form': quick_repair_order_form
    }
    return render(request, 'repairsquad_home_app/quick_repair_order_form.html', context)

def RepairOrderView(request):
    page_tittle = "Quick Repair Order"
    
    if request.method == 'POST':
        pass
    else:
        repair_order_form = RepairOrderForm()

    context = {
        'page_tittle': page_tittle,
        'repair_order_form': repair_order_form
    }
    return render(request, 'repairsquad_home_app/repair_order_form.html', context)