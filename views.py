from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render_to_response

def base(request):
	return render_to_response('base.html')

def login(request):
	return render_to_response('login.html')
def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return render_to_response('base.html')

    return render_to_response('login.html')
# def blog(request):
# 	return render_to_response('blog.html')
def register(request):
	return render_to_response('register.html')

from forms import accountForm

from django.http import HttpResponseRedirect
from modelView.models import *

def returnToUserMain(request):
    username = request.session.get('username')
    images = Media.objects.filter(username=username, type="image").values_list('path',flat=True)
    videos = Media.objects.filter(username=username, type="video").values_list('path',flat=True)
    audios = Media.objects.filter(username=username, type="audio").values_list('path',flat=True)

    return render(request, 'allMediaBrowser.html', {'username': username, 'images': images, 'videos': videos, 'audios': audios})

def returnToMain(request):
    images = Media.objects.filter(type="image").values_list('path',flat=True)
    videos = Media.objects.filter(type="video").values_list('path',flat=True)
    audios = Media.objects.filter(type="audio").values_list('path',flat=True)
    return render(request, 'allMediaBrowser.html', {'images': images, 'videos': videos, 'audios': audios})


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
                modifyPassword = "Modify password successlly !"
                t = Account.objects.get(username=request.session.get('username'))
                t.password = request.POST['password']
                t.save() 

    firstname =  Account.objects.filter(username=request.session.get('username')).values_list('firstname',flat=True)[0]
    lastname =  Account.objects.filter(username=request.session.get('username')).values_list('lastname',flat=True)[0]
    company =  Account.objects.filter(username=request.session.get('username')).values_list('company',flat=True)[0]
    #"values" get method can alse be used,use index
    address =  Account.objects.filter(username=request.session.get('username')).values('address')[0]['address']

    return render_to_response('editProfile.html',{'username':request.session.get('username'),
        'firstname':firstname, 'lastname':lastname, 'company':company, 'address':address,
        'success':success, 'modifyPassword':modifyPassword})


def metaUpdate(request):
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

    meta =  Media.objects.filter(path=path).values_list('meta',flat=True)[0]
    keyword =  Media.objects.filter(path=path).values_list('keyword',flat=True)[0]
    #"values" get method can alse be used
    mediaType = Media.objects.filter(path=path).values_list('type',flat=True)[0]
    # must have '/'
    path = '/' + path
    if mediaType == 'image':
        #use medias here
        medias = Media.objects.filter(type='image').values_list('path',flat=True)
        return render_to_response('singleMediaBrowser.html',{'type':mediaType,'username':request.session.get('username'),
            'meta':meta, 'keyword':keyword,'media': path, 'medias':medias})
    elif mediaType == 'video':
        medias = Media.objects.filter(type='video').values_list('path',flat=True)
        return render_to_response('singleMediaBrowser.html',{'type':mediaType,'username':request.session.get('username'),
            'meta':meta, 'keyword':keyword,'media': path, 'medias':medias})
    elif mediaType == 'audio':
        medias = Media.objects.filter(type='audio').values_list('path',flat=True)
        return render_to_response('singleMediaBrowser.html',{'type':mediaType,'username':request.session.get('username'),
            'meta':meta, 'keyword':keyword,'media': path, 'medias':medias})
    else:
        pass
    # program can not reach here
    #return render_to_response('singleMediaBrowser.html')
     

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

                    return render(request, 'allMediaBrowser.html', {'username': username, 'images': images, 'videos': videos, 'audios': audios})
                else:
                    errors.append('Passwords don\'t match. Try again?')

    return render(request, 'login.html', {'errors': errors})

# def browser(request): # for no login user
#      return render(request, 'browser.html')

def upload(request): 
     return render(request, 'upload.html',{'username': request.session.get('username')})

from modelView.models import Media
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
            imageType = ['jpg','png','bmp']
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
    meta =  Media.objects.filter(path=media).values_list('meta',flat=True)[0]
    keyword =  Media.objects.filter(path=media).values_list('keyword',flat=True)[0]
    mediaType = Media.objects.filter(path=media).values_list('type',flat=True)[0]

    media = '/' + media
    
    if 'username' in request.session:
        medias = Media.objects.filter(username=request.session.get('username'), type=mediaType).values_list('path',flat=True)

        return render_to_response('singleMediaBrowser.html',{'type':mediaType, 'username':request.session.get('username'),
            'meta':meta, 'keyword':keyword,'media': media, 'medias':medias})
    else: # all images
        medias = Media.objects.filter(type=mediaType).values_list('path',flat=True)
        return render_to_response('singleMediaBrowser.html',{'type':mediaType, 'meta':meta, 'keyword':keyword,'media':media, 'medias':medias})
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
    os.remove(media)

    medias = Media.objects.filter(username=request.session.get('username'), type=mediaType).values_list('path',flat=True)
    delete = "You have deleted that image successfully !"
    return render_to_response('singleMediaBrowser.html', {'type': mediaType,'username':request.session.get('username'), 'medias':medias, 'delete':delete})

def allMediaBrowser(request):
    if 'username' in request.session:
        images = Media.objects.filter(username=request.session.get('username'),type="image").values_list('path',flat=True)
        videos = Media.objects.filter(username=request.session.get('username'),type="video").values_list('path',flat=True)
        audios = Media.objects.filter(username=request.session.get('username'),type="audio").values_list('path',flat=True)

        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images, 'videos': videos, 'audios':audios})
    else:
        images = Media.objects.filter(type="image").values_list('path',flat=True)
        videos = Media.objects.filter(type="video").values_list('path',flat=True)
        audios = Media.objects.filter(type="audio").values_list('path',flat=True)

        return render_to_response('allMediaBrowser.html', {'images':images,'videos': videos, 'audios':audios})

def imageBrowser(request):
    if 'username' in request.session:
        images = Media.objects.filter(username=request.session.get('username'),type="image").values_list('path',flat=True)
        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'images':images})
    else:
        images = Media.objects.filter(type="image").values_list('path',flat=True)
        return render_to_response('allMediaBrowser.html', {'images':images})

def videoBrowser(request):
    if 'username' in request.session:
        videos = Media.objects.filter(username=request.session.get('username'),type="video").values_list('path',flat=True)
        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'videos':videos})
    else:
        videos = Media.objects.filter(type="video").values_list('path',flat=True)
        return render_to_response('allMediaBrowser.html', {'videos':videos})
def audioBrowser(request):
    if 'username' in request.session:
        audios = Media.objects.filter(username=request.session.get('username'),type="audio").values_list('path',flat=True)
        return render_to_response('allMediaBrowser.html', {'username':request.session.get('username'), 'audios':audios})
    else:
        audios = Media.objects.filter(type="audio").values_list('path',flat=True)
        return render_to_response('allMediaBrowser.html', {'audios':audios})

from django.db.models import Q

def search(request):
    query = ''
    mediaType = ''
    if request.method == 'POST':
        if  request.POST.get('query', ''):
            query = request.POST['query']
        if  request.POST.get('mediaType', ''):
            mediaType = request.POST['mediaType']
    queryArray = query.split()     
    medias = Media.objects.filter(Q(type=mediaType), reduce(lambda x, y: x | y, 
        [Q(keyword__contains=queryword) for queryword in queryArray])).values_list('path',flat=True)

    return render(request, 'searchResultBrowser.html', {'type':mediaType, 'medias':medias})

