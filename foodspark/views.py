from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from models import *
import json
from django.views.decorators import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages

### TODO
# check 'id' in session for all views
# modify edit methods to remove old objects

def home(request):
	if 'id' in request.session.keys():
		if request.session['type'] == 'customer':
			restaurants = Restaurant.objects.order_by('name')
			context = {
				'customer':Customer.objects.get(email=request.session['id']),
				'restaurants' : restaurants
			}
			return render(request,'foodspark/userhome.html',context)
		elif request.session['type'] == 'restaurant':
			context = {
				'restaurant':Restaurant.objects.get(email=request.session['id'])
			}
			return render(request,'foodspark/resthome.html',context)
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
			if customer.check_password(password):
				request.session['id'] = email
				request.session['type'] = 'customer'
				return redirect('/')
			else:
				messages.error(request,'Password Incorrect')
				return redirect('/')
		except:
			try:
				restaurant = get_object_or_404(Restaurant, email=email)
				if restaurant.check_password(password):
					request.session['id'] = email
					request.session['type'] = 'restaurant'
					return redirect('/')
				else:
					messages.error(request,'Password Incorrect')
					return redirect('/')
			except:
				messages.error(request,'No Customer or Restaurant is registered with this email')
				return redirect('/')

	elif request.method == 'GET':
		return render(request,'foodspark/login.html')

def signup(request): 
	if request.method == 'POST':
		email = request.POST.get('email')
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
		request.session.modified = True
	except KeyError:
		pass
	return render(request, 'foodspark/login.html')

def editDetails(request):
	if request.method == 'POST':
		if request.session['type'] == 'customer':
			customer = Customer.objects.get(email=request.session['id'])
			context = {
				'customer':customer,
				}
			email = request.POST.get('email')
			name = request.POST.get('name')
			phone = request.POST.get('phone')
			address = request.POST.get('address')
			city = request.POST.get('city')
			if email == customer.email:
				customer.name = name
				customer.address = address
				customer.city	= city
				customer.phone = phone
				customer.email = email
			elif Customer.objects.filter(email=email).exist():
				messages.error(request,'Email Already Taken :(')
				return render(request,'foodspark/userdetails.html',context)
			else :
				customer.email = email
				customer.name = name
				customer.address = address
				customer.city	= city
				customer.phone = phone
			customer.save()
			messages.success(request,'Successfully saved :)')
			return render(request,'foodspark/userdetails.html',context)
		elif request.session['type'] == 'restaurant':
			restaurant = Restaurant.objects.get(email=request.session['id'])
			context - {
				'restaurant' : restaurant,
			}
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
				messages.error(request,'Email Already Taken :(')
		 		return render(request,'foodspark/userdetails.html',context)
			else:
				restaurant.email = email
				restaurant.phone = phone
				restaurant.address = address
				restaurant.name = name
				restaurant.res_type = res_type
				restaurant.cuisine =cuisine
				restaurant.city = city
			restaurant.save()
			messages.success(request,'Successfully saved :)')
			return render(request,'foodspark/userdetails.html',context)

	elif request.method == 'GET':
		return render(request,'foodspark/details.html')

def changePassword(request):
	if request.method == "POST":
		if request.session['type'] == 'customer':
			customer = Customer.objects.get(email=request.session['id'])
			oldPassword = request.POST.get('oldPassword')
			newPassword = request.POST.get('newPassword')
			if customer.check_password(oldPassword):
				customer.set_password(customer.make_password(newPassword))
				messages.success(request,"Password Successfully Changed")
				customer.save()
			else:
				messages.error(request,"Old password is incorrect")
			return render(request,'foodspark/changePassword.html')
		elif request.session['type'] == 'restaurant':
			restaurant = Restaurant.objects.get(email=request.session['id'])
			oldPassword = request.POST.get('oldPassword')
			newPassword = request.POST.get('newPassword')
			if restaurant.check_password(oldPassword):
				restaurant.set_password(restaurant.make_password(newPassword))
				messages.success(request,"Password Successfully Changed")
				restaurant.save()
			else:
				messages.error(request,"Old password is incorrect")
			return render(request,'foodspark/changePassword.html')

	elif request.method == 'GET':
		return render(request,'foodspark/changePassword.html')
	

def search(request):
	searchkey = request.GET.get('search')
	searchtype = request.GET.get('search_param')
	restaurants = Restaurant.objects.filter(name__contains=searchkey)
	context = {
		'customer':Customer.objects.get(email=request.session['id']),
		'restaurants' : restaurants,
		'searchkey' : searchkey
	}
	return render(request,'foodspark/userhome.html',context)

def customerOrderHistory(request):
	customer = Customer.objects.get(email=request.session['id'])
	query = Order.objects.all()
	history = []
	for x in query:
		if x.customer_id == customer.email:
			history.append(x)

def restaurantOrderHistory(request):
	restaurant = Restaurant.objects.get(email=request.session['id'])
	query = Order.objects.all()
	history = []
	for x in query:
		if x.restaurant_id == restaurant.email:
			history.append(x)


def restview(request,restname):
	if 'id' in request.session.keys():
		try:
			customer = Customer.objects.get(email=request.session['id'])
			restaurant =Restaurant.objects.get(name=restname)
			context = {
				'customer' : customer,
				'restaurant': restaurant,
			}
			return render(request,'foodspark/restview.html',context)
		except:
			return HttpResponse("Sorry no restaurant with this name")
	else:
		return redirect('/')

def details(request):
	if 'id' in request.session.keys():
		if request.session['type'] == 'customer':
			context = {
				'customer':Customer.objects.get(email=request.session['id']),
			}
			return render(request,'foodspark/userdetails.html',context)
		elif request.session['type'] == 'restaurant':
			context = {
				'restaurant':Restaurant.objects.get(email=request.session['id'])
			}
			return render(request,'foodspark/restdetails.html',context)
	else:
		return render(request,"foodspark/login.html")

def makepayment(request):
	pass

def history(request):
	if 'id' in request.session.keys():
		customer = Customer.objects.get(email=request.session['id'])
		query = Order.objects.all()
		restaurants = Restaurant.objects.all()
		history = {}
		rests = []

		for x in query:
			if x.customer_id == customer.email:
				y = restaurants.get(email=x.restaurant.email)
				history[x] = y.name

		context = {
				'customer': customer,
				'history' : history,
		}
		return render(request,"foodspark/userhistory.html",context)
	else:
		return render(request,"foodspark/login.html")

def cart(request):
	if 'id' in request.session.keys():
		customer = Customer.objects.get(email=request.session['id'])
		query = Order.objects.all()
		history = []
		for x in query:
			if x.customer_id == customer.email and x.deliverystatus=='p':
				history.append(x)
		context = {
				'customer': customer,
				'cart' : history
		}
		return render(request,"foodspark/ordercart.html",context)
	else:
		return render(request,"foodspark/login.html")

def recommendedRests():
	pass