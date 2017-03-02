from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
import hashlib
from django.core.validators import  *
from django.core.exceptions import ValidationError
import datetime

# default order time bug hai
class Restaurant(models.Model):
	email = models.EmailField(primary_key = True)
	password = models.CharField(max_length=100)
	name = models.CharField(max_length=200)
	address = models.TextField()
	RES_TYPE = (
		('B','Bar'),
		('R','Restaurant'),
		('C','Cafe')
	)
	res_type = models.CharField(max_length=1,choices = RES_TYPE,default = 'R')
	cuisine = models.CharField(null = True, max_length=100)
	# RATING = (
	# 	('1','1'),
	# 	('2','2'),
	# 	('3','3'),
	# 	('4','4'),
	# 	('5','5')
	# )
	# rating = models.CharField(null = True,max_length=1,choices = RATING)
	# countrating = models.IntegerField(default = 0)
	city = models.CharField(max_length = 100,null = True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	phone = models.CharField(validators=[phone_regex],max_length=15,blank = True)
	#image = models.ImageField(default = '/home/projjal/Projects/Foodspark/foodspark/static/img')
	imgurl = models.CharField(max_length=1000,null=True)
	 ############################################################
	def make_password(self ,password):
		assert password
		hashedpassword = hashlib.md5(password).hexdigest()
		return hashedpassword
	def check_password(self, password):
		assert password
		hashed = hashlib.md5(password).hexdigest()
		return self.password == hashed
	def set_password(self, password):
		self.password = password

class Customer(models.Model):
	# userid = models.CharField(primary_key = True,max_length =50)
	password = models.CharField(max_length=100)
	name = models.CharField(max_length=200)
	address = models.TextField()
	city = models.CharField(max_length = 100)
	email = models.EmailField(primary_key = True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	phone = models.CharField(validators=[phone_regex],max_length=15,blank = True)
	def make_password(self ,password):
		assert password
		hashedpassword = hashlib.md5(password).hexdigest()
		return hashedpassword
	def check_password(self, password):
		assert password
		hashed = hashlib.md5(password).hexdigest()
		return self.password == hashed
	def set_password(self, password):
		self.password = password

class FoodItem(models.Model):
	resid = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	cuisine = models.CharField(max_length=100)
	COURSE = (
		('s','Starter'),
		('m','Main Course'),
		('d','Desert')
	)
	course = models.CharField(max_length=1,choices=COURSE)
	price = models.IntegerField()
	availability_time = models.TimeField()
	ordercount = models.IntegerField(default = 0)
	# image = models.ImageField(null = True) ###########################################################
	# group = models.ForeignKey()

class Order(models.Model):
 	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
 	restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
 	foodlist = models.CharField(max_length = 500,validators=[validate_comma_separated_integer_list],null=True)
 	foodqty = models.CharField(max_length = 500,validators=[validate_comma_separated_integer_list],null=True)
 	amount = models.IntegerField(default = 0)
	ordertime = models.TimeField()
	orderdate = models.DateField(auto_now_add=True)	
	DSTATUS = (
		('p','Pending'),
		('d','Delivered')
	)
	deliverystatus = models.CharField(max_length=1,choices=DSTATUS,default = 'p')

	def calamount(self):
		self.amount = 0
		myl = self.foodlist.split(",")
		qty = self.foodqty.split(",")
		for x,y in zip(myl,qty):
			fitem = FoodItem.objects.get(pk=int(x))
			self.amount = self.amount + fitem.price*int(y)

	def getfooditems(self):
		myl = self.foodlist.split(",")
		items = []
		for x in myl:
			items.append(FoodItem.objects.get(pk=int(x)))
		return items

	def getqty(self):
		myl = self.foodqty.split(",")
		return myl

class Cart(models.Model):
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
 	fooditem = models.ForeignKey(FoodItem,on_delete=models.CASCADE)
 	foodqty = models.IntegerField()
