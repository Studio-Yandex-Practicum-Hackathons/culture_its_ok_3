from django.contrib import admin

from .models import (AudioExhibit, DescriptionExhibit, Exhibit, Journey,
                     PhotoExhibit, ReflectionExhibit, Route, VideoExhibit)


class PhotoExhibitTabularInline(admin.TabularInline):
    model = PhotoExhibit


class AudioExhibitTabularInline(admin.TabularInline):
    model = AudioExhibit


class VideoExhibitTabularInline(admin.TabularInline):
    model = VideoExhibit


class DescriptionExhibitTabularInline(admin.TabularInline):
    model = DescriptionExhibit


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "rating"
    )
    search_fields = ("description", "title")
    list_filter = ("rating",)
    empty_value_display = "-пусто-"


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    inlines = [PhotoExhibitTabularInline, AudioExhibitTabularInline,
               VideoExhibitTabularInline, DescriptionExhibitTabularInline]
    list_display = (
        "name",
        "address",
        "rating",
        "author",
        "route"
    )

    list_filter = ("name", )
    empty_value_display = "-пусто-"
    list_editable = ("route",)


@admin.register(ReflectionExhibit)
class ReflectionExhibitAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "exhibit",
        "author",
        "contact",
    )
    search_fields = ("text", "exhibit",)
    list_filter = ("author", "exhibit")
    empty_value_display = "-пусто-"


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ('traveler', 'route', 'now_exhibit',)
