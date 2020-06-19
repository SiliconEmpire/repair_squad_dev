from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
)
from repairsquad_home_app.models import (
    RepairOrderModel,
)

# Create your views here.

def registerView(request):
    page_tittle = 'Register'
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            username = reg_form.cleaned_data.get('username')
            user_email = reg_form.cleaned_data.get('email')
            messages.success(
                request, f'{username} Your account has been created! You are now able to log in')
            ############# thank you email to the registerered user ##############
            content = "Welcome To Repair Squad, NIGERIA'S NO 1 ONLINE GADGET REPAIR SERVICE...... Be sure your profile is up to date,  it will help us provide our services to you the best we can! "
            html_msg = render_to_string('repairsquad_home_app/email_templates/email.html', context={
                'username': username,
                'content': content,
            })
            send_mail(
                "REPAIR SQUAD NOTIFICATION",
                f"REPAIR SQUAD. Hello {request.user.username} Welcome To Repair Squad, NIGERIA'S NO 1 ONLINE GADGET REPAIR SERVICE...... Be sure your profile is up to date,  it will help us provide our services to you the best we can! ",
                settings.EMAIL_HOST_USER,
                [user_email],
                fail_silently=True,
                html_message=html_msg,
            )

            return redirect('login')
        else:
            for msg in reg_form.error_messages:
                messages.error(
                    request, f"{msg}: {reg_form.error_messages[msg]}")
    else:

        reg_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'reg_form': reg_form, 'page_tittle': page_tittle, })


@login_required
def profile(request):
    page_tittle = f'Hello {request.user.username}'
    repairOrder_qs = RepairOrderModel.objects.all().filter(
        owner=request.user).order_by('-order_date')
    page_obj = Paginator(repairOrder_qs, 2)
    context = {
        'page_tittle': page_tittle,
        'repairOrder_qs': repairOrder_qs,
        'page_obj':page_obj.page(1)
    }
    return render(request, 'users/profile.html', context)

class ProfileView(LoginRequiredMixin, ListView):
    model = RepairOrderModel
    template_name = 'users/profile.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'repairOrder_qs'
    paginate_by = 4

    def get_queryset(self):
        print("*************************************")
        print(self.request)
        user = get_object_or_404(User, username=self.request.user)
        return RepairOrderModel.objects.filter(owner=user).order_by('-order_date')

@login_required
def profile_update_view(request):
    page_tittle = "Profile Update"
    if request.method == 'POST':
        u_u_form = UserUpdateForm(request.POST, instance=request.user)
        p_u_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile)
        if u_u_form.is_valid() and p_u_form.is_valid():
            u_u_form.save()
            p_u_form.save()
            username = u_u_form.cleaned_data.get('username')
            messages.success(
                request, f' {username} Your profile has been updated!')
            # print("++++++++++++++++++++")
            # print(request.user)
            # print(request.user.profile.phone_number)
            return redirect('profile')
    else:
        u_u_form = UserUpdateForm(instance=request.user)
        p_u_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'page_tittle': page_tittle,
        'u_u_form': u_u_form,
        'p_u_form': p_u_form
    }
    return render(request, 'users/profile_update.html', context)