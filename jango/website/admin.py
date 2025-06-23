from django.contrib import admin

# Register your models here.

from .models import SongList

@admin.register(SongList)
class SongListAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'year')  # ✅ show these in list
    list_filter = ('year',)                    # ✅ filter by this field
    search_fields = ('title', 'album')         # ✅ searchable fields