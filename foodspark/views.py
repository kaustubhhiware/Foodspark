from django.shortcuts import render, redirect
from django.http import HttpResponse
from models import *
import json
from django.views.decorators import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages

# Create your views here.

def home(request):
	# if 'id' in request.session.keys():
	# 	customer = Customer.objects.get(email = request.session['id'])
	# 	if (customer is not None):
	# 		return render(request, ) #...................
	# 	return render(request,) #.............
	# else:
	if 'id' in request.session.keys():
		if request.session['type'] == 'customer':
			restaurants = Restaurant.objects.order_by('name')
			context = {
				'name':Customer.objects.get(email=request.session['id']).name,
				'restaurants' : restaurants
			}
			return render(request,'foodspark/userhome.html',context)
		elif request.session['type'] == 'restaurant':
			return render(request,'foodspark/resthome.html')
	else:
		return render(request,"foodspark/login.html")

@ensure_csrf_cookie
def login(request):
	print "hello"
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		try:
			customer = Customer.objects.get(email=email)
		except DoesNotExist:
			restaurant = get_object_or_404(Restaurant, email=email)

		if customer:
			if customer.check_password(password):
				request.session['id'] = email
				request.session['type'] = 'customer'
				return redirect('/')
			else:
				messages.error(request,'Password Incorrect')
				print 'here'
				return redirect('/')

		if restaurant:
			if restaurant.check_password(password):
				request.session['id'] = email
				request.session['type'] = 'restaurant'
				return redirect('/')
			else:
				messages.error(request,'Password Incorrect')
				print 'here'
				return redirect('/')

	elif request.method == 'GET':
		return render(request,'foodspark/login.html')

def signup(request): 
	if request.method == 'POST':
		email = request.POST.get('email')
		# if Customer.objects.filter(email=email).exists():

		name = request.POST.get('name')
		phone = request.POST.get('phone')
		password = request.POST.get('password')
		address = request.POST.get('address')
		usertype = request.POST.get('usertype')
		if usertype == 'Customer':
			user = Customer(name = name, email = email, phone = phone, address = address)
			user.set_password(user.make_password(password))
			user.save()
			request.session['id'] = email
			request.session['type'] = 'customer'
		elif usertype == 'Restaurant':
			user = Restaurant(name= name, email = email, phone = phone, address = address)
			user.set_password(user.make_password(password))
			user.save()
			request.session['id'] = email
			request.session['type'] = 'restaurant'
		return redirect('/')

	if request.method == 'GET':
		return render(request,'foodspark/login.html')

def logout(request):
	try:
		del request.session['id']
		del request.session['type']
	except KeyError:
		pass
	return render(request, 'foodspark/login.html')

def editCustomer(request):
	if request.method == 'POST':
		customer = Customer.objects.get(email=request.session['id'])
		email = request.POST.get('email')
		# if Customer.objects.filter(email=email).exists():
		name = request.POST.get('name')
		phone = request.POST.get('phone')
		#password = request.POST.get('password')
		address = request.POST.get('address')
		city = request.POST.get('city')
		if email == customer.email:
			customer.name = name #check syntax
			customer.address = address
			customer.city	= city
			customer.phone = phone
			customer.email = email
		elif Customer.objects.filter(email=email).exist():
			#email taken
			print "Email Already taken, email not updated"
			customer.address = address
			customer.city	= city
			customer.phone = phone
			customer.name = name
		else :
			customer.name = name #check syntax
			customer.address = address
			customer.city	= city
			customer.phone = phone
			customer.email = email
		customer.save()
		restaurants = Restaurant.objects.order_by('name')
		context = {
			'name':customer.name,
			'restaurants' : restaurants
			}
		return render(request,'foodspark/userhome.html',context)

	elif request.method == 'GET':
		return render(request,'foodspark/')

def editRestaurant(request):
	if request.method == "POST":
		restaurant = Restaurant.objects.get(email=request.session['id'])
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		address = request.POST.get('address')
		name = request.POST.get('name')
		res_type = request.POST.get('res_type')
		cuisine = request.POST.get('cuisine')
		city = request.POST.get('city')
		if email == restaurant.email:
			restaurant.phone = phone
			restaurant.address = address
			restaurant.name = name
			restaurant.res_type = res_type
			restaurant.cuisine =cuisine
			restaurant.city = city
		elif Restaurant.objects.filter(email=email).exist():
			#email taken
	 		print "Email Already taken, email not updated"
	 		restaurant.phone = phone
			restaurant.address = address
			restaurant.name = name
			restaurant.res_type = res_type
			restaurant.cuisine =cuisine
			restaurant.city = city
		else:
			restaurant.phone = phone
			restaurant.address = address
			restaurant.name = name
			restaurant.res_type = res_type
			restaurant.cuisine =cuisine
			restaurant.city = city
			restaurant.email = email
		restaurant.save()
		return render(request,'foodspark/resthome.html')

	elif request.method == 'GET':
		return render(request,'foodspark/')

def customerChangePassword(request):
	if request.method == "POST":
		customer = Customer.objects.get(email=request.session['id'])
		oldPassword = request.POST.get('oldPassword')
		newPassword = request.POST.get('newPassword')
		if customer.check_password(oldPassword):
			customer.set_password(customer.make_password(newPassword))
			print "Password changed"
		else:
			print "Old Password is incorrect"
		customer.save()
		return render(request,'foodspark/userhome.html')

	elif request.method == 'GET':
		return render(request,'foodspark/')

def restaurantChangePassword(request):
	if request.method == "POST":
		restaurant = Restaurant.objects.get(email=request.session['id'])
		oldPassword = request.POST.get('oldPassword')
		newPassword = request.POST.get('newPassword')
		if restaurant.check_password(oldPassword):
			restaurant.set_password(restaurant.make_password(newPassword))
			print "Password changed"
		else:
			print "Old Password is incorrect"
		restaurant.save()
		return render(request,'foodspark/resthome.html')

	elif request.method == 'GET':
		return render(request,'foodspark/')

def customerHistory(request):
	pass
	

def search(request):
	print '1'
	print request.body
	searchkey = request.GET.get('search')
	restaurants = Restaurant.objects.filter(name__contains=searchkey)
	context = {
		'name':Customer.objects.get(email=request.session['id']).name,
		'restaurants' : restaurants
	}
	return render(request,'foodspark/userhome.html',context)
