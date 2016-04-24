from django.db import models
from django.contrib import admin

class Account(models.Model):
	username = models.CharField(max_length=50,null=True)
	password = models.CharField(max_length=50,null=True)
	firstname = models.CharField(max_length=150,null=True)
	lastname = models.CharField(max_length=50,null=True)
	company = models.CharField(max_length=100,null=True)
	address = models.CharField(max_length=100,null=True)
	# email    = models.EmailField(null=True)
	def __str__(self):
		return 'username:%s password:%s' % (self.username, self.password)	
	class Admin:
		pass
# put before download
class Media(models.Model):
	# filename length is large engough
	filename 	= models.CharField(max_length=150,null=True)
	# account  = models.ForeignKey(Account)
	username 	= models.CharField(max_length=50,null=True)
	type 	 	= models.CharField(max_length=50,null=True)
	path	 	= models.FileField(upload_to='static/media/%Y/%m/%d')
	IP 	     	= models.IPAddressField(null=True)
	uploadTime  = models.DateTimeField(auto_now_add=True, blank=True)
	meta 		= models.CharField(max_length=200,null=True)
	keyword 	= models.CharField(max_length=200,null=True)
	aveScore	= models.FloatField(default=0.0,null=True)
	numOfViewer	= models.IntegerField(default=0,null=True)
	def __str__(self):
		return 'name:%s type:%s' % (self.path, self.filename)	
	class Admin:
		pass
class Comment(models.Model):
	#path
	mediaPath   =  models.CharField(max_length=200,null=True)
	username    = models.CharField(max_length=50,null=True)
	content 	= models.CharField(max_length=250,null=True)
	commentTime = models.DateTimeField(auto_now_add=True, blank=True)
	commentUser = models.CharField(max_length=50,null=True)
	def __str__(self):
		return 'name:%s path:%s' % (self.username, self.mediaPath)	
	class Admin:
		pass
class Score(models.Model):
	#path
	mediaPath =  models.CharField(max_length=200,null=True)
	#owner
	username  = models.CharField(max_length=50,null=True)
	score	  = models.FloatField(default=0.0,null=True)
	scoreTime = models.DateTimeField(auto_now_add=True, blank=True)
	scoreUser = models.CharField(max_length=50,null=True)
	def __str__(self):
		return 'name:%s path:%s' % (self.username, self.mediaPath)	
	class Admin:
		pass
class Download(models.Model):
	IP 			 = models.IPAddressField(null=True)
	downloadTime = models.DateTimeField(auto_now_add=True,null=True)
	username     = models.CharField(max_length=50,null=True)
	path 		 = models.CharField(max_length=200,null=True)
	downloadUser = models.CharField(max_length=50,null=True)
	def __str__(self):
		return self.IP
	class Admin:
		pass

class Contactlist(models.Model):
	username     = models.CharField(max_length=50,null=True)
	contact      = models.CharField(max_length=50,null=True)
	ifFriend	 = models.CharField(max_length=50,default='No')

class Friendlist(models.Model):
	username     = models.CharField(max_length=50,null=True)
	friend       = models.CharField(max_length=50,null=True)

class Blocklist(models.Model):
	username     = models.CharField(max_length=50,null=True)
	blockedUser  = models.CharField(max_length=50,null=True)

# add to block user to view 
class BlocklistAdd(models.Model):
	username     = models.CharField(max_length=50,null=True)
	blockedUser  = models.CharField(max_length=50,null=True)

class SendMessage(models.Model):
	sender     = models.CharField(max_length=50,null=True)
	reciever   = models.CharField(max_length=50,null=True)
	content    = models.CharField(max_length=250,null=True)
	#deault: not read
	ifRead     = models.CharField(max_length=50, default='No')

class Playlist(models.Model):
	username   = models.CharField(max_length=50,null=True)
	path 	   = models.CharField(max_length=200,null=True)
	type	   = models.CharField(max_length=250,null=True)
	playTime   = models.DateTimeField(auto_now_add=True,null=True)

class Subscribe(models.Model):
	username	   = models.CharField(max_length=50,null=True)
	subscribedUser = models.CharField(max_length=50,null=True)

class FavoriteList(models.Model):
	username	= models.CharField(max_length=50,null=True)
	listName 	= models.CharField(max_length=50,null=True)

class FavoriteListMedia(models.Model):
	username    = models.CharField(max_length=50,null=True)
	listName 	= models.CharField(max_length=50,null=True)
	# correspoding to foreign key
	path 	    = models.CharField(max_length=200,null=True)
	type	    = models.CharField(max_length=50,null=True)
