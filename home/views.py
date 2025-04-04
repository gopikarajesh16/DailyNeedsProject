from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .models import Products,Category
from django.contrib.auth.decorators import login_required
from .forms import ProductsForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Categoryserializer,Productsserializer
from .models import Products
from .forms import ProfileUpdateForm
import json
from django.contrib import messages
from .models import Profile  
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Products
from django.shortcuts import get_object_or_404
from .models import Order  # Add this line







def homefn(request):
    return render(request, 'home.html')  # Ensure correct template is loaded

# @login_required(login_url='/login')
# def profilefn(request):
#     c=Products.objects.filter(us=request.user)
#     return render(request,'profile.html',{'pro':c})

@login_required(login_url='/login')
def profilefn(request):
    profile, created = Profile.objects.get_or_create(us=request.user)  # ✅ Ensuring correct field name
    form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  

    return render(request, 'profile.html', {'form': form, 'profile': profile})

# @login_required(login_url='/login')
# def productfn(request):
#     c=Products.objects.all()
#     g=Category.objects.all()
#     return render(request,'products.html',{'pro':c,'cat':g})

# def productfn(request):
#     c = Products.objects.all()
#     g = Category.objects.all()
    
#     # Ensure price is always a float
#     for product in c:
#         try:
#             product.price = float(product.price)  # Convert price to float
#         except (ValueError, TypeError):
#             product.price = 0.00  # Default to 0.00 if conversion fails
    
#     return render(request, 'products.html', {'pro': c, 'cat': g})
from django.db.models import Avg,Count

# def productfn(request):
#     c = Products.objects.all().annotate(avg_rating=Avg('order__rating'))  # Calculate average rating
#     g = Category.objects.all()
    
#     for product in c:
#         try:
#             product.price = float(product.price)  # Ensure price is float
#         except (ValueError, TypeError):
#             product.price = 0.00  # Default to 0.00 if conversion fails
    
#     return render(request, 'products.html', {'pro': c, 'cat': g})

def productfn(request):
    c = Products.objects.all().annotate(
        avg_rating=Avg('order__rating'),  # Calculate average rating
        rating_count=Count('order__rating')  # Count number of ratings
    )
    g = Category.objects.all()
    
    for product in c:
        try:
            product.price = float(product.price)  # Ensure price is float
        except (ValueError, TypeError):
            product.price = 0.00  # Default to 0.00 if conversion fails
    
    return render(request, 'products.html', {'pro': c, 'cat': g})

def categoryfn(request,p_id):
    g=Category.objects.all()
    c=Products.objects.filter(ctry=p_id)
    return render(request,'products.html',{'pro':c,'cat':g})

def viewproductfn(request,p_id):
    r=Products.objects.get(id=p_id)
    return render(request,'viewproduct.html',{'abc':r})


def formfn(request):
    return render(request,'form.html')


    
def addfn(request):
    a = request.GET['number1']
    b = request.GET['number2']
    c = int(a)+int(b)
    return render(request,'result.html',{'r':c})
    
    
def registerfn(request):
    return render(request,'register.html')


def saveuserfn(request):
    if request.method == "POST":
        u = request.POST.get('uname', '').strip()
        e = request.POST.get('email', '').strip()
        f = request.POST.get('fname', '').strip()
        l = request.POST.get('lname', '').strip()
        p1 = request.POST.get('psw1', '')
        p2 = request.POST.get('psw2', '')
        is_farmer = request.POST.get('is_farmer', 'off')  # Default 'off' if not checked

        if p1 != p2:
            return render(request, 'register.html', {'er': "Passwords do not match"})

        try:
            user = User.objects.create_user(username=u, first_name=f, last_name=l, email=e, password=p1)


            profile, created = Profile.objects.get_or_create(us=user)
            profile.is_farmer = (is_farmer == 'on')  
            profile.save()

            return redirect('/login')

        except IntegrityError:
            return render(request, 'register.html', {'er': "Username already exists. Try another one."})

    return render(request, 'register.html')


def loginfn(request):
    if request.method == 'POST': 
        u = request.POST.get('uname')  
        p1 = request.POST.get('psw1')  

        user = auth.authenticate(username=u, password=p1)  

        if user:  
            auth.login(request, user)  
            profile = Profile.objects.filter(us=user).first()  

            if profile and profile.is_farmer:  
                return redirect('/product') 
            else:
                return redirect('/user/products/') 
        
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'login.html')

    return render(request, 'login.html')









def logoutfn(request):
    auth.logout(request)
    return redirect('/login')



@login_required
def addproductsfn(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('details', '').strip()
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category') 

        if not desc:
            desc = "No description provided."

        try:
            category = Category.objects.get(id=category_id)  
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect('addproducts')

        if name and price:
            product = Products(name=name, details=desc, price=price, image=image, farmer=request.user, ctry=category)
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('/product/')  




    categories = Category.objects.all()  
    return render(request, 'addproducts.html', {'categories': categories})







def editproductfn(request, p_id):
    p = Products.objects.get(id=p_id)
    
    if request.method == 'POST':
        f = ProductsForm(request.POST, request.FILES, instance=p)
        if f.is_valid():
            f.save()
            return redirect('/product')
    else:
        f = ProductsForm(instance=p)
    
    return render(request, 'editproduct.html', {'form': f})




def deleteproductfn(request,p_id):
    if request.method=='POST':
        p=Products.objects.get(id=p_id)
        p.delete()
        return redirect('/product')
    else:
        return render(request,'deleteproduct.html')

def searchfn(request):
    o=request.GET['ghi']
    g=Category.objects.all()
    c=Products.objects.filter(name__icontains=o)
    return render(request,'products.html',{'pro':c,'cat':g})


def newapifn(request):
    return render(request,'newpage.html')


@api_view(['GET'])
def viewcategoryapi(request):
    g=Category.objects.all()
    z = Categoryserializer(g,many=True)
    return Response(z.data)



@api_view(['GET'])   
def apiproducts(request):
    g=Products.objects.all()
    c= Productsserializer(g,many=True)
    return Response(c.data)


@api_view(['GET'])
def apiproductsview(request,pid):
    g=Products.objects.get(id=pid)
    c = Productsserializer(g,many=False)
    return Response(c.data)




def checkout(request):
    if request.method == "POST":
        cart_data = request.POST.get("cart_data")  # Get cart data from form
        cart = json.loads(cart_data)  # Convert JSON string to dictionary
        return render(request, "checkout.html", {"cart": cart})





def success(request):
    return render(request, 'success.html')

def cart_view(request):
    cart = request.session.get("cart", {})  # Get cart from session (or empty dict if not set)
    
    total_price = sum(product["price"] * product["quantity"] for product in cart.values())

    return render(request, "cart.html", {"cart": cart, "total_price": total_price})






def cart_view(request):
    items = Item.objects.all()
    total_amount = calculate_total_amount()
    
    return render(request, 'cart.html', {'items': items, 'total_amount': total_amount})


@login_required
def checkout(request):
    if request.method == "POST":
        cart_data = request.POST.get("cart_data")  # Get cart JSON from hidden input
        import json
        cart = json.loads(cart_data)  # Convert JSON to Python dict
        
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect("products")

        # Create an order for each product in the cart
        for product_id, item in cart.items():
            try:
                product = Products.objects.get(id=product_id)  # Get product from DB
                Order.objects.create(
                    user=request.user,  # Customer placing the order
                    product=product,
                    quantity=item["quantity"],
                    total_price=float(item["price"]) * int(item["quantity"])
                )
            except Products.DoesNotExist:
                messages.error(request, f"Product {item['name']} not found.")
                continue

        messages.success(request, "Your order has been placed successfully!")
        return redirect("success")  # Redirect to success page after placing the order

    return redirect("products")  # If accessed via GET, go back to products


@login_required
def profile_update(request):
    profile = request.user.profile  # Get the logged-in user's profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving

    else:
        form = ProfileUpdateForm(instance=profile)  # Pre-fill form with current data

    return render(request, 'profile_update.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

@login_required
def profile_view(request):
    profile = request.user.profile  # Get the user's profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to refresh the profile page

    else:
        form = ProfileUpdateForm(instance=profile)  # Pre-fill the form

    return render(request, 'profile.html', {'form': form})
@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by("-order_date")  # Show latest orders first

    return render(request, "orders.html", {"orders": user_orders})



@login_required
def profile_view(request):
    profile = request.user.profile  # Get the logged-in user's profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to reload the page with updated data

    else:
        form = ProfileUpdateForm(instance=profile)  # Pre-fill form with current data

    return render(request, 'profile.html', {'form': form})

# @login_required
# def farmer_orders(request):


#     orders = Order.objects.filter(product__farmer=request.user)
#     return render(request, "farmer_orders.html", {"orders": orders})

@login_required
def farmer_orders(request):
    # Ensure the logged-in user is the farmer of the product
    orders = Order.objects.filter(product__farmer=request.user).order_by("-order_date")

    return render(request, "farmer_orders.html", {"orders": orders})



    from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Order

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.product.farmer != request.user:  # Ensure only the farmer can update
        return HttpResponseForbidden("You are not allowed to update this order.")

    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()
    return redirect("farmer_orders")


@login_required
def rate_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        if 1 <= rating <= 5:  # Ensure rating is between 1 and 5
            order.rating = rating
            order.save()
    
    return redirect("orders")  # Redirect back to orders page
