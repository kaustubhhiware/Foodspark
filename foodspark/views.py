from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from models import *
import json
from django.views.decorators import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.core.exceptions import *
import datetime


def home(request):
	if 'id' in request.session.keys():
		if request.session['type'] == 'customer':
			foodlist = FoodItem.objects.all().order_by('-ordercount')[:5]
			restaurants = Restaurant.objects.order_by('name')
			context = {
				'customer':Customer.objects.get(email=request.session['id']),
				'restaurants' : restaurants,
				'foodlist' : foodlist,
			}
			return render(request,'foodspark/userhome.html',context)
		elif request.session['type'] == 'restaurant':
			restaurant = Restaurant.objects.get(email=request.session['id'])
			query = Order.objects.order_by('-pk').all()
			dic = {}
			customer = {}
			for x in query:
				if x.restaurant_id == restaurant.email:
					dic2 = {}
					if(x.deliverystatus == 'd'):
						continue
					x.calamount()
					for i,j in zip(x.getfooditems(),x.getqty()):
						dic2[i] = j
					dic[x] = dic2
					customer[x] = x.customer

			context = {
				'foods' : dic,
				'customer' : customer,
				'restaurant' : restaurant,
			}

			return render(request,'foodspark/resthome.html',context)
	else:
		return render(request,"foodspark/login.html")

@ensure_csrf_cookie
def login(request):
	print "hello"
	if request.method == 'POST':
		print request.POST.keys()
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
			name = request.POST.get('name')
			phone = request.POST.get('phone')
			address = request.POST.get('address')
			city = request.POST.get('city')

			if name!="":
				customer.name = name
			if address!="":
				customer.address = address
			if city!="":
				customer.city	= city
			if phone!="":
				customer.phone = phone
			customer.save()
			messages.success(request,'Successfully saved :)')
			return render(request,'foodspark/userdetails.html',context)
		elif request.session['type'] == 'restaurant':
			restaurant = Restaurant.objects.get(email=request.session['id'])
			context = {
				'restaurant' : restaurant,
			}
			name = request.POST.get('name')
			phone = request.POST.get('phone')
			address = request.POST.get('address')
			res_type = request.POST.get('res_type')
			cuisine = request.POST.get('cuisine')
			city = request.POST.get('city')

			if phone!="":
				restaurant.phone = phone
			if address!="":
				restaurant.address = address
			if name!="":
				restaurant.name = name
			# restaurant.res_type = res_type
			if cuisine!="":
				restaurant.cuisine =cuisine
			if city!="":
				restaurant.city = city
			restaurant.save()
			messages.success(request,'Successfully saved :)')
			return render(request,'foodspark/restdetails.html',context)

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
	if searchtype == 'Restaurant':
		restaurants = Restaurant.objects.filter(name__contains=searchkey)
	elif searchtype == 'Cuisine':
		foods = FoodItem.objects.filter(cuisine__contains=searchkey)
		restaurants = []
		for x in foods:
			if x.resid not in restaurants:
				restaurants.append(x.resid)
	elif searchtype == 'Food':
		foods = FoodItem.objects.filter(name__contains=searchkey)
		restaurants = []
		for x in foods:
			if x.resid not in restaurants:
				restaurants.append(x.resid)
	elif searchtype == 'City':
		print searchkey
		restaurants = Restaurant.objects.filter(city__contains=searchkey)
	elif searchtype == 'All':
		restaurants = Restaurant.objects.filter(name__contains=searchkey)
		restaurants = list(restaurants)
		foods_cuisine = FoodItem.objects.filter(cuisine__contains=searchkey)
		foods = FoodItem.objects.filter(name__contains=searchkey)
		for x in foods:
			if x.resid not in restaurants:
				restaurants.append(x.resid)
		for x in foods_cuisine:
			if x.resid not in restaurants:
				restaurants.append(x.resid)
		rescity = Restaurant.objects.filter(city__contains=searchkey)
		rescity = list(rescity)
		for i in rescity:
			if i not in restaurants:
				restaurants.append(i)

	context = {
		'customer':Customer.objects.get(email=request.session['id']),
		'restaurants' : restaurants,
		'searchkey' : searchkey
	}
	return render(request,'foodspark/userhome.html',context)

def restaurantOrderHistory(request):
	restaurant = Restaurant.objects.get(email=request.session['id'])
	query = Order.objects.order_by('-pk').all()
	dic = {}
	customer = {}
	for x in query:
		if x.restaurant_id == restaurant.email:
			dic2 = {}
			if(x.deliverystatus == 'p'):
				continue
			x.calamount()
			for i,j in zip(x.getfooditems(),x.getqty()):
				dic2[i] = j
			dic[x] = dic2
			customer[x] = x.customer

	context = {
		'foods' : dic,
		'customer' : customer,
		'restaurant' : restaurant,
	}

	return render(request,'foodspark/resthistory.html',context)

def restprofile(request):
	restaurant = Restaurant.objects.get(email=request.session['id'])
	fooditems = FoodItem.objects.all()
	menu = {}
	for fi in fooditems:
		if fi.resid == restaurant:
			try:
				menu[fi.cuisine].append(fi)
			except KeyError:
				menu[fi.cuisine] = [fi]
		context = {
			'restaurant' : restaurant,
			'menu' : menu
		}
	return render(request,'foodspark/restprofile.html',context)

def restview(request,restname):
	if 'id' in request.session.keys():
		try:
			customer = Customer.objects.get(email=request.session['id'])
			restaurant =Restaurant.objects.get(name=restname)
			foodall = FoodItem.objects.all()
			fooditems = {}
			for x in foodall:
				if x.resid.email == restaurant.email:
					try:
						fooditems[x.cuisine].append(x)
					except KeyError:
						fooditems[x.cuisine] = [x]
			context = {
				'customer' : customer,
				'restaurant': restaurant,
				'fooditems' : fooditems,
			}
			return render(request,'foodspark/restview.html',context)
		except ObjectDoesNotExist:
			return HttpResponse("Sorry no restaurant with this name")
	else:
		return redirect('/')

def cart(request):
	if 'id' in request.session.keys():
		if request.method == 'GET':
			customer = Customer.objects.get(email=request.session['id'])
			query = Cart.objects.all()
			cart = {}
			amount = 0
			for x in query:
				if x.customer.email == customer.email:
					amount = amount + x.fooditem.price * x.foodqty
					try:
						cart[x.fooditem.resid].append(x)
					except KeyError:
						cart[x.fooditem.resid] = [x]

			if not cart:
				messages.info(request,"Your cart is currently empty")
			context = {
					'customer': customer,
					'cart' : cart,
					'amount' : amount
			}
			return render(request,"foodspark/ordercart.html",context)
		elif request.method == 'POST':
			########delete cart update order
			customer = Customer.objects.get(email=request.session['id'])
			orders = {}
			ordersqty = {}
			for q in Cart.objects.all():
				if q.customer == Customer.objects.get(email=request.session['id']):
					try:
						orders[q.fooditem.resid] = orders[q.fooditem.resid] + ',' + str(q.fooditem.pk)
					except KeyError:
						orders[q.fooditem.resid] = str(q.fooditem.pk)
					try:
						ordersqty[q.fooditem.resid] = ordersqty[q.fooditem.resid] + ',' + str(q.foodqty)
					except KeyError:
						ordersqty[q.fooditem.resid] = str(q.foodqty)
					q.delete()
			for x,y in zip(orders,ordersqty):
				o = Order(customer=customer,restaurant=x,foodlist=orders[x],foodqty=ordersqty[y],ordertime=datetime.datetime.now(),deliverystatus='p')
				o.calamount()
				o.save()
			messages.success(request,"Payment Successfull :)")
			return render(request,"foodspark/ordercart.html")
	else:
		return render(request,"foodspark/login.html")

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

def history(request):
	if 'id' in request.session.keys():
		customer = Customer.objects.get(email=request.session['id'])
		query = Order.objects.order_by('-pk').all()
		pending_rest = {}
		pending_items = {}
		history_rest = {}
		history_items = {}
		for x in query:
			if x.customer == customer:
				if(x.deliverystatus == 'p'):
					print "1"
					dic2 = {}
					x.calamount()
					for i,j in zip(x.getfooditems(),x.getqty()):
						dic2[i] = j
					pending_items[x] = dic2
					pending_rest[x] = x.restaurant
				if(x.deliverystatus == 'd'):
					dic2 = {}
					x.calamount()
					for i,j in zip(x.getfooditems(),x.getqty()):
						dic2[i] = j
					history_items[x] = dic2
					history_rest[x] = x.restaurant


		context = {
			'customer' : customer,
			'pending_items' : pending_items,
			'pending_rest' : pending_rest,
			'history_items' : history_items,
			'history_rest' : history_rest,
		}
		return render(request,"foodspark/userhistory.html",context)
	else:
		return render(request,"foodspark/login.html")


def recommendedRests():
	pass

def saveToCart(request):
	if 'id' in request.session.keys():
		foodall = FoodItem.objects.all()
		for x in foodall:
			if 'food' + str(x.pk) in request.POST.keys():
				if int(request.POST['food' + str(x.pk)]) > 0:
					cartitem = Cart(customer = Customer.objects.get(email=request.session['id']), fooditem = FoodItem.objects.get(pk=x.pk), foodqty= request.POST['food' + str(x.pk)])
					cartitem.save()
		customer = Customer.objects.get(email=request.session['id'])
		query = Cart.objects.all()
		cart = {}
		amount = 0
		for x in query:
			if x.customer.email == customer.email:
				amount = amount + x.fooditem.price * x.foodqty
				try:
					cart[x.fooditem.resid].append(x)
				except KeyError:
					cart[x.fooditem.resid] = [x]
		if not cart:
			messages.info(request,"Your cart is currently empty")
		context = {
				'customer': customer,
				'cart' : cart,
				'amount' : amount
		}
		for x,y in cart.iteritems():
			for z in y:
				z.fooditem.ordercount = z.fooditem.ordercount + z.foodqty
				z.fooditem.save()
		return render(request,"foodspark/ordercart.html",context)
	else:
		return render(request,"foodspark/login.html")

def delivered(request):
	if 'id' in request.session.keys() and request.session['type'] == 'restaurant':
		order = Order.objects.get(pk = request.POST['orderid'])
		order.deliverystatus = 'd'
		order.save()
		return redirect('/')

	else:
		return render(request,"foodspark/login.html")

def addfooditem(request):
	if 'id' in request.session.keys() and request.session['type'] == 'restaurant':
		restaurant = Restaurant.objects.get(email=request.session['id'])
		name = request.POST['name']
		cuisine = request.POST['cuisine']
		price = request.POST['price']
		food = FoodItem(resid=restaurant,name=name,cuisine=cuisine,price=price,course='s',availability_time=datetime.datetime.now())
		food.save()
		return redirect('/restprofile/')
	else:
		return render(request,"foodspark/login.html")

def removefooditem(request):
	if 'id' in request.session.keys() and request.session['type'] == 'restaurant':
		restaurant = Restaurant.objects.get(email=request.session['id'])
		food = FoodItem.objects.get(pk=request.POST['foodid'])
		food.delete()
		return redirect('/restprofile/')
	else:
		return render(request,"foodspark/login.html")

def about(request):
	if 'id' in request.session.keys():
		if request.session['type'] == 'restaurant':
			user = Restaurant.objects.get(email=request.session['id'])
		else:
			user = Customer.objects.get(email=request.session['id'])
		context = {
			'user': user,
		}
		return render(request,"foodspark/about.html",context)
	else:
		return render(request,"foodspark/about.html")
