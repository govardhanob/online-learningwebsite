"""
URL configuration for Classroomproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Classroomapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',views.index),
    path('',views.profile),
    path('register',views.register),
    path('loginn',views.loginn),
    path('registering',views.registering),
    path('forgot',views.forgot),
    path('updatepassword',views.updatepswd),
    path('updatedpswd',views.updatedpswd),
    path('loggingin',views.loggingin),
    path('profile<email>',views.profile),
    path('teach<email>',views.teach),
    path('teachsecond/<int:cid>',views.teach2,name='teachsecond'),
    path('adddetails',views.adddetails),
    path('addcontent',views.addcontent),
    path('fullclass',views.fullclass),
    path('fullclassteacher<cid>',views.fullclassteacher),
    path('mycourses<email>',views.teach3),
    path('updatecontent',views.updatecontent),
    path('editcontent',views.editcontent),
    path('signout',views.signout),
    path('updatedetails',views.updatedetails),
    path('deletecontent',views.deletecontent),
    path('updateprofile',views.updateprofile),
    path('updatedp',views.updatedp),
    path('updateuserdetails',views.updateuserdetails),
    path('mylearning',views.mylearning),
    path('mycart',views.mycart),
    path('addingcart',views.addingcart),
    path('deletingcart<cid>',views.deletingcart),
    path('whishlist',views.whishlist),
    path('addingwhishlist<cid>',views.addingwhishlist),
    path('deletingwhishlist<cid>',views.deletingwhishlist),
    path('payment',views.payment),
    path('paying',views.paying),
    path('rating',views.rating),
    path('search',views.sreach),
    path('adminpage',views.adminpage,name='adminpage'),
    path('course',views.adminpagecourse),
    path('billing',views.adminpagebilling),
    path('adminprofile',views.adminprofile),
    path('adminsignout',views.adminsignout),
    path('adminprofileupdate',views.adminprofileupdate),
    path('adminrating',views.adminrating),
    path('deleteuser<email>',views.deleteuser),
    path('deletecourse<id>',views.deletecourse),
    path('warningmail<email>',views.warningmail),
    path('coursesales<cid>',views.coursesales)

    

]


if settings.DEBUG==True:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)