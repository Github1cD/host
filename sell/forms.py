from django import forms
from django.contrib.auth import get_user_model
from jsonschema import ValidationError

User = get_user_model()


class verify_mobile_number(forms.Form):
    mobile = forms.IntegerField(
        widget=forms.NumberInput()
    )
    
    def clean_mobile(self):
        num = self.cleaned_data.get('mobile')
        if len(str(num)) == 10:
            return num
        else:
            raise forms.ValidationError('invalid mobile number')
        
# adding product form
class Add_product(forms.Form):
    product_name = forms.CharField(
        label = 'Product Name',
        widget = forms.TextInput(
            attrs={}
        )
    )
    description = forms.CharField(
        label = 'description',
        widget = forms.TextInput(
        attrs={}
        )
    )
    total_quantity = forms.IntegerField(
        label = 'Quantity Available',
        widget = forms.TextInput(
        attrs={}
        )
    )
    price = forms.IntegerField(
        label = 'Price',
        widget = forms.TextInput(
        attrs={}
        )
    )
    product_image = forms.ImageField(
        label = 'upload the product image',
        widget = forms.FileInput(
            attrs={}
        )
    )
    
    def clean_product_image(self):
        image = self.cleaned_data.get('product_image')
        if image is None:
            return ValidationError('image error')

    
    
    