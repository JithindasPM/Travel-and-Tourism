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

]
