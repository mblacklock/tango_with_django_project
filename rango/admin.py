from django.contrib import admin

# Register your models here.

from rango.models import Category, Page, UserProfile

class PageInline(admin.TabularInline):
    model = Page
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    fieldsets = [
        (None,                  {'fields': ['name','views','likes','slug']}),
        ]
    inlines = [PageInline]

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'category', 'url', 'views','slug')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)
