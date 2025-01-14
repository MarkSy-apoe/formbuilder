from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email', 'username', 'first_name', 'last_name')
	readonly_fields = ('id', 'date_joined', 'last_login')

	filter_horizontal = ()
	list_filter=()
	fieldsets=()
	
admin.site.register(Account, AccountAdmin)
admin.site.register(Form)
admin.site.register(FormComponent)