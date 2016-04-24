from django.contrib import admin
from modelView.models import * 
admin.site.register(Cert)
admin.site.register(UserProfile)

# admin.site.unregister(Upload)

admin.site.register(Account)
admin.site.register(Media)
admin.site.register(Download)
admin.site.register(Upload)