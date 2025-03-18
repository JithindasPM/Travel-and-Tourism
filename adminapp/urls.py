from django.urls import path,include
from frontend import views

from adminapp.views import Admin_Dashboard_View
from adminapp.views import State_Add_View
from adminapp.views import State_Update_View
from adminapp.views import State_Delete_View
from adminapp.views import Destination_Add_View
from adminapp.views import Destination_Update_View
from adminapp.views import Destination_Delete_View
from adminapp.views import Package_Add_View
from adminapp.views import Package_Update_View
from adminapp.views import Pakage_Delete_View
from adminapp.views import Admin_Registration_View
from adminapp.views import Package_Details_View
from adminapp.views import Hotel_Add_View
from adminapp.views import Hotel_Update_View
from adminapp.views import Hotel_Delete_View
from adminapp.views import Hotel_Details_View
from adminapp.views import DeleteAllBookingsView
from adminapp.views import User_Details_View




urlpatterns=[

    path('dashboard/',Admin_Dashboard_View.as_view(),name="dashboard"),
    path('state_add/',State_Add_View.as_view(),name="state_add"),
    path('state_update/<int:pk>',State_Update_View.as_view(),name="state_update"),
    path('state_delete/<int:pk>',State_Delete_View.as_view(),name="state_delete"),
    path('destination/',Destination_Add_View.as_view(),name="destination"),
    path('destination_update/<int:pk>',Destination_Update_View.as_view(),name="destination_update"),
    path('destination_delete/<int:pk>',Destination_Delete_View.as_view(),name="destination_delete"),
    path('package/',Package_Add_View.as_view(),name="package"),
    path('package_update/<int:pk>',Package_Update_View.as_view(),name="package_update"),
    path('package_delete/<int:pk>',Pakage_Delete_View.as_view(),name="package_delete"),
    path('admin_registration/',Admin_Registration_View.as_view(),name="admin_registration"),
    path('package_details/<int:pk>',Package_Details_View.as_view(),name="package_details"),
    path('hotel/',Hotel_Add_View.as_view(),name="hotel"),
    path('hotel_update/<int:pk>',Hotel_Update_View.as_view(),name="hotel_update"),
    path('hotel_delete/<int:pk>',Hotel_Delete_View.as_view(),name="hotel_delete"),
    path('hotel_details/<int:pk>',Hotel_Details_View.as_view(),name="hotel_details"),
    path('delete-all-bookings/', DeleteAllBookingsView.as_view(), name='delete_all_bookings'),
    path('user_details/<int:pk>',User_Details_View.as_view(),name="user_details"),

]
