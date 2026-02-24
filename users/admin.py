from django.contrib import admin

# Register your models here.
class ListGGPAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'description')
    search_fields = ('nome')

admin.site.register(ListGGP, ListGGPAdmin)
