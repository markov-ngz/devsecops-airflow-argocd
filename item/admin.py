from django.contrib import admin
from .models import Category, Item
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
        fieldsets = [
            ("Item attributes",{"fields": ["name","category","description"]}),
            ("Cost information",{"fields":["price"]}),
            ]
admin.site.register(Item,ItemAdmin)
admin.site.register(Category)