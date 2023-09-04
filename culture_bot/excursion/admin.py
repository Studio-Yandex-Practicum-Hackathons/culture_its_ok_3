from django.contrib import admin

from .models import (AudioExhibit, DescriptionExhibit, Exhibit, Journey,
                     PhotoExhibit, Route, VideoExhibit)


class PhotoExhibitTabularInline(admin.TabularInline):
    model = PhotoExhibit
    extra = 1


class AudioExhibitTabularInline(admin.TabularInline):
    model = AudioExhibit
    extra = 1


class VideoExhibitTabularInline(admin.TabularInline):
    model = VideoExhibit
    extra = 1


class DescriptionExhibitTabularInline(admin.TabularInline):
    model = DescriptionExhibit
    extra = 1


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
    )
    search_fields = ('description', 'title')
    empty_value_display = '-пусто-'


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    inlines = [PhotoExhibitTabularInline, AudioExhibitTabularInline,
               VideoExhibitTabularInline, DescriptionExhibitTabularInline]
    list_display = (
        'name',
        'address',
        'author',
        'route',
        'order'
    )
    list_filter = ('name', )
    empty_value_display = '-пусто-'
    list_editable = ('route',)


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ('traveler', 'route', 'now_exhibit',)
