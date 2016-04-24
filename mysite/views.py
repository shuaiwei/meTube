from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render_to_response

# enter main page
def base(request):
    request.session['mediaType'] = 'all'
    images = Media.objects.filter(type="image").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    videos = Media.objects.filter(type="video").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    audios = Media.objects.filter(type="audio").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    request.session['image'] = images #type is single
    request.session['video'] = videos
    request.session['audio'] = audios
    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images, 'videos': videos, 'audios':audios})

def login(request):
	return render_to_response('login.html')
def logout(request):
    try:
        del request.session['username']
        del request.session['mediaType']
        del request.session['image']
        del request.session['video']
        del request.session['audio']
        del request.session['favoritelistName']

    except KeyError:
        pass
    return render_to_response('login.html')
# def blog(request):
# 	return render_to_response('blog.html')
def register(request):
	return render_to_response('register.html')

from forms import accountForm

from django.http import HttpResponseRedirect
from modelView.models import *


def returnToMain(request):
    #very important
    request.session['mediaType'] = 'all'
    images = Media.objects.filter(type="image").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    videos = Media.objects.filter(type="video").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    audios = Media.objects.filter(type="audio").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    request.session['image'] = images #type is single
    request.session['video'] = videos
    request.session['audio'] = audios
    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images, 'videos': videos, 'audios':audios})

def edit(request):
    #! just use the first 
    firstname =  Account.objects.filter(username=request.session.get('username')).values_list('firstname',flat=True)[0]
    lastname =  Account.objects.filter(username=request.session.get('username')).values_list('lastname',flat=True)[0]
    company =  Account.objects.filter(username=request.session.get('username')).values_list('company',flat=True)[0]
    address =  Account.objects.filter(username=request.session.get('username')).values_list('address',flat=True)[0]

    return render_to_response('editProfile.html',{'username':request.session.get('username'),
            'firstname':firstname, 'lastname':lastname, 
            'company':company, 'address':address })

def editUpdate(request):
    update = False
    if request.method == 'POST':
        if  request.POST.get('firstname', ''):
            t = Account.objects.get(username=request.session.get('username'))
            update = update or (t.firstname != request.POST['firstname'])
            t.firstname = request.POST['firstname']
            t.save()
        

        if  request.POST.get('lastname', ''):
            t = Account.objects.get(username=request.session.get('username'))
            update = update or  (t.lastname != request.POST['lastname'])
            t.lastname = request.POST['lastname']
            t.save()
       

        if request.POST.get('company', ''):
            t = Account.objects.get(username=request.session.get('username'))
            update = update or  (t.company != request.POST['company'])
            t.company = request.POST['company']
            t.save()
        

        if request.POST.get('address', ''):
            t = Account.objects.get(username=request.session.get('username'))
            update = update or  (t.address != request.POST['address'])
            t.address = request.POST['address']
            t.save() 
     
        if update:
            success = "Update your profile successfully !"
        else:
            success = ''
        modifyPassword = ''
        if request.POST.get('password', '') and request.POST.get('confirm_password', ''):
            if request.POST['password'] == request.POST['confirm_password']: 
                modifyPassword = "Modify password successfully !"
                t = Account.objects.get(username=request.session.get('username'))
                t.password = request.POST['password']
                t.save() 

    firstname =  Account.objects.filter(username=request.session.get('username')).values_list('firstname',flat=True)[0]
    lastname =  Account.objects.filter(username=request.session.get('username')).values_list('lastname',flat=True)[0]
    company =  Account.objects.filter(username=request.session.get('username')).values_list('company',flat=True)[0]
    #"values" get method can also be used,use index
    address =  Account.objects.filter(username=request.session.get('username')).values('address')[0]['address']

    return render_to_response('editProfile.html',{'username':request.session.get('username'),
        'firstname':firstname, 'lastname':lastname, 'company':company, 'address':address,
        'success':success, 'modifyPassword':modifyPassword})


def metaUpdate(request):
    # when doing meta updating, hte must edit his own media, so no blocking
    update = False
    path=''
    if request.method == 'POST':
        if  request.POST.get('path', ''):
            path = request.POST['path']
            path = path[1:]

        if  request.POST.get('meta', ''):
            t = Media.objects.get(path=path)
            update = update or (t.meta != request.POST['meta'])
            t.meta = request.POST['meta']
            t.save()

        if  request.POST.get('keyword', ''):
            t = Media.objects.get(path=path)
            update = update or  (t.keyword != request.POST['keyword'])
            t.keyword = request.POST['keyword']
            t.save()
    aveScore =  Media.objects.filter(path=path).values_list('aveScore',flat=True)[0]
    meta =  Media.objects.filter(path=path).values_list('meta',flat=True)[0]
    keyword =  Media.objects.filter(path=path).values_list('keyword',flat=True)[0]
    #"values" get method can alse be used
    mediaType = Media.objects.filter(path=path).values_list('type',flat=True)[0]
    numOfViewer = Media.objects.filter(path=path).values_list('numOfViewer',flat=True)[0]
    uploader = Media.objects.filter(path=path).values_list('username',flat=True)[0]
    # must have '/'
    path = '/' + path
        #use medias here
    ifEdit = True
    medias = request.session.get(mediaType)  # it is mediaType
    favoriteList = FavoriteList.objects.filter(username=request.session.get('username')).values_list('listName',flat=True)

    return render_to_response('singleMediaBrowser.html',{'favoriteList':favoriteList,'uploader':uploader,'numOfViewer':numOfViewer,'aveScore':aveScore,'ifEdit':ifEdit,'type':mediaType,'username':request.session.get('username'),
        'meta':meta, 'keyword':keyword,'media': path, 'medias':medias})


def registerCheck(request):
    errors = []

    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append('Please enter a username!')
        if not request.POST.get('password', ''):
            errors.append('Please enter a password!')
        if not request.POST.get('passwordConfirm', ''):
            errors.append('Please confirm the password!')
        # if request.POST.get('email') and '@' not in request.POST['email']:
        #     errors.append('Enter a valid e-mail address.')
        if not errors:
            # form = registerForm(request.POST)
            # if form.is_valid():
            #     cf = form.cleaned_data (must have form.is_valid if use it)
            if not Account.objects.filter(username=request.POST['username']).exists():
                
                if request.POST['password'] != request.POST['passwordConfirm']:
                    errors.append('The password doesn\'t match')
                    return render(request, 'register.html', {'errors': errors})

                p = Account(
                    username=request.POST['username'],
                    password=request.POST['password']
                )
                p.save()
                username = request.POST['username']
                return render(request, 'register.html', {'success': username + ' has been registered successfully!' })
            else:
                errors.append('Username already exists. Please use a different username.')


    return render(request, 'register.html', {'errors': errors})

def loginCheck(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append('Please enter a username!')
        if not request.POST.get('password', ''):
            errors.append('Please enter a password!')
        if not errors:
            errors = []
            try:
                result = Account.objects.get(username=request.POST['username'])
            except Account.DoesNotExist:
                errors.append('Username already does not exists.')
            if not errors:
                username = request.POST['username'];
                if request.POST['password'] == Account.objects.get(username=username).password:
                    request.session['username'] = username
                    images = Media.objects.filter(username=username, type="image").values_list('path',flat=True)
                    videos = Media.objects.filter(username=username, type="video").values_list('path',flat=True)
                    audios = Media.objects.filter(username=username, type="audio").values_list('path',flat=True)
                    request.session['mediaType'] = 'personal' #then we can edit
                    # images = Media.objects.filter(type="image").values_list('path',flat=True)
                    # videos = Media.objects.filter(type="video").values_list('path',flat=True)
                    # audios = Media.objects.filter(type="audio").values_list('path',flat=True)
                    request.session['image'] = images #type is single
                    request.session['video'] = videos
                    request.session['audio'] = audios
                    return render(request, 'allMediaBrowser.html', {'username': username, 'images': images, 'videos': videos, 'audios': audios})
                else:
                    errors.append('Passwords don\'t match. Try again?')

    return render(request, 'login.html', {'errors': errors})

# def browser(request): # for no login user
#      return render(request, 'browser.html')

def upload(request): 
     return render(request, 'upload.html',{'username': request.session.get('username')})

from forms import mediaForm
from django.template import RequestContext
import datetime
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

import subprocess
import PIL
from PIL import Image
import shutil

def uploadProcess(request):
    uploadResult = ''
    meta=''
    keyword=''
    if request.method == 'POST':
        if request.POST.get('meta', ''):
            meta = request.POST['meta']
        if request.POST.get('keyword', ''):
            keyword = request.POST['keyword']
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        # new_file = UploadFile(file = request.FILES['theFileInput'])
        file_list =request.FILES.getlist('theFileInput')
        if not file_list:
            uploadResult = "Please select at least one file!"
            return render_to_response('upload.html', {'uploadResult':uploadResult}, context_instance=RequestContext(request))
        # if 'HTTP_X_FORWARDED_FOR' in request.META:
       
        for afile in file_list:

            new_file = Media(meta=meta, keyword=keyword, IP = get_client_ip(request), username =request.session.get('username'), path = afile, type = afile.content_type.split('/')[0], filename = afile.name)
            new_file.save()
            imageType = ['jpg','png','bmp','jpeg']
            videoType = ['flv','ogv','mp4']
            audioType = ['mp3']
            if afile.name.split(".")[1] in imageType:
                name = afile.name
                filePath = Media.objects.filter(username=request.session.get('username')).values_list('path',flat=True).order_by('-id')[0]
                #order is important
                Media.objects.filter(username=request.session.get('username'), path=filePath).delete()
                img = Image.open(filePath)
                #width = 500
                #height = 340
                img = img.resize((500, 340), Image.BILINEAR)
                #cover orignal file directly
                img.save(filePath)
                new_file = Media(meta=meta, keyword=keyword, IP = get_client_ip(request), username =request.session.get('username'), path = filePath, type = 'image', filename = name)
                new_file.save()

            elif afile.name.split(".")[1] in videoType:
                filePath = Media.objects.filter(username=request.session.get('username')).values_list('path',flat=True).order_by('-id')[0]
                Media.objects.filter(username=request.session.get('username'), path=filePath).delete()

                outputTempFile = filePath.split('.')[0] +'######temp######.mp4'
                outputFile = filePath.split('.')[0] +'.mp4'
                name = afile.name.split('.')[0] + '.mp4'
                #width=560 #height=320
                command = ['avconv', '-i', filePath, '-strict', 'experimental', '-vcodec', 'libx264',  '-vf',
                 "scale=iw*min(560/iw\,320/ih):ih*min(560/iw\,320/ih), pad=560:320:(560-iw*min(560/iw\,320/ih))/2:(320-ih*min(560/iw\,320/ih))/2", outputTempFile]
                subprocess.call(command)
                #care order
                shutil.move(outputTempFile, outputFile)
                #should not delete
                #os.remove(filePath)

                new_file = Media(meta=meta, keyword=keyword, IP = get_client_ip(request), username =request.session.get('username'), path = outputFile, type = 'video', filename = name)
                new_file.save()
            else: 
                pass
        uploadResult = "Upload successfully !"
        return render_to_response('upload.html', {'username':request.session.get('username'), 'uploadResult':uploadResult}, context_instance=RequestContext(request))
    else:
        uploadResult ="Uploading failed !"
        return render_to_response('upload.html', {'uploadResult':uploadResult}, context_instance=RequestContext(request))

def test(request):
    return render_to_response('test.html')

# if list out of range, the path / image is not right , lack of '/', or extra '/'
def mediaClick(request):
    media=''
    ifEdit = False
    ifBlock = False
    playlistDelete = False
    playlistShow = False
    favoritelistDelete = False
    favoritelistShow = False
    comments = ''
    numOfViewer = 0
    if request.method == 'POST':
        if  request.POST.get('image', ''):
            media = request.POST['image']
        elif request.POST.get('video', ''):
            media = request.POST['video']
        elif request.POST.get('audio', ''):
            media = request.POST['audio']
        else:
            pass
    media = media[1:]
    #path can decide image uniquely
    owner = Media.objects.filter(path=media).values_list('username',flat=True)[0]
    aveScore =  Media.objects.filter(path=media).values_list('aveScore',flat=True)[0]
    meta =  Media.objects.filter(path=media).values_list('meta',flat=True)[0]
    keyword =  Media.objects.filter(path=media).values_list('keyword',flat=True)[0]
    mediaType = Media.objects.filter(path=media).values_list('type',flat=True)[0]
    comments = Comment.objects.filter(mediaPath = media).values_list('content',flat=True).order_by('-commentTime')
    uploader = Media.objects.filter(path=media).values_list('username',flat=True)[0]

    #prevent scoring by user himself
    if request.session.get('username') == owner:
        ifEdit = True
    else: 
        #can not use filter since no attribute in Queryset, should include it in models
        t = Media.objects.get(path=media)
        t.numOfViewer = t.numOfViewer + 1
        t.save()
        t = Playlist(username=request.session.get('username'), type=mediaType, path=media)
        t.save()
    if request.session.get('mediaType') == 'personal':   
        ifEdit = True
    if request.session.get('mediaType') == 'playlist':   
        playlistDelete = True
        playlistShow = True
    if request.session.get('mediaType') == 'favoritelist':   
        favoritelistDelete = True
        favoritelistShow = True
    numOfViewer = Media.objects.filter(path=media).values_list('numOfViewer',flat=True)[0]
    #block list
    # block vistor
    if not request.session.get('username') and '' in Blocklist.objects.filter(username=owner).values_list('blockedUser',flat=True):
        ifBlock = True
    if request.session.get('username') in Blocklist.objects.filter(username=owner).values_list('blockedUser',flat=True):
        ifBlock = True
    media = '/' + media
    medias = request.session.get(mediaType)  # it is mediaType
    #it does not matter whether request.session.get('username') exist.
    favoriteList = FavoriteList.objects.filter(username=request.session.get('username')).values_list('listName',flat=True)
    listName = request.session.get('favoritelistName')
    return render_to_response('singleMediaBrowser.html',{'playlistShow':playlistShow,'favoritelistShow':favoritelistShow,'listName':listName,'favoritelistDelete':favoritelistDelete,'favoriteList':favoriteList, 'playlistDelete':playlistDelete,'ifBlock':ifBlock, 'uploader':uploader,'numOfViewer':numOfViewer,'aveScore':aveScore,'comments':comments,'ifEdit': ifEdit,'type':mediaType, 'username':request.session.get('username'),
            'meta':meta, 'keyword':keyword,'media': media, 'medias':medias})

import os 
            
def mediaDelete(request):
    media=''
    # needed, otherwise, image is local
    if request.method == 'POST':
        if  request.POST.get('image', ''):
            media = request.POST['image']
        elif  request.POST.get('video', ''):
            media = request.POST['video']
        elif  request.POST.get('audio', ''):
            media = request.POST['audio']
        else:
            pass
    media = media[1:]
    #must be put before delete funtion
    mediaType = Media.objects.filter(path=media).values_list('type',flat=True)[0]

    Media.objects.filter(path=media).delete()
    Comment.objects.filter(mediaPath=media).delete()
    Score.objects.filter(mediaPath=media).delete()
    Playlist.objects.filter(path=media).delete()
    FavoriteListMedia.objects.filter(path=media).delete()

    os.remove(media)
    # update medias variables syncly 
    medias = request.session.get(mediaType)  # it is mediaType
    medias = list(medias)
    medias.remove( media.decode('utf8'))
    #Do not forget to update session here
    request.session[mediaType] = medias

    #medias = Media.objects.filter(username=request.session.get('username'), type=mediaType).values_list('path',flat=True)
    delete = "You have deleted it successfully !"
    return render_to_response('singleMediaBrowser.html', {'type': mediaType,'username':request.session.get('username'), 'medias':medias, 'delete':delete})

def allMediaBrowser(request):
    request.session['mediaType'] = 'all'
    images = Media.objects.filter(type="image").values_list('path',flat=True)
    videos = Media.objects.filter(type="video").values_list('path',flat=True)
    audios = Media.objects.filter(type="audio").values_list('path',flat=True)
    request.session['image'] = images #type is single
    request.session['video'] = videos
    request.session['audio'] = audios
    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images, 'videos': videos, 'audios':audios})
   
def allMediaBrowserPersonal(request):
    request.session['mediaType'] = 'personal'
    if 'username' in request.session:
        images = Media.objects.filter(username=request.session.get('username'),type="image").values_list('path',flat=True)
        videos = Media.objects.filter(username=request.session.get('username'),type="video").values_list('path',flat=True)
        audios = Media.objects.filter(username=request.session.get('username'),type="audio").values_list('path',flat=True)
        request.session['image'] = images #type is single
        request.session['video'] = videos
        request.session['audio'] = audios
        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images, 'videos': videos, 'audios':audios})
    else:
        images = Media.objects.filter(type="image").values_list('path',flat=True)
        videos = Media.objects.filter(type="video").values_list('path',flat=True)
        audios = Media.objects.filter(type="audio").values_list('path',flat=True)
        request.session['image'] = images #type is single
        request.session['video'] = videos
        request.session['audio'] = audios
        return render_to_response('allMediaBrowser.html', {'images':images,'videos': videos, 'audios':audios})
def imageBrowser(request):
    request.session['mediaType'] = 'all'
    images = Media.objects.filter(type="image").values_list('path',flat=True)
    request.session['image'] = images #type is single

    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images})

def imageBrowserPersonal(request):
    request.session['mediaType'] = 'personal'
    if 'username' in request.session:
        images = Media.objects.filter(username=request.session.get('username'),type="image").values_list('path',flat=True)
        request.session['image'] = images #type is single
        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images})
    else:
        images = Media.objects.filter(type="image").values_list('path',flat=True)
        request.session['image'] = images #type is single
        return render_to_response('allMediaBrowser.html', {'images':images})

def videoBrowser(request):
    request.session['mediaType'] = 'all'
    videos = Media.objects.filter(type="video").values_list('path',flat=True)
    request.session['video'] = videos
    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'videos':videos})

def videoBrowserPersonal(request):
    request.session['mediaType'] = 'personal'
    if 'username' in request.session:
        videos = Media.objects.filter(username=request.session.get('username'),type="video").values_list('path',flat=True)
        request.session['video'] = videos  
        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'videos':videos})
    else:
        videos = Media.objects.filter(type="video").values_list('path',flat=True)
        request.session['video'] = videos
        return render_to_response('allMediaBrowser.html', {'videos':videos})

def audioBrowser(request):
    request.session['mediaType'] = 'all'
    audios = Media.objects.filter(type="audio").values_list('path',flat=True)
    request.session['audio'] = audios
    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'audios':audios})

def audioBrowserPersonal(request):
    request.session['mediaType'] = 'personal'
    if 'username' in request.session:
        audios = Media.objects.filter(username=request.session.get('username'),type="audio").values_list('path',flat=True)
        request.session['audio'] = audios
        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'audios':audios})
    else:
        audios = Media.objects.filter(type="audio").values_list('path',flat=True)
        request.session['audio'] = audios
        return render_to_response('allMediaBrowser.html', {'audios':audios})

from django.db.models import Q

def search(request):
    query = ''
    mediaType = ''
    if request.method == 'POST':
        if  request.POST.get('query', ''):
            query = request.POST['query']
        else: # prevent empty query
            return render_to_response('allMediaBrowser.html', {'username':request.session.get('username')})
        if  request.POST.get('mediaType', ''):
            mediaType = request.POST['mediaType']
    
    request.session['mediaType'] = 'search'
    queryArray = query.split() 
    #use another template here
    if mediaType =='allMedia':
        images = Media.objects.filter(Q(type='image'), reduce(lambda x, y: x | y, 
            [Q(keyword__contains=queryword) for queryword in queryArray])).values_list('path',flat=True)
        videos = Media.objects.filter(Q(type='video'), reduce(lambda x, y: x | y, 
            [Q(keyword__contains=queryword) for queryword in queryArray])).values_list('path',flat=True)
        audios = Media.objects.filter(Q(type='audio'), reduce(lambda x, y: x | y, 
            [Q(keyword__contains=queryword) for queryword in queryArray])).values_list('path',flat=True)
        request.session['image'] = images #type is single
        request.session['video'] = videos
        request.session['audio'] = audios
        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'),'images':images,'videos': videos, 'audios':audios})
    else:
        medias = Media.objects.filter(Q(type=mediaType), reduce(lambda x, y: x | y,[Q(keyword__contains=queryword) for queryword in queryArray])).values_list('path',flat=True)
        # request.session['medias'] = medias
        request.session[mediaType]= medias
        return render(request, 'searchResultBrowser.html', {'username':request.session.get('username'),'type':mediaType, 'medias':medias})

import time
from django.db.models import Avg

def comment(request):
    commentContent = ''
    score = 0.0
    path=''
    update = False
    aveScore = 0
    owner = ''
    if request.method == 'POST':
        if  request.POST.get('path', ''):
            path = request.POST['path']
            path = path[1:]
            owner = Media.objects.filter(path=path).values_list('username',flat=True)[0]
        if  request.POST.get('score', ''):
            score = request.POST['score']
            username = request.session.get('username')
            scoreTime = time.asctime( time.localtime(time.time()) )
            t = Score(mediaPath = path, score = score, scoreUser=username,username = owner)
            t.save()
            t = Media.objects.get(path=path)
            #can not use objects.get() for Score since multiple result can produce
            t.aveScore = Score.objects.filter(mediaPath = path).aggregate(Avg('score')).values()[0]
            aveScore = t.aveScore
            t.save()
        if  request.POST.get('commentContent', ''):
            content = request.POST['commentContent']
            username = request.session.get('username')
            commentTime = time.asctime( time.localtime(time.time()) )
            #error when username is None
            if username:
                content = content + '\nBy user ' + username + ' at ' + commentTime
            else:
                content = content + '\nBy visitor ' + ' at ' + commentTime

            t = Comment(mediaPath = path, content = content, commentUser=username)
            t.save()
    comments = Comment.objects.filter(mediaPath = path).values_list('content',flat=True).order_by('-commentTime')
    mediaType = Media.objects.filter(path=path).values_list('type',flat=True)[0]
    numOfViewer = Media.objects.filter(path=path).values_list('numOfViewer',flat=True)[0]
    uploader = Media.objects.filter(path=path).values_list('username',flat=True)[0]

    # must have '/'
    path = '/' + path
    
    #medias = Media.objects.filter(type=mediaType).values_list('path',flat=True)
    medias = request.session.get(mediaType)  # it is mediaType
    favoriteList = FavoriteList.objects.filter(username=request.session.get('username')).values_list('listName',flat=True)

    return render_to_response('singleMediaBrowser.html',{'favoriteList':favoriteList,'uploader':uploader,'numOfViewer':numOfViewer,'aveScore':aveScore,'type':mediaType,'username':request.session.get('username'),
        'comments':comments,'media': path, 'medias':medias})

def download(request):
    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = ''
    username = ''
    if request.method == 'POST':
        if  request.POST.get('path', ''):
            path = request.POST['path']
            path = path[1:]
            owner = Media.objects.filter(path=path).values_list('username',flat=True)[0]
            filename = Media.objects.filter(path=path).values_list('filename',flat=True)[0]
            username = Media.objects.filter(path=path).values_list('username',flat=True)[0]
    t = Download(username = username, IP = get_client_ip(request), downloadUser =request.session.get('username'), path = path)
    t.save()

    filePath     =  path # Select your file here.
    download_name = filename
    wrapper      = FileWrapper(open(filePath))
    content_type = mimetypes.guess_type(filePath)[0]
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filePath)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response

def friend(request):
    username = request.session.get('username')
    friendlist = Friendlist.objects.filter(username=username).values_list('friend',flat=True)
    return render_to_response('friend.html',{'username':username, 'friendlist':friendlist})

def block(request):
    username = request.session.get('username')
    blocklist = Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True)
    blocklistAdd = BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True)

    return render_to_response('block.html',{'blocklistAdd':blocklistAdd,'username':username, 'blocklist':blocklist})

def searchFriend(request):
    searchedFriend = ''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('query', ''):
            searchedFriend = request.POST['query']
    searchedFriend = Account.objects.filter(username=searchedFriend).values_list('username',flat=True)
    # delete null error
    if searchedFriend: 
        searchedFriend = searchedFriend[0]
    #prevent search himself
    if searchedFriend == request.session.get('username'):
        searchedFriend =''
    friendlist = Friendlist.objects.filter(username=username).values_list('friend',flat=True)
    return render_to_response('friend.html',{'ifSearch':True, 'searchedFriend':searchedFriend,'username':username, 'friendlist':friendlist})

def searchBlock(request):
    searchedBlock = ''
    blockVistor = False
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('query', ''):
            searchedBlock = request.POST['query']
    if not searchedBlock:
        blockVistor = True
    searchedBlock = Account.objects.filter(username=searchedBlock).values_list('username',flat=True)
    # add 'if' to stop null error
    if searchedBlock: 
        searchedBlock = searchedBlock[0]
    #prevent search himself
    if searchedBlock == request.session.get('username'):
        searchedBlock =''
    blocklist = Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True)
    blocklistAdd = BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True)

    return render_to_response('block.html',{'blocklistAdd':blocklistAdd,'blockVistor':blockVistor,'ifSearch':True, 'searchedBlock':searchedBlock,'username':username, 'blocklist':blocklist})

def addFriend(request):
    searchedFriend = ''
    blockAddFriend = False
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('searchedFriend', ''):
            searchedFriend = request.POST['searchedFriend']
    if  searchedFriend.decode('utf8') in Friendlist.objects.filter(username=username).values_list('friend',flat=True):
        searchedFriend = ''
    elif  searchedFriend.decode('utf8') in Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True):
        searchedBlock = ''
    elif searchedFriend.decode('utf8') in BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True):
        searchedBlock = ''
        blockAddFriend = True
    else: 
        t = Friendlist(username=username, friend=searchedFriend)
        t.save()
        # add the friend to contactlist automatically.
        if searchedFriend.decode('utf8') not in Contactlist.objects.filter(username=username).values_list('contact',flat=True):
            t = Contactlist(username=username, contact=searchedFriend, ifFriend = True)
            t.save()    
    friendlist = Friendlist.objects.filter(username=username).values_list('friend',flat=True)
    return render_to_response('friend.html',{'blockAddFriend':blockAddFriend,'ifAdd':True,'addedUser':searchedFriend,'username':username, 'friendlist':friendlist})

def addBlock(request):
    searchedBlock = ''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('searchedBlock', ''):
            searchedBlock = request.POST['searchedBlock']
    if  searchedBlock.decode('utf8') in Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True):
        searchedBlock = ''
    #elif  searchedBlock.decode('utf8') in Friendlist.objects.filter(username=username).values_list('friend',flat=True):
        #searchedBlock = ''
    elif  '' in Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True):
        searchedBlock = ''
    else: 
        if searchedBlock =='[]':
            #blockedUser=''
            t = Blocklist(username=username, blockedUser='')
            t.save()
        else:
            t = Blocklist(username=username, blockedUser=searchedBlock)
            t.save()
    blocklist = Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True)
    blocklistAdd = BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True)

    return render_to_response('block.html',{'blocklistAdd':blocklistAdd,'ifAdd':True,'addedUser':searchedBlock,'username':username, 'blocklist':blocklist})

def sendAndDelete(request):
    friend=''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('delete', ''):
            friend = request.POST['friend']
            Friendlist.objects.filter(username=username,friend=friend).delete()
        if  request.POST.get('send', ''):
            reciever = request.POST['friend']
            return render_to_response('sendMessage.html',{'username':username,'reciever':reciever})

    friendlist = Friendlist.objects.filter(username=username).values_list('friend',flat=True)
    return render_to_response('friend.html',{'username':username, 'friendlist':friendlist})

def deleteBlockedUser(request):
    blockedUser=''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('delete', ''):
            blockedUser = request.POST['blockedUser']
            Blocklist.objects.filter(username=username,blockedUser=blockedUser).delete()

    blocklist = Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True)
    blocklistAdd = BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True)

    return render_to_response('block.html',{'blocklistAdd':blocklistAdd,'username':username, 'blocklist':blocklist})


# In sendAndDelete, we give the reciever.
def sendMessage(request):
    infoContent = ''
    reciever = ''
    username = request.session.get('username')
    sendTime = time.asctime( time.localtime(time.time()) )
    if request.method == 'POST':
        if  request.POST.get('infoContent', ''):
            infoContent = request.POST['infoContent']
            infoContent = infoContent + '\nBy user ' + username + ' at ' + sendTime
        if  request.POST.get('reciever', ''):
            reciever = request.POST['reciever']
    if  infoContent:
        success = 'The message has been sent successfully!'
        t = SendMessage(sender=username, reciever=reciever,content=infoContent)
        t.save()
    else:
        success = 'The message can not be empty.'
    return render_to_response('sendMessage.html',{'success':success,'username':username,'reciever':reciever})

def newMessage(request):
    username = request.session.get('username')
    messages = SendMessage.objects.filter(reciever=username, ifRead='No').values_list('content',flat=True)
    return render_to_response('newMessage.html',{'username':username,'messages':messages})
    # can not be used here, SendMessage.objects.filter(reciever=username, ifRead='No').update(ifRead='Yes')

def markRead(request):
    username = request.session.get('username')
    SendMessage.objects.filter(reciever=username, ifRead='No').update(ifRead='Yes')
    return render_to_response('newMessage.html',{'username':username})

def mostViewed(request):
    request.session['mediaType'] = 'all'
    images = Media.objects.filter(type="image").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    videos = Media.objects.filter(type="video").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    audios = Media.objects.filter(type="audio").values_list('path',flat=True).order_by('-numOfViewer')[:5]
    request.session['image'] = images #type is single
    request.session['video'] = videos
    request.session['audio'] = audios
    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images, 'videos': videos, 'audios':audios})

def mostRecentUpload(request):
    request.session['mediaType'] = 'all'
    images = Media.objects.filter(type="image").values_list('path',flat=True).order_by('-uploadTime')[:5]
    videos = Media.objects.filter(type="video").values_list('path',flat=True).order_by('-uploadTime')[:5]
    audios = Media.objects.filter(type="audio").values_list('path',flat=True).order_by('-uploadTime')[:5]
    request.session['image'] = images #type is single
    request.session['video'] = videos
    request.session['audio'] = audios
    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images, 'videos': videos, 'audios':audios})

def playlist(request):
    # use personal here to delete in playlist
    request.session['mediaType'] = 'playlist'
    username = request.session.get('username')
    images = Playlist.objects.filter(type="image",username=username).values_list('path',flat=True).distinct().order_by('-playTime')
    videos = Playlist.objects.filter(type="video",username=username).values_list('path',flat=True).distinct().order_by('-playTime')
    audios = Playlist.objects.filter(type="audio",username=username).values_list('path',flat=True).distinct().order_by('-playTime')
    request.session['image'] = images #type is single
    request.session['video'] = videos
    request.session['audio'] = audios
    return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images, 'videos': videos, 'audios':audios})
def playlistDelete(request):
    path=''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('path', ''):
            path = request.POST['path']
            path = path[1:]
    mediaType = Playlist.objects.filter(path=path).values_list('type',flat=True)[0]
    Playlist.objects.filter(path=path).delete()


    images = Playlist.objects.filter(type="image",username=username).values_list('path',flat=True).distinct().order_by('-playTime')
    videos = Playlist.objects.filter(type="video",username=username).values_list('path',flat=True).distinct().order_by('-playTime')
    audios = Playlist.objects.filter(type="audio",username=username).values_list('path',flat=True).distinct().order_by('-playTime')

    request.session['image'] = images #type is single
    request.session['video'] = videos
    request.session['audio'] = audios

    medias = request.session.get(mediaType)  # it is mediaType

    delete = "You have deleted it from playlist successfully !"
    return render_to_response('singleMediaBrowser.html', {'type': mediaType,'username':request.session.get('username'), 'medias':medias, 'delete':delete})

def subscribe(request):
    path=''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('path', ''):
            path = request.POST['path']
            path = path[1:]
    subscribedUser = Media.objects.filter(path=path).values_list('username',flat=True)[0]
    if  subscribedUser not in Subscribe.objects.filter(username=username).values_list('subscribedUser',flat=True):
        t = Subscribe(username=username, subscribedUser=subscribedUser)
        t.save()
        subscribeSuccess = 'You subscribed that user successfully!'
    else:
        subscribeSuccess = 'You have already subscribed that user before.'
    aveScore =  Media.objects.filter(path=path).values_list('aveScore',flat=True)[0]
    keyword =  Media.objects.filter(path=path).values_list('keyword',flat=True)[0]
    comments = Comment.objects.filter(mediaPath = path).values_list('content',flat=True).order_by('-commentTime')
    mediaType = Media.objects.filter(path=path).values_list('type',flat=True)[0]
    numOfViewer = Media.objects.filter(path=path).values_list('numOfViewer',flat=True)[0]
    uploader = Media.objects.filter(path=path).values_list('username',flat=True)[0]

    # must have '/'
    path = '/' + path
    
    #medias = Media.objects.filter(type=mediaType).values_list('path',flat=True)
    medias = request.session.get(mediaType)  # it is mediaType
    favoriteList = FavoriteList.objects.filter(username=username).values_list('listName',flat=True)

    return render_to_response('singleMediaBrowser.html',{'favoriteList':favoriteList,'subscribeSuccess':subscribeSuccess,'uploader':uploader,'numOfViewer':numOfViewer,'aveScore':aveScore,'type':mediaType,'username':request.session.get('username'),
        'comments':comments,'media': path, 'medias':medias})

def subscribeList(request):
    username = request.session.get('username')
    subscribedList = Subscribe.objects.filter(username=username).values_list('subscribedUser',flat=True)
    return render_to_response('subscribedList.html',{'username':username,'subscribedList':subscribedList})

def subscribeViewAndDelete(request):
    username = request.session.get('username')
    subscribedUser=''
    if request.method == 'POST':
        if request.POST.get('view', ''):
            subscribedUser = request.POST['subscribedUser']
            images = Media.objects.filter(username=subscribedUser, type="image").values_list('path',flat=True)
            videos = Media.objects.filter(username=subscribedUser, type="video").values_list('path',flat=True)
            audios = Media.objects.filter(username=subscribedUser, type="audio").values_list('path',flat=True)
            request.session['image'] = images #type is single
            request.session['video'] = videos
            request.session['audio'] = audios
            return render(request, 'allMediaBrowser.html', {'username': username, 'images': images, 'videos': videos, 'audios': audios})
        if  request.POST.get('delete', ''):
            subscribedUser = request.POST['subscribedUser']
            Subscribe.objects.filter(username=username,subscribedUser=subscribedUser).delete()
    subscribedList = Subscribe.objects.filter(username=username).values_list('subscribedUser',flat=True)
    return render_to_response('subscribedList.html',{'username':username, 'subscribedList':subscribedList})

def favoriteList(request):
    request.session['mediaType'] = 'favoritelist'
    username = request.session.get('username')
    favoriteList = FavoriteList.objects.filter(username=username).values_list('listName',flat=True)
    return render_to_response('favoriteList.html',{'username':username, 'favoriteList':favoriteList})
def addFavoriteList(request):
    username = request.session.get('username')
    listName = ''
    if request.method == 'POST':
        if request.POST.get('listName', ''):
            listName = request.POST['listName']
    if not listName:
        favoriteListSuccess = 'The favorite list can not be empty!'
    elif  listName not in FavoriteList.objects.filter(username=username).values_list('listName',flat=True):
        t = FavoriteList(username = username, listName = listName)
        t.save()
        favoriteListSuccess = 'You create the new favorite list successfully!'
    else:
        favoriteListSuccess = 'The favorite have already been there.'
        
    favoriteList = FavoriteList.objects.filter(username=username).values_list('listName',flat=True)
    return render_to_response('favoriteList.html',{'favoriteListSuccess':favoriteListSuccess,'username':username, 'favoriteList':favoriteList})

def deleteAndViewFavoriteList(request):
    username = request.session.get('username')
    listName=''
    if request.method == 'POST':
        if request.POST.get('view', ''):
            listName = request.POST['listName']
            request.session['favoritelistName'] = listName
            images = FavoriteListMedia.objects.filter(username=username, listName = listName, type="image").values_list('path',flat=True)
            videos = FavoriteListMedia.objects.filter(username=username, listName = listName, type="video").values_list('path',flat=True)
            audios = FavoriteListMedia.objects.filter(username=username, listName = listName, type="audio").values_list('path',flat=True)
            request.session['image'] = images #type is single
            request.session['video'] = videos
            request.session['audio'] = audios
            #!!!! add listName here not the one below render_to_response
            return render(request, 'allMediaBrowser.html', {'listName':listName,'username': username, 'images': images, 'videos': videos, 'audios': audios})
        if  request.POST.get('delete', ''):
            listName = request.POST['listName']
            FavoriteList.objects.filter(username=username,listName=listName).delete()
            FavoriteListMedia.objects.filter(username=username,listName=listName).delete()
    favoriteList = FavoriteList.objects.filter(username=username).values_list('listName',flat=True)
    return render_to_response('favoriteList.html',{'username':username, 'favoriteList':favoriteList}) 

def saveMediaToFavoriteList(request):
    username = request.session.get('username')
    listName = ''
    path = ''
    saveToFavoriteSuccess = ''
    if request.method == 'POST':
        if  request.POST.get('path', ''):
            path = request.POST['path']
            path = path[1:]
        if request.POST.get('listName', ''):
            listName = request.POST['listName']

    mediaType = Media.objects.filter(path=path).values_list('type',flat=True)[0]

    if listName not in FavoriteListMedia.objects.filter(username=username, path=path,listName=listName).values_list('listName',flat=True):
        saveToFavoriteSuccess = "Save the media to favorite list successfully"
        t = FavoriteListMedia(username=username,path=path,type=mediaType,listName=listName)
        t.save()
    else:
        saveToFavoriteSuccess = "The media is already in the favorite list."

    aveScore =  Media.objects.filter(path=path).values_list('aveScore',flat=True)[0]
    keyword =  Media.objects.filter(path=path).values_list('keyword',flat=True)[0]
    comments = Comment.objects.filter(mediaPath = path).values_list('content',flat=True).order_by('-commentTime')
    mediaType = Media.objects.filter(path=path).values_list('type',flat=True)[0]
    numOfViewer = Media.objects.filter(path=path).values_list('numOfViewer',flat=True)[0]
    uploader = Media.objects.filter(path=path).values_list('username',flat=True)[0]

    # must have '/'
    path = '/' + path
    
    #medias = Media.objects.filter(type=mediaType).values_list('path',flat=True)
    medias = request.session.get(mediaType)  # it is mediaType
    favoriteList = FavoriteList.objects.filter(username=username).values_list('listName',flat=True)

    return render_to_response('singleMediaBrowser.html',{'listName':listName,'favoriteList':favoriteList,'saveToFavoriteSuccess':saveToFavoriteSuccess,'uploader':uploader,'numOfViewer':numOfViewer,'aveScore':aveScore,'type':mediaType,'username':request.session.get('username'),
        'comments':comments,'media': path, 'medias':medias})

# delete one media each time
def favoritelistDelete(request):
    path = ''
    listName = ''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('path', ''):
            path = request.POST['path']
            path = path[1:]
        if  request.POST.get('listName', ''):
            listName = request.POST['listName']

    mediaType = FavoriteListMedia.objects.filter(path=path).values_list('type',flat=True)[0]
    FavoriteListMedia.objects.filter(username=username, listName = listName, path=path).delete()
    images = FavoriteListMedia.objects.filter(type="image",username=username,listName=listName).values_list('path',flat=True).distinct()
    videos = FavoriteListMedia.objects.filter(type="video",username=username,listName=listName).values_list('path',flat=True).distinct()
    audios = FavoriteListMedia.objects.filter(type="audio",username=username,listName=listName).values_list('path',flat=True).distinct()

    request.session['image'] = images #type is single
    request.session['video'] = videos
    request.session['audio'] = audios

    medias = request.session.get(mediaType)  # it is mediaType

    delete = "You have deleted it from FavoriteList successfully !"
    return render_to_response('singleMediaBrowser.html', {'type': mediaType,'username':request.session.get('username'), 'medias':medias, 'delete':delete})


def contact(request):
    username = request.session.get('username')
    contactlist = Contactlist.objects.filter(username=username).values_list('contact',flat=True)
    return render_to_response('contact.html',{'username':username, 'contactlist':contactlist})


def searchContact(request):
    searchedContact = ''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('query', ''):
            searchedContact = request.POST['query']
    searchedContact = Account.objects.filter(username=searchedContact).values_list('username',flat=True)
    # delete null error
    if searchedContact: 
        searchedContact = searchedContact[0]
    #prevent search himself
    if searchedContact == request.session.get('username'):
        searchedContact =''
    contactlist = Contactlist.objects.filter(username=username).values_list('contact',flat=True)
    return render_to_response('contact.html',{'ifSearch':True, 'searchedContact':searchedContact,'username':username, 'contactlist':contactlist})

def addContact(request):
    searchedContact = ''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('searchedContact', ''):
            searchedContact = request.POST['searchedContact']
    if  searchedContact.decode('utf8') in Contactlist.objects.filter(username=username).values_list('contact',flat=True):
        searchedContact = ''
    elif  searchedContact.decode('utf8') in Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True):
        searchedBlock = ''
    else: 
        t = Contactlist(username=username, contact=searchedContact)
        t.save()
    
    contactlist = Contactlist.objects.filter(username=username).values_list('contact',flat=True)
    return render_to_response('contact.html',{'ifAdd':True,'addedUser':searchedContact,'username':username, 'contactlist':contactlist})

def sendAndDeleteContact(request):
    contact=''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('delete', ''):
            contact = request.POST['contact']
            Contactlist.objects.filter(username=username,contact=contact).delete()
        if  request.POST.get('send', ''):
            reciever = request.POST['contact']
            return render_to_response('sendMessage.html',{'username':username,'reciever':reciever})

    contactlist = Contactlist.objects.filter(username=username).values_list('contact',flat=True)
    return render_to_response('contact.html',{'username':username, 'contactlist':contactlist})

def searchBlockAdd(request):
    searchedBlock = ''
    blockVistor = False
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('query', ''):
            searchedBlock = request.POST['query']
    if not searchedBlock:
        blockVistor = True
    searchedBlock = Account.objects.filter(username=searchedBlock).values_list('username',flat=True)
    # add 'if' to stop null error
    if searchedBlock: 
        searchedBlock = searchedBlock[0]
    #prevent search himself
    if searchedBlock == request.session.get('username'):
        searchedBlock =''
    blocklist = Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True)
    blocklistAdd = BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True)
    
    return render_to_response('block.html',{'blocklistAdd':blocklistAdd,'blockVistor':blockVistor,'ifSearchAdd':True, 'searchedBlock':searchedBlock,'username':username, 'blocklist':blocklist})

def addBlockAdd(request):
    searchedBlock = ''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('searchedBlock', ''):
            searchedBlock = request.POST['searchedBlock']
    if  searchedBlock.decode('utf8') in BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True):
        searchedBlock = ''
    # elif  '' in BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True):
    #     searchedBlock = ''
    else: 
        if searchedBlock =='[]':
            #blockedUser=''
            t = BlocklistAdd(username=username, blockedUser='')
            t.save()
        else:
            t = BlocklistAdd(username=username, blockedUser=searchedBlock)
            t.save()
    blocklist = Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True)
    blocklistAdd = BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True)

    return render_to_response('block.html',{'blocklistAdd':blocklistAdd,'ifAdd':True,'addedUser':searchedBlock,'username':username, 'blocklist':blocklist})


def deleteBlockedAddUser(request):
    blockedUser=''
    username = request.session.get('username')
    if request.method == 'POST':
        if  request.POST.get('delete', ''):
            blockedUser = request.POST['blockedUser']
            BlocklistAdd.objects.filter(username=username,blockedUser=blockedUser).delete()

    blocklist = Blocklist.objects.filter(username=username).values_list('blockedUser',flat=True)
    blocklistAdd = BlocklistAdd.objects.filter(username=username).values_list('blockedUser',flat=True)

    return render_to_response('block.html',{'blocklistAdd':blocklistAdd,'username':username, 'blocklist':blocklist})








