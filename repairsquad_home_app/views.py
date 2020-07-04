from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import ProfileUpdateForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from users.forms import UserUpdateForm, ProfileUpdateForm
from .models import (
    QuickRepairOrderModel,
    RepairOrderModel,
    ContactAndFeedbackModel
)
from .forms import (
    QuickRepairOrderForm,
    RepairOrderForm,
    ContactAndFeedbackForm,
    TrackOrderForm
)


def contactAndFeedbackView(request):
    if request.method == 'POST':
        print("------------------------------------------------------------------------------------")
        contact_and_feedback_form = ContactAndFeedbackForm(request.POST)
        if contact_and_feedback_form.is_valid():
            print("------------------------------------------------------------------------------------")
            contact_and_feedback_form.save()
            name = contact_and_feedback_form.cleaned_data.get('name')
            messages.success(
                request, f'{name}, Thanks For Contacting Us Our Customer Care Will Get Back To You Soon')
            content = "THERE IS A FEEDBACK FROM A REPAIR SQUAD USER, PLEASE CHECK THE BACK END TO REVIEW"
            html_msg = render_to_string('repairsquad_home_app/email_templates/email.html', context={
                'username': request.user.username,
                'content': content,
            })
            send_mail(
                "REPAIR SQUAD NOTIFICATION",
                "THERE IS A FEEDBACK FROM A REPAIR SQUAD USER, PLEASE CHECK THE BACK END TO REVIEW",
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER, ],
                fail_silently=True,
                html_message=html_msg,
            )
            return redirect('home',)
        else:
            messages.error(
                    request, f' oOps! Invalid, please complete the form before sumbitting')
            return redirect('home',)
    else:
        return redirect( 'home',)


def trackOrderView(request):
    page_tittle = 'Order Status'
    if request.method == 'POST':
        track_order_form = TrackOrderForm(request.POST)
        if track_order_form.is_bound and track_order_form.is_valid():
            orderID = track_order_form.cleaned_data.get('order_ID', None)
            order_exists = RepairOrderModel.objects.filter(
                order_id=orderID).exists()
            if order_exists:
                order_instance_qs = RepairOrderModel.objects.get(
                    order_id=orderID)

                context = {
                    'page_tittle': page_tittle,
                    'order_instance_qs': order_instance_qs,
                }
                return render(request, 'repairsquad_home_app/track_status.html', context)
            else:
                messages.error(
                    request, f' oOps! Invalid Order ID')
                return redirect('home',)
        else:
            print("invalid")
            messages.error(
                request, f'INVALID!!!')
            return redirect('home',)
    else:
        print("invalid")
        messages.error(
            request, f'INVALID REQUEST!!!')
        return redirect('home',)


def home_page_view(request):
    page_tittle = 'Welcome To Repair Squad'
    if request.method == 'POST':
        pass
    else:
        contact_and_feedback_form = ContactAndFeedbackForm()
        track_order_form = TrackOrderForm()
    context = {
        'page_tittle': page_tittle,
        'contact_and_feedback_form': contact_and_feedback_form,
        'track_order_form': track_order_form
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
                        ' back, we recommend that you sign up, login place your repair order'
                        ' thanks. the Repair Squad Team'
                    )
                    messages.warning(request, f' Hi, {name} This quick repair order service is meant for first time visitors'
                                     ' only, our system detects that you\'ve'
                                     ' used this service before, you may not get a call'
                                     ' back, we recommend that you sign up/login and place your repair order '
                                     ' thanks. the Repair Squad Team')
                    return redirect('repair_order')

            else:
                quick_repair_order_form.save()
                print(
                    f'Hi, {name} thanks for choosing to use Repair Squad, we will call you as soon as possible ')
                messages.success(
                    request, f'Hi, {name} thanks for choosing to use Repair Squad, our customer care will contact you soon ')
                return redirect('home')

        
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
    username = request.user

    if request.method == 'POST':
        p_u_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile)
        repair_order_form = RepairOrderForm(request.POST)
        repair_order_form.instance.owner = request.user
        if repair_order_form.is_valid() and p_u_form.is_valid():
            p_u_form.save()
            repair_order_form.save()
            
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
        # else:
        #     messages.error(
        #         request,
        #         f'{username}, Please complete the form'
        #     )
        #     return redirect('repair_order')

    else:
        repair_order_form = RepairOrderForm()
        p_u_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'page_tittle': page_tittle,
        'repair_order_form': repair_order_form,
        'p_u_form': p_u_form
    }
    return render(request, 'repairsquad_home_app/repair_order_form.html', context)


@login_required
def RepairOrderUpdateView(request, pk):
    page_tittle = "Update Your Repair Order"
    order_instance = get_object_or_404(RepairOrderModel, id=pk)
    username = request.user
    if order_instance.owner == request.user:
        if request.method == 'POST':
            repairOrder_update_form = RepairOrderForm(
                request.POST, instance=order_instance)
            if repairOrder_update_form.is_valid():
                repairOrder_update_form.save()
                messages.success(
                    request, f'{username}, Your Order Have Been Successfully Updated!')
                return redirect('profile')

        else:
            repairOrder_update_form = RepairOrderForm(instance=order_instance)
        context = {
            'page_tittle': page_tittle,
            'repairOrder_update_form': repairOrder_update_form
        }
        return render(request, 'repairsquad_home_app/repairOrderUpdate.html', context)
    else:
        print("NO")
        messages.warning(
            request, f'{username}, You Do Not Have Access To This!!!')
        return redirect('profile')
