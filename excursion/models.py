from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Route(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    exhibits = models.ManyToManyField() # todo
    route_map = models.ImageField(
        upload_to='posts/image/',
        blank=True,
        verbose_name="Картинка",
        help_text="Добавьте картинку к вашему посту ",
    )
    reviews = # todo
    rating =


class Exhibit(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to='posts/image/',
        blank=True,
        verbose_name="Картинка",
        help_text="Добавьте картинку к вашему посту ",
    )
    address =  models.CharField(max_length=200)
    rating =
    author =

class Reviews(models.Model):
    author =
    text =
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

class ReviewOnRoute(Reviews):
    route =


class ReviewOnExhibit(Reviews):
    exhibit =
    finish_time =
