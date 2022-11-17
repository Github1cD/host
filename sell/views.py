from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .forms import verify_mobile_number,Add_product
from .models import Seller,Products
from django.contrib.auth.decorators import login_required


# Create your views here.
User = get_user_model()

def sell(request):
    return render(request,'sell.html')

@login_required
def verify_mobile(request):
    form = verify_mobile_number(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            user = User.objects.get(id=request.user.id)
            seller_id = 100+request.user.id
            obj = Seller.objects.create(
                seller_id = seller_id,
                user = user,
                mobile = mobile,
            )
            obj.save()
            
            return HttpResponse('seller page')
    return render(request,'mobile.html',{'form':form})

@login_required
def add_product(request):
    form = Add_product(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            image = form.cleaned_data.get('product_image')
            name = form.cleaned_data.get('product_name')
            description = form.cleaned_data.get('description')
            quantity = form.cleaned_data.get('total_quantity')
            price = form.cleaned_data.get('price')
            seller_id = (request.user.id)+100
            seller = Seller.objects.get(seller_id=seller_id)
            obj = Products.objects.create(
                product_name = name,
                product_image = image,
                description = description,
                total_quantity = quantity,
                seller = seller,
                price = price,
            )
            obj.save()             
            return redirect('/')
        form.non_field_errors()
        field_errors = [(field.label, field.errors) for field in form]
        print(field_errors)
        return HttpResponse('error in the form')
    
    return render(request, 'addproduct.html',{'form':form})