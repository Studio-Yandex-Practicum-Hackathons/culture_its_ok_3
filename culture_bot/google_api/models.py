from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from excursion.models import Exhibit, Route


class UserFeedback(models.Model):
    telegram_id = models.CharField(
        'user id telegram', max_length=150, blank=True
    )
    start_time_route = models.DateTimeField()
    end_time_route = models.DateTimeField(null=True, blank=True)
    exhibit_comment = models.BooleanField(default=False)
    route_review = models.BooleanField(default=False)
    route = models.ForeignKey(Route, null=True, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Feedback пользователя"
        verbose_name_plural = "Feedback пользователей"


    def __str__(self):
        return f"User {self.telegram_id}"


class ExhibitComment(models.Model):
    text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_feedback = models.ForeignKey(UserFeedback, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE)
    rating_exhibit = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.text


class RouteReview(models.Model):
    text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_feedback = models.ForeignKey(UserFeedback, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    rating_route = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.text
