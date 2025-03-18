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
from frontend.models import Booking
from django.views.generic import View

@login_required
def success(request,pk):
    # Filter User_Details based on the logged-in user
    detail = User_Details.objects.get(id = pk)
    spot=detail.package.spot
    booking=Booking.objects.get(user_deatil=detail.id)
    return render(request, 'success.html', {'detail': detail,'spot':spot,'booking':booking})


# Create your views here.
def Homepage(request):
    x = state.objects.all()
    if request.user.is_authenticated:
        y= User_Details.objects.filter(user=request.user)
        return render(request,"Frontend_page.html",{'x':x,'Y':y})
    return render(request,"Frontend_page.html",{'x':x})

class Booking_Delete_View(View):
    def get(self,request,*args,**Kwargs):
        id=Kwargs.get('pk')
        User_Details.objects.get(id=id).delete()
        return redirect('Homepage')

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
    pkg = Package.objects.get(id=p_id)
    
    calculated_amount = pkg.amount * 100
    
    # Fetch hotels associated with the package
    # hotels = Hotel.objects.get(id=hotel_id)

    return render(request, "checkout_page.html", {'pkg': pkg, 'calculated_amount': calculated_amount, 'hotels': hotel})

# class RegistrationView(FormView):
#     def get(self, request, *args, **kwargs):
#         form = RegistrationForm()
#         return render(request, 'Signup.html', {"form": form})

#     def post(self, request, *args, **kwargs):
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"registration successfully")
#             return redirect('login')
#         messages.error(request,"Please enter correct details")
#         return render(request, 'Signup.html', {"form": form})

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import RegistrationForm
from django.contrib.auth.models import User

class RegistrationView(FormView):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'Signup.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user after the form is validated
            user = form.save()

            # Send a confirmation email
            self.send_confirmation_email(user)

            # Show success message
            messages.success(request, "Registration successful.")
            return redirect('login')
        
        # Show error message if form is not valid
        messages.error(request, "Please enter correct details.")
        return render(request, 'Signup.html', {"form": form})

    def send_confirmation_email(self, user):
        subject = 'Registration Successful - Welcome to Paradise Found'
        message = f"""
        Dear {user.username},

        Welcome to Paradise Found!

        Thank you for registering with us. We are excited to have you on board. 
        You can now log in and start exploring all the amazing features we offer.

        If you have any questions or need assistance, feel free to reach out to our support team.

        Best regards,
        The Paradise Found Team
        """
        from_email = settings.EMAIL_HOST_USER  # Use the email defined in your settings
        recipient_list = [user.email]

        # Send plain-text email
        send_mail(subject, message, from_email, recipient_list)

  

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

                if usr.is_superuser:
                    return redirect("dashboard")
                return redirect("Homepage")

        messages.error(request, "Invalid Userlogin")
        return render(request, 'userlogin.html', {"form": form, "messages": messages.get_messages(request)})


    
def signout_view(request, *args, **kwargs):
        logout(request)
        return redirect("Homepage")


from django.core.mail import send_mail
from django.conf import settings

def User_details(request, pk):
    if request.method == "POST":
        n = request.POST.get('name')
        s = request.POST.get('state')
        st = request.POST.get('street')
        t = request.POST.get('town')
        p = request.POST.get('phone')
        e = request.POST.get('email')
        d = request.POST.get('date')
        travel=request.POST.get('travel_way')
        aadhar_file = request.FILES.get('aadhar')
        

        hotel_obj = Hotel.objects.get( id=pk)
        
        obj = User_Details.objects.create(
            U_Name=n,
            U_State=s,
            U_Street=st,
            U_Town=t,
            U_Phone=p,
            U_Email=e,
            package=hotel_obj.package,
            date=d,
            user=request.user,
            hotel=hotel_obj,
            travel_way=travel,
            U_Aadhar=aadhar_file
        )
        obj.save()

        subject = 'Welcome to Paradise Found'
        message =f"Dear {request.user.username},\n\n" f"Congratulations! Your booking at {hotel_obj.hotel_name} has been successfully confirmed. We are delighted to welcome you on {d} and ensure you have an unforgettable experience. \n We are delighted to welcome you on {d} and ensure you have an unforgettable experience. \n We look forward to serving you at {hotel_obj.hotel_name} and making your trip truly memorable! 🌴✨"

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e,]
        send_mail(subject, message, email_from, recipient_list)

        # Razorpay Payment Integration
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_IzIBFTmzd3zzKk', 'mMvIdZd7a4EU1pMd9tSQEbE0'))
        
        grand_total = hotel_obj.package.amount  # Ensure this value is fetched correctly
        
        if travel == 'Bike':
            extra_charge = 799
            grand_total += extra_charge
        elif travel == 'Car':
            extra_charge = 1499
            grand_total += extra_charge
        user = User_Details.objects.get(id=obj.id)
        book=Booking.objects.create(hotel=hotel_obj, user=request.user, total_amount=grand_total, package=hotel_obj.package,user_deatil=user)

        payment = client.order.create({
            'amount': int(grand_total * 100),  # Convert to paise (100 paise = 1 INR)
            'currency': order_currency,
            'payment_capture': '1'
        })

        return redirect("success", pk=obj.id)

def feedback(request):
    if request.method == "POST":
        na = request.POST.get('Name')
        ema = request.POST.get('email')
        feed = request.POST.get('feedback')
        obj = Feedback(Name=na, email=ema, feedback=feed)
        obj.save()
        return redirect('Homepage')