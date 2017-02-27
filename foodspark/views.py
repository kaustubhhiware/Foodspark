from django.shortcuts import render, redirect
from django.http import HttpResponse
from models import *
import json
from django.views.decorators import csrf
from django.views.decorators.csrf import ensure_csrf_cookie


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
				return HttpResponse('password incorrect')

		if restaurant:
			if restaurant.check_password(password):
				request.session['id'] = email
				request.session['type'] = 'restaurant'
				return redirect('/')
			else:
				return HttpResponse('password incorrect')				

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

def editCustomer(request):
	if request.method == 'POST':
		customer = Customer.objects.get(email=request.session['id'])
		email = request.POST.get('email')
		# if Customer.objects.filter(email=email).exists():
		name = request.POST.get('name')
		phone = request.POST.get('phone')
		password = request.POST.get('password')
		address = request.POST.get('address')
		if email == customer.email:
			customer.name = name #check syntax
			#fill rest
		elif Customer.objects.filter(email=email).exist():
			#email taken
			customer.email = email
		#fill rest

	elif request.method == 'GET':
		return render(request,'foodspark/')

# def editRestaurant(request):
	# copy paste edit Customer

