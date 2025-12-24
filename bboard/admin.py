from django.contrib import admin

from bboard.models import Bb, Rubric

class BbAdmin(admin.ModelAdmin):
    list_display = ('title_and_price', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title_and_price', 'content')
    search_fields = ('title_and_price', 'content')

admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
