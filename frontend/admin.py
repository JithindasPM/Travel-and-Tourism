from django.contrib import admin
from frontend.models import state,destination,Package,Hotel,User_Details,Feedback,Booking

# Register your models here.
admin.site.register(state)
admin.site.register(destination)
admin.site.register(Package)
admin.site.register(Hotel)
admin.site.register(User_Details)
admin.site.register(Feedback)
admin.site.register(Booking)
