from django.contrib import admin
from .models import Category,Page,UserProfiles

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_deplay=('title','category','url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfiles)
