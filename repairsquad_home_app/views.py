from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import ProfileUpdateForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from users.forms import UserUpdateForm, ProfileUpdateForm
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

@login_required
def RepairOrderView(request):
    page_tittle = "Repair Order"
    
    if request.method == 'POST':
        p_u_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile)
        repair_order_form = RepairOrderForm(request.POST)
        repair_order_form.instance.owner = request.user
        if repair_order_form and p_u_form.is_valid():
            p_u_form.save()
            repair_order_form.save()
            username = request.user
            messages.success(
                request,
                f'{username}, Thanks for placing a repair order . Our customer care will be contacting you soon, to confirm and process your request'
            )
            odr_id = RepairOrderModel.objects.all().filter(
                owner=request.user).order_by('-order_date')[0].order_id
            
            content = f"Thanks for Placing a repair order. Your Order ID is {odr_id} . Our customer care will be contacting you soon, to confirm and process your request"
            html_msg = render_to_string('repairsquad_home_app/email_templates/email.html', context={
                'username': request.user.username,
                'content': content,
            })
            send_mail(
                "REPAIR SQUAD NOTIFICATION",
                f"Hi {request.user.username} Thanks for Placing a repair order. Your Order ID is {odr_id} . Our customer care will be contacting you soon, to confirm and process your request ",
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=True,
                html_message=html_msg,
            )

            admin_content = f"THE USERNAME ABOVE PLACE A REPAIR ORDER WITH ORDER ID {odr_id} . PLEASE CHECK IT UP AND PROCESS"
            admin_html_msg = render_to_string('repairsquad_home_app/email_templates/email.html', context={
                'username': request.user.username,
                'content': admin_content,
            })
            send_mail(
                "REPAIR SQUAD NOTIFICATION",
                f"THE USERNAME ABOVE PLACE A REPAIR ORDER WITH ORDER ID {odr_id} . PLEASE CHECK IT UP AND PROCESS",
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=True,
                html_message=admin_html_msg,
            )
            return redirect('profile')
        
    else:
        repair_order_form = RepairOrderForm()
        p_u_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'page_tittle': page_tittle,
        'repair_order_form': repair_order_form,
        'p_u_form': p_u_form
    }
    return render(request, 'repairsquad_home_app/repair_order_form.html', context)