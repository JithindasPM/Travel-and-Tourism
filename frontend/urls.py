from django.urls import path
from frontend import views
from frontend.views import Booking_Delete_View

urlpatterns=[
    # path('Homepage/',views.Homepage,name="Homepage"),
    path('Checkout_page/<int:p_id>',views.Checkout_page,name="Checkout_page"),
    path('User_details/<int:pk>/',views.User_details,name="User_details"),


    path('Singlepage/<int:id>',views.Singlepage,name="Singlepage"),
    path('Destination_single/<int:id>',views.Destination_single,name="Destination_single"),
    path('Final_destination/<int:id>',views.Final_destination,name="Final_destination"),
    path('signup',views.RegistrationView.as_view(),name="Signup"),
    path('login/', views.SignInView.as_view(), name="login"),
    path('logout/',views.signout_view,name="logout"),
    path('success/<int:pk>/',views.success, name="success"),
    path('feedback/',views.feedback,name="feedback"),
    path('booking_delete/<int:pk>',Booking_Delete_View.as_view(),name="booking_delete"),


]
