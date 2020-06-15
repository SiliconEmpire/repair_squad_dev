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
        
    )

    model = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
            }
        )
    )

    serial_no_or_IMEI = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
            }
        )
    )

    fault_details = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "",
            }
        )
    )

    pick_up_address = forms.DateField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
            }
        )
    )

    pick_up_date = forms.CharField(
        required=True,
        widget=forms.SelectDateWidget()
    )

    coupon_code = forms.CharField(
        required=False,
    )

    survey = forms.CharField(
        required=False,
        help_text='How did you hear about us',
        widget=forms.Textarea(
            attrs={
                "placeholder": "",
            }
        )
    )

    terms_and_condition = forms.BooleanField(
        required=True,
        help_text='lorem epsum'
    )

    class Meta:
        model = RepairOrderModel
        fields = [
            'device_type',
            'brand',
            'model',
            'serial_no_or_IMEI',
            'fault_details',
            'pick_up_address',
            'pick_up_date',
            'coupon_code',
            'survey',
            'terms_and_condition'
        ]
