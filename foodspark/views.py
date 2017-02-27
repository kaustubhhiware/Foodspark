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
	return HttpResponse("wassup")

# def details(request):
# 	if (request.session['type'] == 'customer'):
# 		return render(request, )
# 	elif (request.session['type'] == 'restaurant'):
# 		return render(request, )

# def cart(request):
# 	return render
@ensure_csrf_cookie
def login(request):
	print "hello"
	if request.method == 'POST':
		# json_data = request.body
		# if not json_data:
		# 	print "here1"
		# 	response = {'status': 1 , 'message' : 'Confirmed', 'url':'/login/'}
		# 	return HttpResponse(json.dumps(response), content_type='application/json')
		# json_data = json.loads(json_data)
		email = request.POST.get('email')
		password = request.POST.get('password')
		try:
			customer = Customer.objects.get(email=email)
		except:
			customer = None

		if customer and customer.check_password(password):
			print "here2"
			request.session['id'] = customer.email
			return HttpResponse("hi")#json.dumps(response), content_type='application/json')
		else:
			print "here3"
			return redirect('/')

	elif request.method == 'GET':
		print "here4"
		return render(request,'foodspark/login.html')

def signup(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		password = request.POST.get('password')
		address = request.POST.get('address')
		usertype = request.POST.get('usertype')
		newCustomer = Customer(name = name, email = email, phone = phone)
		newCustomer.set_password(newCustomer.make_password(password))
		newCustomer.save()
		print "Created Users succesfully"
		return redirect('/')

	if request.method == 'GET':
		return render(request,'foodspark/login.html')
