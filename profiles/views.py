from http.client import HTTPResponse
# for mail
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail


from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .forms import Registration, Loginform, PasswordResetForm
from .models import Location,Qr_login
from django.contrib import messages
from .geopymod import locate,Find_distance
from .qrcodemod import Qr
from hashlib import sha256 as sha
import smtplib, ssl

from sell.models import Products


User = get_user_model()
url = '127.0.0.1:8000/'

def index(request):
    products = Products.objects.all()
    users = User.objects.all()
    return render(request,'home.html',{'products':products,'users':users})

def RegistrationForm(request, *args, **kwargs):
    form = Registration(request.POST or None)
    if request.method == 'POST':
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            village = form.cleaned_data.get('village')
            mandal = form.cleaned_data.get('mandal')
            district = form.cleaned_data.get('district')
            state = form.cleaned_data.get('state')
            country = form.cleaned_data.get('country')
            pin = form.cleaned_data.get('pin')
            user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
            user.save()
            obj = locate(village, mandal, district, state, country, pin)

            lat , lon = obj.lat_lon()
            loc = Location.objects.create(user=user,village=village,mandal=mandal,district=district,state=state,country=country,pin = pin,latitude= lat,longitude = lon)
            loc.save()
            
                
            return redirect('accounts/login/')
        else:
            return render(request,'registration.html',{'form':form})
            
    else:    
        return render(request,'registration.html',{'form':form})
    
def login_view(request):
    form = Loginform(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request,username=username,password=password)
            if user != None:
                auth.login(request,user)
                #return HTTPResponse('!!you are logged in successfully')
                return redirect('/')
            else:
                messages.info(request,'invalid username or password')
                return render(request,'login.html',{'form':form,})
    else:
        return render(request,'login.html',{'form':form})


def logout_view(request):
    auth.logout(request)
    return redirect('/')

#method for

def qr_login(request, key=None):
    if key == None:
        messages.info(request,'invalid qrcode user your credentials instead')
        return render(request,'login.html')
    else:
        kobj = Qr_login.objects.get(key = key)
        uobj = User.objects.get(id= kobj.user_id)
        #user = auth.authenticate(request,username=uobj.username, password = uobj.password)
        if uobj != None:
            auth.login(request,uobj)
            return redirect('/')
        else:
            
            return redirect('/')
        

#testing Find_distance code in geopymod.py
@login_required
def find_distance(request):
    cus =  Location.objects.get(user_id=request.user.id)
    users = Location.objects.all()
    out = {}
    for user in users:
        if user.user_id != cus.user_id:
            dobj = Find_distance(cus.latitude,cus.longitude,user.latitude,user.longitude)
            dis = dobj.distance()
            out[(User.objects.get(id=user.user_id)).username] =dis

    return render(request,'home.html',{'distance':out})

@login_required
def qr(request):
    qobj = Qr_login.objects.get(user_id=request.user.id)
    pattern = url+qobj.key
    gen = Qr()
    img = gen.gen_qr(pattern)
    return render(request,'home.html',{'img':img})



# need to update in the future
def password_reset_request(request):
    password_reset_form = PasswordResetForm(request.POST or None)
    if request.method == "POST":
        
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'vamseed123@gmail.com' , [user.email])
                    except Exception as e:
                        messages.info(request,e)
                        return render(request,'404.html')
                    return redirect("/password_reset/done/")
            else:
                messages.info(request,'Invalid email there is no account with that mail address')
                return render(request,"password_reset.html", {"password_reset_form":password_reset_form})
   
    return render(request, "password_reset.html",{"password_reset_form":password_reset_form})
    
# resetting the password

