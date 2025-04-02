

"""
URL configuration for myproject01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from home.views import *

from django.conf import settings
from django.conf.urls.static import static
# from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', homefn),
    path ('home/', homefn),
    path ('product/', productfn),
    path ('user/products/', productfn ),
    path ('formpage/', formfn),
    path ('add/', addfn), 
    # path ('viewproduct/<int:p_id>', viewproductfn),
    path('viewproduct/<int:p_id>/', viewproductfn, name='viewproduct'),
    path ('register/', registerfn),
    path ('saveuser/', saveuserfn),
    path ('login/',loginfn),
    path ('logout/',logoutfn),
    path ('addproduct/',addproductsfn),
    path ('editproduct/<int:p_id>',editproductfn),
    path ('deleteproduct/<int:p_id>',deleteproductfn),
    path ('category/<int:p_id>',categoryfn),
    path ('search/', searchfn),
    path ('new/', newapifn),
    path ('api-category/',viewcategoryapi),
    path ('api-products/',apiproducts),
    path ('api-products-view/<int:pid>',apiproductsview),
    path('profile/', profilefn, name='profile'),
    path('checkout/', checkout, name='checkout'),
    path('success', success, name='success'),
    path('addproduct/', addproductsfn, name='addproducts'),
    path("farmer/orders/", farmer_orders, name="farmer_orders"),
    path("order/<int:order_id>/update/", update_order_status, name="update_order_status"),
    path("orders/", orders, name="orders"),
    path("order/<int:order_id>/rate/", rate_order, name="rate_order"),
    
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) 

# urlpatterns += debug_toolbar_urls()
