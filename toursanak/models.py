from django.db import models
#to migrate with build in model:
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Category(models.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=130)
	slug = models.SlugField(editable=False,unique=True)
	def get_absolute_url(self):
  		return ('Category', (), {'slug': self.slug,'id': self.id,})
  	def save(self):
  		self.slug = slugify(self.name)
  		super(Category, self).save()
  	#add name in admin not object
  	def __str__(self):
  		return self.name
class Page(models.Model):
    id = models.AutoField(primary_key=True)
    name =models.CharField(max_length=200)
    description=models.TextField()
    slug = models.SlugField(editable=False,unique=True)
    def get_absolute_url(self):
    	return ('Page', (), {'slug': self.slug,'id': self.id,})
  	def save(self):
  		self.slug = slugify(self.name)
  		super(Page, self).save()
  	def __str__(self):
  		return self.name
class Tour(models.Model):
	id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=400,db_index=True)
	feature_image=models.ImageField(upload_to = 'static/images/feature_image/')
	banner=models.ImageField(upload_to = 'static/images/banner/',blank=True,null=True)
	slug = models.SlugField(editable=False,unique=True)
	short_description=models.CharField(db_index=True,max_length=200)
	description=models.TextField(db_index=True,null=True,blank=True)
	keywords=models.TextField(db_index=True,null=True,blank=True)
	category=models.ForeignKey(Category, on_delete=models.CASCADE)
	map=models.TextField(null=True,blank=True)
	#map=models.TextField()
	created_by=models.ForeignKey(User,editable=False,on_delete=models.CASCADE,null=True,blank=True)
	published_at=models.DateTimeField(db_index=True,auto_now_add=True)
  	def get_absolute_url(self):
  		return ('Tour', (), {'slug': self.slug,'id': self.id,})
  	def save(self):
  		self.slug = slugify(self.title)
  		#self.created_by=request.user
  		super(Tour, self).save()
  	def __str__(self):
  		return self.title
class Schedule(models.Model):
	id=models.AutoField(primary_key=True)
	tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
	start_date=models.DateField(null=True,blank=True)
	end_date=models.DateField(null=True,blank=True)
	price = models.IntegerField(default=0,null=True,blank=True)
class Image(models.Model):
	id=models.AutoField(primary_key=True)
	imagename=models.ImageField(upload_to = 'static/images/albums/')
	tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
	#tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
	# def __str__(self):
 #  		return self.imagename
class Tab(models.Model):
	id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=100)
	tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
	def __str__(self):
  		return self.title
class TabDetail(models.Model):
	id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=300)
	description=models.TextField()
	tab=models.ForeignKey(Tab,on_delete=models.CASCADE)
	def __str__(self):
  		return self.title
class Contact(models.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=50)
	email=models.CharField(max_length=50)
	description=models.TextField(null=True,blank=True)
class Booking(models.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=30)
	email=models.CharField(max_length=50)
	description=models.TextField(null=True,blank=True)
	tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
	schedule=models.ForeignKey(Schedule,on_delete=models.CASCADE)	
	registered_at=models.DateTimeField(db_index=True,auto_now_add=True)
	def __str__(self):
  		return self.name