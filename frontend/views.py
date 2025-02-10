import django
from django.shortcuts import render,redirect
from frontend.models import state,destination,Package,Hotel,User_Details,Feedback
from .forms import RegistrationForm, LoginForm
from django.views.generic import View, FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User  # Import the User model
from django.shortcuts import render
from .models import User_Details
from django.contrib.auth.decorators import login_required

@login_required
def success(request,pk):
    # Filter User_Details based on the logged-in user
    detail = User_Details.objects.get(id = pk)
    return render(request, 'success.html', {'detail': detail})


# Create your views here.
def Homepage(request):
    x = state.objects.all()
    if request.user.is_authenticated:
        y= User_Details.objects.filter(user=request.user)
        return render(request,"Frontend_page.html",{'x':x,'Y':y})
    return render(request,"Frontend_page.html",{'x':x})

def Singlepage(request, id):
    y = destination.objects.filter(State=id)
    bg_img = state.objects.get(id=id).Image if state.objects.filter(id=id).exists() else None

    context = {
        'y': y,
        'bg_img': bg_img
    }

    return render(request, "single_page.html", context)

def Destination_single(request, id):
    z = Package.objects.filter(destination=id)
    bg_img = destination.objects.get(id=id).Image if destination.objects.filter(id=id).exists() else None


    context = {
        'z': z,
        'bg_img': bg_img
    }

    return render(request,"destination_single.html",context)

def Final_destination(request,id):
    a = Hotel.objects.filter(package=id)
    bg_img = Package.objects.get(id=id).Image if Package.objects.filter(id=id).exists() else None
    pkg=Package.objects.get(id=id)
   

    context = {
        'a': a,
        'bg_img': bg_img,
        'pkg':pkg
    }
    return render(request,"Final_destination.html",context)

def Checkout_page(request, p_id):
    hotel_id = request.GET.get('hotel_id')
    hotel = None
    if hotel_id:
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            # Handle the case where the hotel with the given ID does not exist
            pass
    print(hotel_id)
    pkg = Package.objects.get(id=p_id)
    calculated_amount = pkg.amount * 100
    
    # Fetch hotels associated with the package
    # hotels = Hotel.objects.get(id=hotel_id)

    return render(request, "checkout_page.html", {'pkg': pkg, 'calculated_amount': calculated_amount, 'hotels': hotel})

class RegistrationView(FormView):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'Signup.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration successfully")
            return redirect('login')
        messages.error(request,"Please enter correct details")
        return render(request, 'Signup.html', {"form": form})
  

class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'userlogin.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            psw = form.cleaned_data.get('password')
            usr = authenticate(request, username=uname, password=psw)
            if usr:
                login(request, usr)  
                messages.success(request, "Login successfully")

                if usr.is_superuser:
                    return redirect("dashboard")
                return redirect("Homepage")

        messages.error(request, "Invalid Userlogin")
        return render(request, 'userlogin.html', {"form": form, "messages": messages.get_messages(request)})

    
def signout_view(request, *args, **kwargs):
        logout(request)
        return redirect("Homepage")




def User_details(request,pk):
    if request.method == "POST":
        n = request.POST.get('name')
        s = request.POST.get('state')
        st = request.POST.get('street')
        t = request.POST.get('town')
        p = request.POST.get('phone')
        e = request.POST.get('email')
        d = request.POST.get('date')
        hotel_obj =Hotel.objects.get(id=pk)
        obj = User_Details.objects.create(U_Name=n,U_State=s,U_Street=st,U_Town=t,U_Phone=p,U_Email=e,package=hotel_obj.package,date=d,user=request.user,hotel=hotel_obj)
        obj.save()
        
        
        return redirect("success",pk=obj.id)
    
# Create Razorpay payment
    order_currency = 'INR'
    client = razorpay.Client(auth=('rzp_test_IzIBFTmzd3zzKk', 'mMvIdZd7a4EU1pMd9tSQEbE0'))

    payment = client.order.create({'amount': int(grand_total * 1000), 'currency': "INR", 'payment_capture': '1'})

def feedback(request):
    if request.method == "POST":
        na = request.POST.get('Name')
        ema = request.POST.get('email')
        feed = request.POST.get('feedback')
        obj = Feedback(Name=na, email=ema, feedback=feed)
        obj.save()
        return redirect('Homepage')