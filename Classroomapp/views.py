from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
import random
from .models import *
from django.contrib.auth.models import User
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from django.db.models import Sum
from django.contrib.sessions.models import Session
import stripe
from django.conf import settings
import re
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
def index(request):
    request.session.flush()
    return render(request,'index.html')
    


def register(request):
    return render(request,'register.html')


def loginn(request):
    return render(request,'login.html')


def registering(request):
    if request.method=='POST':
        fullname=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        repassword=request.POST['repassword']
        if Userdetails.objects.filter(email=email).exists():
            messages.info(request,'user already exists')
            return redirect(register)
        if User.objects.filter(email=email, is_superuser=True).exists():
            messages.info(request,'user already exists')
            return redirect(register)
            
        if password==repassword:
            pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
            regex = re.compile(pattern)
            if regex.match(password):
                z=Userdetails.objects.create(fullname=fullname,email=email,password=password)
                z.save()
                return redirect(loginn)
            else:
                messages.info(request,'password is not strong')
                return redirect(register)

        else:
            messages.info(request,'Re entered password is not same')
            return redirect(register)
            
      
           
        
           
def forgot(request):
    return render(request,'forgot.html')


def otpgenerate():
      return random.randint(1001,9999)


def send_otp_email(receiver_email, otp):
    sender_email = ""
    password = ""

    message = MIMEText(f'your OTP for Updating password is {otp}')
    message['Subject'] = "OTP Email"
    message['From'] = sender_email
    message['To'] = receiver_email
    server=None
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        
    except Exception as e:
        return HttpResponse("An Error  Occurred")
    finally:
        if server:
            server.quit()



def updatepswd(request):
     if request.method=='POST':
        email=request.POST['email']
     
        if Userdetails.objects.filter(email=email).exists(): 
            aa=otpgenerate()
            send_otp_email(email,aa)
            return render(request,'forgotpassword.html',{'a':email,'b':aa})
        if User.objects.filter(email=email, is_superuser=True).exists():
            aa=otpgenerate()
            send_otp_email(email,aa)
            return render(request,'forgotpassword.html',{'a':email,'b':aa})
        else:
            return redirect(loginn)
def updatedpswd(request):
    email1 = request.POST.get('email1')
    user_otp=request.POST['otp']
    real_otp=request.POST['otpp']
    password=request.POST['password']
    repassword=request.POST['password1']
    if User.objects.filter(email=email1).exists():
        if real_otp==user_otp:
            if password==repassword:
                u=User.objects.get(email=email1)
                u.set_password(password)
                u.save()
                request.session.flush()
                return redirect(loginn)
            else:
                messages.info(request,'Re entered password is incorrect')
                return render(request,'forgotpassword.html',{'a':email1,'b':real_otp})
        else:
            messages.info(request,'OTP is incorrect')
            return render(request,'forgotpassword.html',{'a':email1,'b':real_otp})
    else:
        if real_otp==user_otp:
            if password==repassword:
                u=Userdetails.objects.get(email=email1)
                u.password=password
                u.save()
                request.session.flush()
                return redirect(loginn)
            else:
                messages.info(request,'Re entered password is incorrect')
                return render(request,'forgotpassword.html',{'a':email1,'b':real_otp})
        else:
            messages.info(request,'OTP is incorrect')
            return render(request,'forgotpassword.html',{'a':email1,'b':real_otp})
def profile(request,email=''):
    
    if 'tid' in request.session:
        
        if email:
            user=Userdetails.objects.get(email=email)
            subjects=Coursedetails.objects.all().order_by('-date')
            cart=[i.courseid for i in Cart.objects.filter(usermail=email)]
            whishlist=[j.courseid for j in Whishlist.objects.filter(email=email)]
            mylearning=[z.courseid for z in Mylearnings.objects.filter(usermail=email)]
            deletedcourse=[i.courseid for i in Deletedcourse.objects.all()]
            return render(request,'profile.html',{'user':user,'s':subjects,'cart':cart,'whishlist':whishlist,'ml':mylearning,'dl':deletedcourse})
        else:
            email = request.session['tid']
            user=Userdetails.objects.get(email=email)
            subjects=Coursedetails.objects.all().order_by('-date')
            cart=[i.courseid for i in Cart.objects.filter(usermail=email)]
            whishlist=[j.courseid for j in Whishlist.objects.filter(email=email)]
            mylearning=[z.courseid for z in Mylearnings.objects.filter(usermail=email)]
            deletedcourse=[i.courseid for i in Deletedcourse.objects.all()]
            return render(request,'profile.html',{'user':user,'s':subjects,'cart':cart,'whishlist':whishlist,'ml':mylearning,'dl':deletedcourse})
    else:
        return render(request,'index.html')
     

def loggingin(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        if Userdetails.objects.filter(email=email).exists():
            user=Userdetails.objects.get(email=email)
            
            if user.password==password:
                
                
                request.session['tid']=email
                return redirect(profile,email=email)
            else:
                messages.info(request,'Incorrect Password')
                return render(request,'login.html')
        elif User.objects.filter(email=email, is_superuser=True).first():
            admin=User.objects.get(email=email,is_superuser=True)
            if admin.check_password(password):
                request.session['admin']=email
                return redirect(adminpage)
            else:
                messages.error(request,"Invalid Credentials")
                return render(request,'login.html') 
        else:
            messages.info(request,'Invalid User')
            return render(request,'login.html')

def teach(request,email):
    if 'tid' in request.session:
        user=Userdetails.objects.get(email=email)
        
        
        return render(request,'teach.html',{'u':user})
    else:
        return render(request,'index.html')

def teach2(request,cid):
    if 'tid' in request.session:
        course=Coursedetails.objects.get(courseid=cid)
        user=Userdetails.objects.get(email=course.email)
        return render(request,'teach2.html',{'u':user,'c':course})
    else:
        return render(request,'index.html')
    

def adddetails(request):
    if 'tid' in request.session:
        if request.method == 'POST':
            
            email1 = request.POST['email']
            category=request.POST['category'] 
            title=request.POST['title']
            description=request.POST['description']
            fee=request.POST['fee']
            thumbnail=request.FILES['thumbnail']
            
            if fee:
                teachername=Userdetails.objects.get(email=email1)

                c=Coursedetails.objects.create(email=email1,coursecategory=category,coursename=title,description=description,fees=int(fee),thumbnail=thumbnail,teachername=teachername.fullname)
                c.save()
                # return teach2(request,cid=c.courseid)
                return redirect('teachsecond',cid=c.courseid) 
            
            else:
                teachername=Userdetails.objects.get(email=email1)

                c=Coursedetails.objects.create(email=email1,coursecategory=category,coursename=title,description=description,fees=0,thumbnail=thumbnail,teachername=teachername.fullname)

                c.save()
                return redirect('teachsecond',cid=c.courseid)
                # return teach2(request,cid=c.courseid)  
    else:
        return render(request,'index.html')


def addcontent(request):
    if 'tid' in request.session:
        if request.method == 'POST':
            email=request.POST['email']
            cid=request.POST['cid']
            try:
                notes=request.FILES['notes']
                
                notetitle=request.POST['nottitle']
                
            except:
                pass

            else:
                teachername=Userdetails.objects.get(email=email)

                course=Coursecontent.objects.create(email=email,courseid=int(cid),notes=notes,notestitle=notetitle,teachername=teachername.fullname)

            try:
                video=request.FILES['videos']
                
            except:
            
                pass
            else:
                title=request.POST['title']
                teachername=Userdetails.objects.get(email=email)

                course=Coursecontent.objects.create(email=email,courseid=int(cid),video=video,videotitle=title,teachername=teachername.fullname)
            course.save()
            return redirect('teachsecond',cid=cid)
    else:
        return render(request,'index.html')


def fullclass1(request,cid,email):
    if 'tid' in request.session:
        mm=Mylearnings.objects.filter(usermail=email)
        a=0
       
        rate=0
        rate=Rating.objects.filter(email=email,courseid=cid)
        if rate:
            rate=rate[0].ratingvalue
        
        for i in mm:
            if i.courseid==int(cid):
                a+=1
        
        if a>0:
                user=Userdetails.objects.get(email=email)
                course_details=Coursedetails.objects.get(courseid=cid)
                course_content=Coursecontent.objects.filter(courseid=cid)
                return render(request,'fullclass.html',{'u':user,'cd':course_details,'cc':course_content,'rating':rate})
        else:
            mylearning=Mylearnings.objects.create(usermail=email,courseid=int(cid))
            mylearning.save()
            coursedetails=Coursedetails.objects.get(courseid=cid)
            user=Userdetails.objects.get(email=email)
            Orders.objects.create(useremail=email,teachermail=coursedetails.email,amountpaid=0,courseid=cid,coursename=coursedetails.coursename,teachername=coursedetails.teachername,username=user.fullname)
            course_details=Coursedetails.objects.get(courseid=cid)
            course_content=Coursecontent.objects.filter(courseid=cid)
            
            return render(request,'fullclass.html',{'u':user,'cd':course_details,'cc':course_content,'rating':rate})
    return render(request,'index.html')

def fullclass(request):
    if 'tid' in request.session:

        if request.method == 'POST':
            email=request.POST['email']
            cid=request.POST['cid']
            return fullclass1(request,cid,email)
    return render(request,'index.html')
def fullclassteacher(request,cid):
        a=0
       
        rate=0
        rate=Rating.objects.filter(email=request.session['tid'],courseid=cid)
        if rate:
            rate=rate[0].ratingvalue
        user=Userdetails.objects.get(email=request.session['tid'])
        course_details=Coursedetails.objects.get(courseid=cid)
        course_content=Coursecontent.objects.filter(courseid=cid)
        return render(request,'fullclass.html',{'u':user,'cd':course_details,'cc':course_content,'rating':rate})
    
def teach3(request,email) :
    if 'tid' in request.session:
        mycourse=Coursedetails.objects.filter(email=email)
        # if mycourse:
        user=Userdetails.objects.get(email=email)
        deletedcourse=[i.courseid for i in Deletedcourse.objects.all()]
        return render(request,"mycourse.html",{"user":user,"s":mycourse,'dl':deletedcourse})
        # else:
        #     return teach(request,email)
    else:
        return render(request,'index.html') 


    
def updatecontent(request):
    if 'tid' in request.session:
        cid=request.POST["cid"]
        return teach2(request,cid)
    else:
        return render(request,'index.html')
    
def signout(request):
    if 'tid' in request.session:
        request.session.flush()
        return redirect(profile) 
    
def editcontent(request):
    if 'tid' in request.session:
        if request.method == 'POST':
            cid=request.POST["cid"]
            user=Userdetails.objects.get(email=request.session['tid'])
            course=Coursedetails.objects.get(courseid=cid)
            content =Coursecontent.objects.filter(courseid=cid)
            return render(request,'editcontent.html',{'course':course,'cc':content,'u':user})
    else:
        return render(request,'index.html')   
def updatedetails(request):
    if 'tid' in request.session:
        if request.method == 'POST':
            cid=request.POST['cid']
            email1 = request.POST['email1']
            title=request.POST['title']
            description=request.POST['description']
            fee=request.POST['fee']
            course=Coursedetails.objects.filter(courseid=cid)
            if fee=='':
                fee=0
            if description:
                course.update(description=description)
            try:
                category=request.POST['category1'] 
            except :
                course.update(coursename=title,fees=fee)
                try:
                    coursename=Orders.objects.get(courseid=cid)
                except:

                    pass
                else:
                    coursename.coursename=title
                    coursename.save()
                
                
            else:
                course.update(coursecategory=category,coursename=title,fees=fee)
                try:
                    coursename=Orders.objects.get(courseid=cid)
                except:

                    pass
                else:
                    coursename.coursename=title
                    coursename.save()

                return teach3(request,email1)
            try:
                thumbnail=request.FILES['thumbnail']
            except:
                return teach3(request,email1)
            else:
                course1=Coursedetails.objects.get(courseid=cid)
                course1.thumbnail.save(thumbnail.name,thumbnail) 
                
                return teach3(request,email1)     
    else:
        return render(request,'index.html')
            


def deletecontent(request):
    if 'tid' in request.session:
        if request.method == 'POST':
            email1 = request.POST['email1']
            if 'my_checkbox' in request.POST:
                # Checkbox is checked
                a=request.POST.getlist('my_checkbox')
                for i in a:
                    Coursecontent.objects.filter(id=i).delete()
                return teach3(request,email1)
            else:
                return teach3(request,email1)
        else:
            return teach3(request,email1)
    else:
        return render(request,'index.html')
    
def updateprofile(request):
    if 'tid' in request.session:
        user=Userdetails.objects.get(email=request.session["tid"])
        return  render(request,'updateprofile.html',{'u':user})
    else:
        return render(request,'index.html')

def updatedp(request):
    if 'tid' in request.session:
        if request.method == 'POST':
            cid=request.POST['idnumber']
            dp=request.FILES['profilepic']
            course1=Userdetails.objects.get(id=cid)
            course1.profilepic.save(dp.name,dp)
            return redirect(updateprofile) 
    else:
        return render(request,'index.html')
    
def  updateuserdetails(request):
    if 'tid' in request.session:
        if request.method == 'POST':
            cid=request.POST['idnumber']
            fullname=request.POST['fullname']
            password=request.POST['password']
            email=request.POST['email']
            user=Userdetails.objects.get(id=cid)
            if request.session['tid']==email:
                if user.password==password:
                    user1=Userdetails.objects.filter(id=cid)
                    user1.update(fullname=fullname)
                    Coursedetails.objects.filter(email=email).update(teachername=fullname)
                    Coursecontent.objects.filter(email=email).update(teachername=fullname)
                    
                    return redirect(updateprofile) 
                else:
                
                    return  render(request,'updateprofile.html',{'u':user,'m':'invailid password'})
            else:
                if User.objects.filter(email=email, is_superuser=True).exists() or Userdetails.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect(updateprofile) 
                else:
                    
                    
                    course=Coursedetails.objects.filter(email=request.session['tid'])
                    coursecontent=Coursecontent.objects.filter(email=request.session['tid'])
                    mylearning=Mylearnings.objects.filter(usermail=request.session['tid'])
                    cart=Cart.objects.filter(usermail=request.session['tid'])
                    whishlist=Whishlist.objects.filter(email=request.session['tid'])
                    rating=Rating.objects.filter(email=request.session['tid'])
                    ordert=Orders.objects.filter(teachermail=request.session['tid'])
                    orderu=Orders.objects.filter(useremail=request.session['tid'])

                    request.session.flush()
                    Userdetails.objects.filter(id=cid).update(email=email,fullname=fullname)
                    course.update(email=email,teachername=fullname)
                    coursecontent.update(email=email,teachername=fullname)
                    mylearning.update(usermail=email)
                    cart.update(usermail=email)
                    whishlist.update(email=email)
                    rating.update(email=email)
                    newname=Userdetails.objects.get(email=email)
                    ordert.update(teachermail=email,username=newname.fullname,teachername=newname.fullname)
                    orderu.update(useremail=email,username=newname.fullname)
                    request.session['tid']=email
                    return redirect(updateprofile) 
            
    else:
        return render(request,'index.html')

def mylearning(request):
    if 'tid' in request.session:
        tid = request.session['tid']
        courses = Mylearnings.objects.filter(usermail=tid)
        
        l=[]
        for i in courses:
            l.append(i.courseid)
        
        coursedetails = Coursedetails.objects.filter(courseid__in=l).order_by('-date')
        user=Userdetails.objects.get(email=tid)
        
        
        return render(request,"mylearning.html",{"user":user,"data":coursedetails})
    else:
         return render(request,'index.html')
    
def addingcart(request):
    if 'tid'  in request.session:
        email=request.session['tid']
        cartdata=Cart.objects.filter(usermail=email)
        
        l=[]
        for i in cartdata:
            l.append(i.courseid)
        cartdetails = Coursedetails.objects.filter(courseid__in=l).order_by('-date')
        user=Userdetails.objects.get(email=email)
        total_fees = Cart.objects.filter(usermail=email).aggregate(total_fees=Sum('fees'))['total_fees']

        return render(request,'cart.html',{'cart':cartdetails,'user':user,'sum':total_fees})
    
    else:
        return render(request,'index.html')

def mycart(request):
    if 'tid'  in request.session:
        if request.method == 'POST':
            email=request.POST['email']
            cid=request.POST['cid']
            if  Cart.objects.filter(courseid=cid,usermail=email).exists():
                cartdata=Cart.objects.filter(usermail=email)
                price=Coursedetails.objects.get(courseid=cid).fees
                l=[]
                for i in cartdata:
                    l.append(i.courseid)
                cartdetails = Coursedetails.objects.filter(courseid__in=l).order_by('-date')
                user=Userdetails.objects.get(email=email)
                total_fees = Cart.objects.filter(usermail=email).aggregate(total_fees=Sum('fees'))['total_fees']
                
                return render(request,'cart.html',{'cart':cartdetails,'user':user,'sum':total_fees})
            else:
                price=Coursedetails.objects.get(courseid=cid).fees
                cart=Cart.objects.create(usermail=email,courseid=cid,fees=price)
                cart.save()
                cartdata=Cart.objects.filter(usermail=email)
                l=[]
                for i in cartdata:
                    l.append(i.courseid)
                cartdetails = Coursedetails.objects.filter(courseid__in=l).order_by('-date')
                user=Userdetails.objects.get(email=email)
                total_fees = Cart.objects.filter(usermail=email).aggregate(total_fees=Sum('fees'))['total_fees']
    
                return render(request,'cart.html',{'cart':cartdetails,'user':user,'sum':total_fees})
        
    else:
        return render(request,'index.html')
    
def deletingcart(request,cid):
    if  'tid'  in request.session :
        Cart.objects.get(courseid=cid,usermail=request.session['tid']).delete()
        addingwhishlist(request,cid=cid)
        return redirect(addingcart)
    else:
         
        return render(request,'index.html')

def whishlist(request):
    if  'tid'  in request.session :
        email=request.session['tid']
        whishlistdata=Whishlist.objects.filter(email=email)
        
        l=[]
        for i in whishlistdata:
            l.append(i.courseid)
        whishlistdetails = Coursedetails.objects.filter(courseid__in=l).order_by('-date')
        user=Userdetails.objects.get(email=email)

        return render(request,'whishlist.html',{'whishlist':whishlistdetails,'user':user})
    
    else:
        return render(request,'index.html')

def addingwhishlist(request,cid):
    if 'tid'  in request.session:
        
        email=request.session['tid']
        if Whishlist.objects.filter(courseid=cid,email=email).exists():
            return redirect(profile,email=email)
        else:
            Whishlist.objects.create(email=email,courseid=cid).save()
            whishlistdata=Whishlist.objects.filter(email=email)
        
            l=[]
            for i in whishlistdata:
                l.append(i.courseid)
            whishlistdetails = Coursedetails.objects.filter(courseid__in=l).order_by('-date')
            user=Userdetails.objects.get(email=email)

            return render(request,'whishlist.html',{'whishlist':whishlistdetails,'user':user})
        
def deletingwhishlist(request,cid):
    if  'tid'  in request.session :
        Whishlist.objects.get(courseid=cid,email=request.session['tid']).delete()
        return redirect(whishlist)
    else:
         
        return render(request,'index.html')
    
def payment(request):
    if  'tid'  in request.session :
        return render(request,"payment.html")
    else:
         
        return render(request,'index.html')

def paying(request):
    if 'tid'  in request.session :
        if request.method == 'POST':
            token = request.POST.get('stripeToken')
            total_fees = Cart.objects.filter(usermail=request.session['tid']).aggregate(total_fees=Sum('fees'))['total_fees']
            total_fees=int(total_fees*100)
            # Process the payment using Stripe API
            try:
                source = stripe.Source.create(
                    type="card",
                    token=token
                )
                
                # Use the source object for payment
                payment_intent = stripe.PaymentIntent.create(
                    amount=total_fees,  # Amount in cents
                    currency="inr",
                    source=source.id,  # Use the source ID here
                    description="Example Payment"
                )

                # Payment successful
                cartdata=Cart.objects.filter(usermail=request.session['tid'])
                
                course_ids = [item.courseid for item in cartdata]
                for course_id in course_ids:
                    Mylearnings.objects.create(courseid=course_id, usermail=request.session['tid'])
                    Cart.objects.filter(courseid=course_id,usermail=request.session['tid']).delete()
                    Whishlist.objects.filter(courseid=course_id,email=request.session['tid']).delete()
                    course=Coursedetails.objects.get(courseid=course_id)
                    ud=Userdetails.objects.get(email=request.session['tid'])
                    td=Userdetails.objects.get(email=course.email)
                    Orders.objects.create(useremail=request.session['tid'],teachermail=course.email,courseid=course.courseid,amountpaid=course.fees,coursename=course.coursename,username=ud.fullname,teachername=td.fullname)
                    purchasemail(email=request.session['tid'],coursename=course.coursename)
                return render(request,'paymentsuccess.html')
            except stripe.error.CardError as e:
                # Payment failed
                error_message = str(e)
                return HttpResponse("Error: " + error_message)
                

    else:
         
        return render(request,'index.html')
    
def rating(request):
    if 'tid'  in request.session :
        if request.method == 'POST':
            cid = request.POST.get('cid')
            rating_value = request.POST.get('rating')
            feedback = request.POST.get('feedback')

            existing_rating = Rating.objects.filter(email=request.session['tid'], courseid=cid).first()
           
           
            if existing_rating:
                existing_rating.ratingvalue = rating_value
                existing_rating.feedback = feedback
                existing_rating.save()

            else:
                Rating.objects.create(ratingvalue=rating_value, feedback=feedback, courseid=cid, email=request.session['tid'])
            ratings2 = Rating.objects.filter(courseid=cid)
            total_ratings = ratings2.count()
            if total_ratings > 0:
                
                max_rating = ratings2.aggregate(Sum('ratingvalue'))['ratingvalue__sum']
                rate = round(float(max_rating) / total_ratings) 
                print(max_rating)
            else:
                rate = 0  
            Coursedetails.objects.filter(courseid=cid).update(rating=rate,total_rating=total_ratings)
            
            
            return fullclass1(request, cid=cid, email=request.session['tid'])    

    else:
        return render(request,'index.html')
    

def sreach(request):
    
    if 'tid' in request.session:
        query = request.POST['search']
        
        email = request.session['tid']
        user=Userdetails.objects.get(email=email)
        subjects = Coursedetails.objects.filter(coursename__icontains=query)
        cart=[i.courseid for i in Cart.objects.filter(usermail=email)]
        
        whishlist=[j.courseid for j in Whishlist.objects.filter(email=email)] 
        mylearning = [z.courseid for z in Mylearnings.objects.filter(usermail=email)]
        deletedcourse=[i.courseid for i in Deletedcourse.objects.all()]
        subjects = subjects.exclude(courseid__in=mylearning)
        subjects = subjects.exclude(courseid__in=deletedcourse)
        return render(request,'search.html',{'user':user,'s':subjects,'cart':cart,'whishlist':whishlist})
    else:
        return render(request,'index.html')
     
def adminpage(request):
    if 'admin' in request.session:
        user=Userdetails.objects.all()
        deletedcourses=[i.courseid for i in Deletedcourse.objects.all()]

        teacher=Coursedetails.objects.all().exclude(courseid__in=deletedcourses)
        teacheremail=[i.email for i in teacher]
        user_count = user.count()
        teachercount=len(set(teacheremail))
        totalcourse=[i.courseid for i in teacher]
        totalcourse1=len(totalcourse)
        total_fees = Orders.objects.all().aggregate(total_fees=Sum('amountpaid'))['total_fees']
        message = request.GET.get('message', '')
        return render(request,"dashboard.html",{"users":user,'teachermail':teacheremail,'count':user_count,'teachercount':teachercount,'totalfees':total_fees,'tl':totalcourse1,'m':message})
    else:
        return render(request,'index.html')

def adminpagecourse(request):
    if 'admin' in request.session:
        course=Coursedetails.objects.order_by("-date")
        deletedcourse=[i.courseid for i in Deletedcourse.objects.all()]
        
        return render(request,'course.html',{'course':course,'deletedcourse':deletedcourse})
    else:
        return render(request,'index.html')
    
def adminpagebilling(request):
    if 'admin' in request.session:
        orders=Orders.objects.all()

        return render(request,'billing.html',{'order':orders})
    else:
        return render(request,'index.html')
    
def adminprofile(request):
    if 'admin' in request.session:

        admin=User.objects.get(email=request.session['admin'],is_superuser=True)
        
        return render(request,'adminprofile.html',{'admin':admin})
    else:
        return render(request,'index.html')

def adminsignout(request):
    request.session.flush()
    return redirect(profile)

def adminprofileupdate(request):
    if 'admin' in request.session:
        email=request.POST['email']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        id=request.POST['id']

        username=request.POST['username']
        password=request.POST['password']
        admin=User.objects.get(id=id,is_superuser=True)

        if admin.check_password(password):
            if User.objects.filter(email=email).exists():
                admin.username=username
                admin.first_name=firstname
                admin.last_name=lastname
                admin.save()
                return redirect(adminprofile)
            else:
                request.session.flush()
                admin.email=email
                admin.username=username
                admin.first_name=firstname
                admin.last_name=lastname
                admin.save()
                request.session['admin']=email

                return redirect(adminprofile)
        else:
            messages.info(request,'incorrect password')
            return redirect(adminprofile)
    else:
        return render(request,'index.html')
    
def adminrating(request):
    ratings=Rating.objects.all()
  
    return render(request,'rating.html',{'ratings':ratings})



def deleteuser(request,email):
 
  
    Userdetails.objects.filter(email=email).delete()
    course=Coursedetails.objects.filter(email=email)
    cid=[i.courseid for i in course]
    Deletedcourse.objects.bulk_create([Deletedcourse(courseid=cid_val) for cid_val in cid])
    Mylearnings.objects.filter(usermail=email).delete()
    Whishlist.objects.filter(email=email).delete()
    Cart.objects.filter(usermail=email).delete()
    Rating.objects.filter(email=email).delete()
    
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in active_sessions:
        session_data = session.get_decoded()
        if email == session_data.get('tid'):
            session.delete()

  
    
    return redirect(adminpage)

def deletecourse(request,id):
    if 'tid' in request.session:
        Cart.objects.filter(courseid=id).delete()
        Whishlist.objects.filter(courseid=id).delete()
        Deletedcourse.objects.create(courseid=id)
        return teach3(request,email=request.session['tid'])
    else:
        return render(request,'index.html')


 
def warningmail(request,email):
    sender_email = ""
    password = ""
    body = """
    Dear User,

    Here is your account report:

    We are writing to inform you that we have received reports regarding inappropriate content associated with your account and course. We take such matters seriously as they violate our community guidelines and terms of service.
    We urge you to review our guidelines and ensure that all content you post or interact with on our platform complies with our policies. Failure to do so may result in further action, including account suspension or termination.
    We value your participation in our community and hope that you will take the necessary steps to address this issue promptly. If you have any questions or concerns, please don't hesitate to contact us.
    
    If you have any questions or concerns, feel free to contact us.

    Best regards,
    Admin Team
    """
    message = MIMEMultipart()
    message['Subject'] = "User Account Report"
    message['From'] = sender_email
    message['To'] = email
    message.attach(MIMEText(body, 'plain'))
    server=None
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
        
    except Exception as e:
        return HttpResponse("An Error  Occurred")
    finally:
        if server:
            server.quit()
    
    return redirect(reverse('adminpage') + '?message=Mail+sent')

def coursesales(request,cid):
    orders=Orders.objects.filter(teachermail=request.session['tid'],courseid=cid)
    total_amount_paid = orders.aggregate(total_amount=Sum('amountpaid'))['total_amount']
    return render(request,'coursesales.html',{'order':orders,'email':request.session['tid'],'earnings':total_amount_paid})

def purchasemail(email,coursename):
    sender_email = ""
    password = ""
    body =f"""
    Dear User,

    Thank you for choosing Onlineclassroom for your recent purchase!

    We're excited to confirm that your order has been successfully processed . Below, you'll find the details of your purchase:

    - Coursename: {coursename}
    
    

    We hope you're as thrilled about your new course as we are to send it to you. If you have any questions about your order or anything else, please feel free to reach out to our customer support team .

    Thank you again for choosing Online Classroom. We truly appreciate your business!

    Best Regards,
    Online Classroom

    """
    message = MIMEMultipart()
    message['Subject'] = "Purchase mail"
    message['From'] = sender_email
    message['To'] = email
    message.attach(MIMEText(body, 'plain'))
    server=None
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
        
    except Exception as e:
        return HttpResponse("An Error  Occurred")
    finally:
        if server:
            server.quit()
    
