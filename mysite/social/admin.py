from django.contrib import admin

# Register your models here.
from .models import SocialUser

class SocialUserModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'email', 'created_date']
    list_display_links = ['created_date']
    list_filter = ['name', 'surname']
    search_fields = ['name', "surname", 'email', 'city']

    class Meta:
        model = SocialUser


admin.site.register(SocialUser, SocialUserModelAdmin)
