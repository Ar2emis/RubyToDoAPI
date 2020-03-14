from django.contrib import admin, auth


admin.site.unregister(auth.models.Group)
# admin.site.unregister(auth.models.User)