"""testymolo URL Configuration

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
from django.contrib import admin
from django.urls import path
from datamolo import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path('', views.Main.index, name='index'),
    path('new-session/', views.Main.new_session, name="new-session"),
    path('load-figure/', views.Main.load_mainfigure_protein, name="load-figure" ),
    path('minus-figure/', views.Main.load_minusfigure_protein, name="minus-figure" ),
    path('plus-figure/<int:protein_id>/', views.Main.load_plusfigure_protein, name="plus-figure" ),
    path('module/<int:subseq_id>/', views.Main.load_card_module, name="module" ),
    path('profile/<int:profile_id>/', views.Main.load_mainfigure_profile, name="profile"),
    path('check_logo/', views.Main.check_mainfigure_logo, name="check-logo"),
    #path('load-logo/<str:temp_id>/', views.Main.load_mainfigure_logo, name="load-logo"),
    path('download/', views.Main.download, name='download'),
] 
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
