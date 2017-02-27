from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
import hashlib


# Create your models here.
class Restaurant(models.Model):
	email = models.EmailField(primary_key = True)
	password = models.CharField(max_length=100)
	name = models.CharField(max_length=200)
	address = models.TextField()
	# RES_TYPE = (   ############fill it up##################################################@#
	# 	('B','Bar'),
	# 	('R','Restaurant'),
	# 	('C','Cafe')
	# )
	# res_type = models.CharField(max_length=1,choices = RES_TYPE)
	# cuisine = models.CharField(null = True, max_length=100)
	# RATING = (
	# 	('1','1'),
	# 	('2','2'),
	# 	('3','3'),
	# 	('4','4'),
	# 	('5','5')
	# )
	# rating = models.CharField(null = True,max_length=1,choices = RATING) 
	# city = models.CharField(max_length = 100)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	phone = models.CharField(validators=[phone_regex],max_length=15,blank = True) 
	# image = models.ImageField(null=True) ############################################################
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

	def details(self):
		return {
			'userid' : self.userid,
			'name' : self.name,
			'email' : self.email,
			'password' : self.password,
			'phone' : self.phone
		}

#class Admin(models.Model):   #######################
#	adminid = models.ForeignKey(Customer,on_delete=models.CASCADE,primary_key=True)

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
	image = models.ImageField() ###########################################################
	# group = models.ForeignKey()

# class Payment(models.Model):
# 	amount = models.IntegerField()
# 	discount = models.IntegerField()

# class Order(models.Model):
# 	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
# 	restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
# 	# food = models.OneToMany
# 	amount = models.IntegerField()
# 	ordertime = models.TimeField()
# 	STATUS = (
# 		('p','Pending'),
# 		('d','Delivered')
# 	)
# 	paymentstatus = models.CharField(max_length=1,choices=STATUS)
# 	