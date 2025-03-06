from django.shortcuts import render,redirect
from django.views.generic import View
from django.views.generic import FormView
from django.contrib import messages
from django.db.models import Sum


from frontend.models import state
from frontend.models import destination
from frontend.models import Package
from frontend.models import User
from frontend.models import User_Details
from frontend.models import Hotel
from frontend.models import Booking

from adminapp.forms import State_Form
from adminapp.forms import Destination_Form
from adminapp.forms import Package_Form
from adminapp.forms import Admin_Registration_Form
from adminapp.forms import Hotel_Form

# Create your views here.

# class Admin_Dashboard_View(View):
#     def get(self,request,*args,**kwargs):
#         id=request.user.id
#         # Get hotels created by the logged-in admin
#         admin_hotels = Package.objects.filter(user=id)
#         # Get bookings for those hotels
#         admin_bookings = User_Details.objects.filter(package__in=admin_hotels).order_by('-id')
#         # totel_revenue=admin_bookings
#         total_amount = admin_bookings.aggregate(total_amount=Sum('package__amount'))['total_amount']
#         total_booking=admin_bookings.count()
#         destinations = admin_bookings.values('package').distinct().count()
#         users = admin_bookings.values('U_Name').distinct().count()
#         return render(request,'admin.html',{'admin_bookings':admin_bookings,'total_booking':total_booking,'total_amount':total_amount,'users':users,'destinations':destinations})

class DeleteAllBookingsView(View):
    def get(self, request, *args, **kwargs):
        Booking.objects.all().delete()
        return redirect('Homepage') 

from django.db.models import Sum

class Admin_Dashboard_View(View):
    def get(self, request, *args, **kwargs):
        id = request.user.id

        # Get packages created by this admin
        admin_packages = Package.objects.filter(user=id)

        # Get bookings related to these packages
        admin_bookings = Booking.objects.filter(package__in=admin_packages).order_by('-id')

        # Total booking count
        total_booking = admin_bookings.count()

        # Unique destinations from the packages booked
        destinations = admin_bookings.values('package').distinct().count()

        # Unique users who booked
        users = admin_bookings.values('user').distinct().count()

        # Total revenue from the 'total_amount' field in the Booking model
        total_amount = admin_bookings.aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0

        return render(request, 'admin.html', {
            'admin_bookings': admin_bookings,
            'total_booking': total_booking,
            'total_amount': total_amount,
            'users': users,
            'destinations': destinations
        })


class State_Add_View(View):
    def get(self,request,*args,**kwargs):
        form=State_Form()
        datas=state.objects.all()
        return render(request,'state.html',{'form':form,'datas':datas})
    def post(self,request,*args,**kwargs):
        form=State_Form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        datas=state.objects.all()
        form=State_Form()
        return render(request,'state.html',{'form':form,'datas':datas})
    
class State_Update_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=state.objects.get(id=id)
        form=State_Form(instance=data)
        datas=state.objects.all()
        return render(request,'state.html',{'form':form,'datas':datas,'data':data})

    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=state.objects.get(id=id)
        form=State_Form(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
        return redirect('state_add')

class State_Delete_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        state.objects.get(id=id).delete()
        return redirect('state_add')


class Destination_Add_View(View):
    def get(self,request,*args,**kwargs):
        form=Destination_Form()
        datas=destination.objects.all()
        return render(request,'destination.html',{'form':form,'datas':datas})
    def post(self,request,*args,**kwargs):
        form=Destination_Form(request.POST,request.FILES)
        if form.is_valid():
            destination.objects.create(**form.cleaned_data,user=request.user)
        datas=destination.objects.all()
        form=Destination_Form()
        return render(request,'destination.html',{'form':form,'datas':datas})

class Destination_Update_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=destination.objects.get(id=id)
        form=Destination_Form(instance=data)
        datas=destination.objects.all()
        return render(request,'destination.html',{'form':form,'datas':datas,'data':data})

    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=destination.objects.get(id=id)
        form=Destination_Form(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
        return redirect('destination')
    
class Destination_Delete_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        destination.objects.get(id=id).delete()
        return redirect('destination')
    
class Package_Add_View(View):
    def get(self,request,*args,**kwargs):
        form=Package_Form()
        datas=Package.objects.all()
        return render(request,'package.html',{'form':form,'datas':datas})
    def post(self,request,*args,**kwargs):
        form=Package_Form(request.POST,request.FILES)
        if form.is_valid():
            Package.objects.create(**form.cleaned_data,user=request.user)
        datas=Package.objects.all()
        form=Package_Form()
        return render(request,'package.html',{'form':form,'datas':datas})

class Package_Update_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Package.objects.get(id=id)
        form=Package_Form(instance=data)
        datas=Package.objects.all()
        return render(request,'package.html',{'form':form,'datas':datas,'data':data})

    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Package.objects.get(id=id)
        form=Package_Form(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
        return redirect('package')

class Pakage_Delete_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Package.objects.get(id=id).delete()
        return redirect('package')


class Admin_Registration_View(View):
    def get(self, request, *args, **kwargs):
        form = Admin_Registration_Form()
        return render(request, "admin_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = Admin_Registration_Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.is_superuser = True
            user.is_staff = True
            user.set_password(form.cleaned_data["password1"]) 
            user.save() 

            messages.success(request, "Registration successful!")
            return redirect("login") 
        
        messages.error(request, "Please enter correct details.")
        return render(request, "admin_form.html", {"form": form})
    
class Package_Details_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Package.objects.get(id=id)
        return render(request,'package_detail.html',{'data':data})
    


class Hotel_Add_View(View):
    def get(self,request,*args,**kwargs):
        form=Hotel_Form()
        datas=Hotel.objects.all()
        return render(request,'hotel.html',{'form':form,'datas':datas})
    def post(self,request,*args,**kwargs):
        form=Hotel_Form(request.POST,request.FILES)
        if form.is_valid():
            Hotel.objects.create(**form.cleaned_data,user=request.user)
        datas=Hotel.objects.all()
        form=Hotel_Form()
        return render(request,'hotel.html',{'form':form,'datas':datas})

class Hotel_Update_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Hotel.objects.get(id=id)
        form=Hotel_Form(instance=data)
        datas=Hotel.objects.all()
        return render(request,'hotel.html',{'form':form,'datas':datas,'data':data})

    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Hotel.objects.get(id=id)
        form=Hotel_Form(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
        return redirect('hotel')

class Hotel_Delete_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Hotel.objects.get(id=id).delete()
        return redirect('hotel')

class Hotel_Details_View(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Hotel.objects.get(id=id)
        return render(request,'hotel_detail.html',{'data':data})


    