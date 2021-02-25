from django.contrib import admin
from django.urls import path
from . import views

app_name="GoCabs"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name="login"),
    path('',views.index,name="index"),
    path('signup/',views.signup,name="signup"),
    path('insval/',views.insval,name="insval"),
    path('dash/',views.dash,name="dash"),
    path('booked/',views.booked,name="booked"),
    path('cbooking/',views.cbooking,name="cbooking"),
    path('rides/',views.rides,name="rides"),
    path('reviews/',views.reviews,name="reviews"),
    path('tstatus/',views.tripstatus,name="tstatus"),
    path('error/',views.error,name="error")
]
