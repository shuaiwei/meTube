from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import *
#needed
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^index/$', base),
    (r'^login/$', login),
    (r'^logout/$', logout),

    (r'^register/$', register),
    # (r'^blog/$', blog),

    (r'^search/$', search), # test query 

    (r'^registerFormSubmit/$', registerCheck),
    (r'^loginFormSubmit/$', loginCheck),
    #(r'^browser/$', browser),
    (r'^upload/$', upload),
    (r'^uploadProcess/$', uploadProcess),

    (r'^returnToMain/$', returnToMain),

    (r'^test/$', test),

    (r'^mediaClick/$', mediaClick),
    (r'^mediaDelete/$', mediaDelete),

    (r'^edit/$', edit),
    (r'^editUpdate/$', editUpdate),

    (r'^allMediaBrowser/$', allMediaBrowser),
    (r'^imageBrowser/$', imageBrowser),
    (r'^videoBrowser/$', videoBrowser),
    (r'^audioBrowser/$', audioBrowser),

    (r'^allMediaBrowserPersonal/$', allMediaBrowserPersonal),
    (r'^imageBrowserPersonal/$', imageBrowserPersonal),
    (r'^videoBrowserPersonal/$', videoBrowserPersonal),
    (r'^audioBrowserPersonal/$', audioBrowserPersonal),

    (r'^metaUpdate/$', metaUpdate),
    
    (r'^comment/$', comment),
    
    (r'^download/$', download),
    
    (r'^friend/$', friend), #show friendlist
    (r'^searchFriend/$', searchFriend),
    (r'^addFriend/$', addFriend),
    #send message
    (r'^sendAndDelete/$', sendAndDelete),
    (r'^sendMessage/$', sendMessage),
    (r'^newMessage/$', newMessage),
    (r'^markRead/$', markRead),

    (r'^block/$', block), #show friendlist
    (r'^searchBlock/$', searchBlock),
    (r'^addBlock/$', addBlock),

    (r'^deleteBlockedUser/$', deleteBlockedUser),

    (r'^mostViewed/$', mostViewed), #show 
    (r'^mostRecentUpload/$', mostRecentUpload), 
    #
    (r'^playlist/$', playlist), 

    (r'^playlistDelete/$', playlistDelete), 

    (r'^subscribe/$', subscribe), 
    (r'^subscribeList/$', subscribeList), 

    (r'^subscribeViewAndDelete/$', subscribeViewAndDelete),

    (r'^favoriteList/$', favoriteList),
    
    (r'^addFavoriteList/$', addFavoriteList),

    (r'^deleteAndViewFavoriteList/$', deleteAndViewFavoriteList),
    
    (r'^saveMediaToFavoriteList/$', saveMediaToFavoriteList),
    
    (r'^favoritelistDelete/$', favoritelistDelete),

    (r'^contact/$', contact),
    (r'^searchContact/$', searchContact),
    (r'^addContact/$', addContact),
    
    (r'^sendAndDeleteContact/$', sendAndDeleteContact),

    (r'^searchBlockAdd/$', searchBlockAdd),
    (r'^addBlockAdd/$', addBlockAdd),
    (r'^deleteBlockedAddUser/$', deleteBlockedAddUser),

)
