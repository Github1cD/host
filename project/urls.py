"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static  
from django.contrib import admin
from django.urls import path,include,re_path

from django.contrib.auth import views as auth_views
from sell.views import(
    verify_mobile,
    sell,
    add_product,
)

from profiles.views import (
    RegistrationForm,
    login_view,
    index,
    logout_view,
    qr_login,
    find_distance,
    qr,
    password_reset_request,
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',RegistrationForm),
    path('accounts/login/',login_view),
    path('accounts/logout/',logout_view),
    path('distance',find_distance),
    path('qr',qr),
    
    re_path(r'qr_login/(?P<key>\w+)/$',qr_login),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/login/register/',RegistrationForm),
    #path('accounts/register/login/',login_view),
    
    #mail
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),   
    path('password-reset', password_reset_request),
    
    #add product
    path('sell/add-product',add_product),
    
    #sell
    path('sell',sell),
    path('verify-mobile-number/',verify_mobile),
    
    path('',index),
    path("__reload__/", include("django_browser_reload.urls")),
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
