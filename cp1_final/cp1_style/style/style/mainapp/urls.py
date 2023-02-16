"""style URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from mainapp.views import door_page, cody_page, review_page,info,reco_result,reco_page, thnk

app_name = "mainapp"



urlpatterns = [
    path('',door_page, name='door_page'),
    path('info/',info,name='info'),
    path('cody/',cody_page, name='cody_page'),
    path('review/', review_page, name="review_page"),
    path('reco/',reco_page,name='reco_page'),
    path('reco/result', reco_result, name="reco_result"),
    path('review/thankyou',thnk,name='thnk'),
]
