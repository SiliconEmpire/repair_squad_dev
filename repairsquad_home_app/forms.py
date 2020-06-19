from django import forms
from .models import QuickRepairOrderModel, RepairOrderModel


class QuickRepairOrderForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "+2348132450841 or 08132450841",
            }
        )
    )

    terms_and_condition = forms.BooleanField(
        required=True,
    )

    class Meta:
        model = QuickRepairOrderModel
        fields = ['name', 'phone_number', 'terms_and_condition']


class RepairOrderForm(forms.ModelForm):

    brand = forms.CharField(
        required=True,
            widget=forms.TextInput(
            attrs={
                "placeholder": " e.g DELL",
            }
        )

    )

    model = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Device model",
            }
        )
    )

    serial_no_or_IMEI = forms.CharField(
        required=True,
        label="Serial No/IMEI",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Device serial No/EMEI",
            }
        )
    )

    fault_details = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": " A detailed description of the fault",
            }
        )
    )

    pick_up_date = forms.DateField(
        required=True,
        # widget=forms.SelectDateWidget(

        #     attrs={
        #         # "class": "datepicker",
        #     }
        # )
    )

    coupon_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Got a coupon/voucher use it here and get a discount on your repair order",
            }
        )
    )

    survey = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "How did you hear about us",
            }
        )
    )

    terms_and_condition = forms.BooleanField(
        required=True,
        label=' I have read and agree to the'
    )

    class Meta:
        model = RepairOrderModel
        fields = [
            'device_type',
            'brand',
            'model',
            'serial_no_or_IMEI',
            'fault_details',
            'pick_up_date',
            'coupon_code',
            'survey',
            'terms_and_condition'
        ]
