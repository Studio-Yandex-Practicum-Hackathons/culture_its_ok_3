from django.contrib import admin

from .models import ExhibitComment, RouteReview, UserFeedback


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "start_time_route",
        "end_time_route",
        "route"
    )
    search_fields = ("route", )
    empty_value_display = "-пусто-"


@admin.register(ExhibitComment)
class ExhibitCommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "route",
        "rating_exhibit",
        "exhibit"
    )
    search_fields = ("text", "rating_exhibit")
    empty_value_display = "-пусто-"


@admin.register(RouteReview)
class RouteReviewAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "route",
        "rating_route"
    )
    search_fields = ("text", "rating_route")
    empty_value_display = "-пусто-"
