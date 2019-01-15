#ref : https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html
# Created by Raphael Partouche 

import requests
from bs4 import BeautifulSoup
import urllib

import numpy as np
import cv2



class itemsinfomation(object):
	"""docstring for itemsinfomation"""
	def setplace(self, _place):
		self.place = _place

	def seturlimage(self, _url):
		self.url_image = _url

	def setdate(self,_date):
		self.date = _date

	def setphonenumber(self, _phonenumber):
		self.phonenumber = _phonenumber

	def setpath(self, _path):
		self.path = _path

	def setsimilarities(self, _int):
		self.similarities = _int

	def print_item_informations(self):
		print ("			")
		print ("Place : " + self.place)
		print ("Url Image : " + str(self.url_image))
		print ("Date : " + str(self.date))
		print ("Phone number : " + str(self.phonenumber))
		print ("Path : " + str(self.path))
		print ("similarities : " + str(self.similarities))

		print( "		_______________			" )

	def __init__(self):
		super(itemsinfomation, self).__init__()
		self.place = "Nowhere"
		self.url_image = "Unknown"
		self.date = "Unknown"
		self.phonenumber = "Unknown"
		self.path = ""
		self.similarities = 0


def checkfoundinformation(list_ITEMS):

	buffer_ = list_ITEMS[0];

	for item in list_ITEMS:


		if buffer_.similarities<=item.similarities : 
			buffer_ = item
	print("\n\n")

	print("..... RESULTS .....")
	buffer_.print_item_informations()

def load_images(list_ITEMS):

	url_images = []

	for item in list_ITEMS:
		url_images.append(item.url_image)

	compteur = 0
	#for url_image in url_images:
	print("..... Loading .....")

	for item in list_ITEMS :
	    compteur = compteur+1;
	    path = "inside/lostandfound_" + str(compteur) + ".jpg"
	    item.setpath(path)
	    urllib.urlretrieve(item.url_image, path)

def featurematching(list_ITEMS):

	
	img_ref = cv2.imread('inside/lostandfound_12.jpg',1) # trainImage

	sift = cv2.xfeatures2d.SIFT_create()

	kp2, des2 = sift.detectAndCompute(img_ref,None)

	similarities = {}

	compteur = 1

	print(".... Loading ....")
	print(".... 10% ....")

	for item in list_ITEMS :

		if compteur == len(list_ITEMS):
			print(".... 80% ....")

			break;

		imgX = cv2.imread(item.path,1) # trainImage

		kpX, desX = sift.detectAndCompute(imgX,None)

		bf = cv2.BFMatcher()

		matches = bf.knnMatch(desX,des2, k=2)

		good = []
		for m,n in matches:
		    if m.distance < 0.75*n.distance:

		        good.append([m])

		
		item.setsimilarities(len(good))
		compteur = compteur +1
	print(".... End ....")


def print_list_items(list_ITEMS):
	for item in list_ITEMS:
		item.print_item_informations()


def return_source(url): 

	url = requests.get(url)

	source = BeautifulSoup(url.text, 'html.parser')
	return source



def retrieve_img(url_):

	source = return_source(url_) 

	for a in source.find_all('h3', class_= 'se_textarea'):
	    	#print(a.text)
	    	date = a.text

	for a in source.find_all('div', class_= 'se_viewArea'):
	    if a.img:
	    	url_image = a.img['src']

	compteur = 0;
	_phonenumber=" "
	_place = " "
	notused = " "
	for a in source.select("p > span"):

		if compteur == 0:
			_place = a.text
		elif compteur == 1: 
			_phonenumber = a.text
		else :
			notused = " "
		compteur = compteur +1 

	item = itemsinfomation()

	item.setdate(date)
	item.seturlimage(url_image)
	item.setphonenumber(_phonenumber)
	item.setplace(_place)
	return item





########################


choice = 0
list_ITEMS= []
while (choice !=3) : 
	print("1. Load from the website : 1\n2. Feature Matching and Results : 2\n3. Exit : 3")
	choice = input()

	if (choice ==1) : 
		source = return_source('https://blog.naver.com/PostList.nhn?blogId=chjin9707&widgetTypeCall=true&categoryNo=1&directAccess=true')

		list_url = []
		for a in source.find_all('a', href=True, class_="link pcol2"):
		    #print "Found the URL:", a['href']
		    list_url.append(a['href'])


		compteur = 0
		for a in list_url:
			list_url[compteur] = 'https://blog.naver.com' + list_url[compteur]
			compteur = compteur +1


		list_ITEMS = []
		for url_page in list_url: 
			list_ITEMS.append(retrieve_img(url_page))
			
		load_images(list_ITEMS)

		print(".... Images loaded ! ....")

		#print_list_items(list_ITEMS)


	if (choice == 2):
		#print("Start feature matching")
		featurematching(list_ITEMS)


		checkfoundinformation(list_ITEMS)
		choice = 3



