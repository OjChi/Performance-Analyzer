from django.contrib import admin
from django.urls import path, include
from . import views

#import dash functions here
# from dashboard.dash_apps.finished_apps import simpleexample
#end dash functions

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('technicalanalysis/', views.technical_analysis, name="technicalanalysis"),
    path('home/', views.homeView, name="home"),
    path('about/', views.aboutView, name="about"),
    path('contact/', views.contactView, name="contact"),
    # path('crypto/', views.cryptoView, name="crypto"),
    path('<slug:company_tech>/', views.cryptoView, name="chart"),

]