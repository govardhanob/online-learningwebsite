from django.db import models

# Create your models here.
class Userdetails(models.Model):
    fullname=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    profilepic=models.ImageField(default='../media/user_images/blank-profile-picture-973460_1280.png')
    def __str__(self):
        return self.fullname
    
class Coursedetails(models.Model):
    email=models.EmailField(max_length=50)
    courseid=models.AutoField(primary_key=True)
    coursecategory=models.CharField(max_length=100,null=False)
    coursename=models.CharField(max_length=100,null=False)
    description=models.TextField()
    thumbnail=models.FileField()
    fees=models.FloatField(default=0)
    date=models.DateField(auto_now_add=True)
    rating=models.IntegerField(default=0)
    total_rating=models.IntegerField(default=0)
    teachername=models.CharField(max_length=100)

   
    def __str__(self):
        return self.coursename

class Coursecontent(models.Model):
    teachername=models.CharField(max_length=100)

    email=models.EmailField(max_length=50)
    courseid=models.IntegerField()
    videotitle=models.CharField(max_length=200)
    video=models.FileField()
    notestitle=models.CharField(max_length=300,blank=True)
    notes=models.FileField(blank=True)
    

class Mylearnings(models.Model):
    usermail=models.EmailField(max_length=50)
    courseid=models.IntegerField()

class Cart(models.Model):
    usermail=models.EmailField(max_length=50)
    courseid=models.IntegerField()
    fees=models.FloatField()

class Whishlist(models.Model):
    email=models.EmailField(max_length=50)
    courseid=models.IntegerField()

class Rating(models.Model):  
    email=models.EmailField(max_length=50)  
    courseid=models.IntegerField()
    ratingvalue=models.PositiveSmallIntegerField()
    feedback=models.CharField(max_length=400,default=None) 

class  Orders(models.Model):
    useremail=models.EmailField(max_length=100)
    teachermail=models.EmailField(max_length=100)
    username=models.CharField(max_length=100)
    coursename=models.CharField(max_length=100)
    teachername=models.CharField(max_length=100)
    amountpaid=models.DecimalField(max_digits=8,decimal_places=2)
    courseid=models.IntegerField()

class Deletedcourse(models.Model):
    courseid=models.IntegerField()