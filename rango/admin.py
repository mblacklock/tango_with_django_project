from django.contrib import admin

# Register your models here.

from rango.models import Category, Page

class PageInline(admin.TabularInline):
    model = Page
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['name','views','likes']}),
        ]
    inlines = [PageInline]

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
