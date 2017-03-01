from foodspark.models import *
import json
import random

def genphone():
	pstr = ""
	for i in xrange(1,11):
		if i==1:
			pstr = pstr + str(random.randint(0,9))
		else:
			pstr = pstr + str(random.randint(0,9))
	return pstr
	
	
def le_email(email):
	pstr = ""
	for  i in xrange(0,len(email)):
		if(email[i]==" "):
			continue
		else:
			pstr = pstr+ email[i]
	return pstr

if __name__ == '__main__':
	for x in xrange(1,1001):
		try : 
			res = Restaurant()
			string = "zomatoapi/"+str(x)+"out.json"
			#print string
			new_f = open(string,"r")
			new_data = json.load(new_f)
			res.name = str(new_data["name"])
			estr = le_email(res.name)+str(x)+"@gmail.com"
			res.email = estr
			res.set_password(res.make_password(le_email(res.name)))
			try : 
				res.address = str(new_data["location"]["address"])
			except:
				res.address = new_data["location"]["address"]
			res.city = str(new_data["location"]["city"])
			res.res_type = str(res.res_type)
			res.cuisine = str(new_data["cuisines"])
			res.imgurl = str(new_data["photos_url"])
			res.phone = genphone()
			res.save()		
			print "saved " + res.name
		except :
			print "Nothing saved"
