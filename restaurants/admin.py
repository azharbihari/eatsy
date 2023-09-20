from django.contrib import admin
from restaurants.models import Restaurant, Category, Menu


class RestaurantAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category)
admin.site.register(Menu)
