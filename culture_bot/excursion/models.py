from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Route(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название маршрута',
    )
    description = models.TextField(
        verbose_name='Описание маршрута',
    )
    lyrics = models.TextField(
        verbose_name='Лирическое описание',
        default='',
    )
    route_map = models.ImageField(
        upload_to='excursion/router_map/',
        blank=True,
        verbose_name='Карта маршрута',
        help_text='Добавьте карту маршрута',
    )

    cover = models.ImageField(
        upload_to='excursion/cover/',
        blank=True,
        verbose_name='Обложка маршрута',
        help_text='Добавьте обложку маршрута',
    )

    # rating = models.IntegerField(
    #     verbose_name='Рейтинг',
    #     default=0,
    # )
    where_start = models.TextField(
        verbose_name='Как пройти к старту',
    )

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    # def get_rating(self):
    #     return ReflectionExhibit.objects.filter(exhibit=self).aggregate(
    #         Avg('rating'))

    def __str__(self):
        return self.title


class Exhibit(models.Model):
    route = models.ForeignKey(
        Route,
        null=True,
        on_delete=models.SET_NULL,
        related_name='exhibit',
        verbose_name='Маршрут',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название экспоната',
    )
    address = models.CharField(
        max_length=200,
        verbose_name='Адрес',
    )
    # rating = models.IntegerField(
    #     verbose_name='Рейтинг',
    #     default=1
    # )

    author = models.CharField(
        max_length=50,
        verbose_name='Художник',
    )

    question_for_reflection = models.TextField(
        verbose_name='Вопрос для рефлексии',
        null=True,
        blank=True,
    )

    answer_for_reflection = models.TextField(
        verbose_name='Ответ для рефлексии',
        null=True,
        blank=True,
    )

    where_start = models.TextField(
        verbose_name='Как пройти к экспонату',
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=0,)

    def save(self):
        order = Route.objects.get(title=self.route.title).exhibit.count()
        self.order = order + 1
        super(Exhibit, self).save()

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'

        models.UniqueConstraint(
            fields=('route', 'order'),
            name='unique_route_for_order'
        ),

    # def get_rating(self):
    #     return ReflectionExhibit.objects.filter(exhibit=self).aggregate(Avg('rating'))
    #

    def __str__(self):
        return self.name


class PhotoExhibit(models.Model):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='photo_exhibit'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to='excursion/exhibit/',
        blank=True,
        verbose_name='Фотографии экспонатов',
        help_text='Добавьте картинку экспоната',
    )


class DescriptionExhibit(models.Model):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='description_exhibit'
    )
    text = models.TextField()


class AudioExhibit(models.Model):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='audio_exhibit'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    audio = models.FileField(upload_to='audios/')


class VideoExhibit(models.Model):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='video_exhibit'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    video = models.FileField(upload_to='videos/')


class ReflectionExhibit(models.Model):
    author = models.CharField(
        max_length=20,
        verbose_name='Комментатор',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    contact = models.CharField(
        max_length=50
    )
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='reflection_exhibit',
        verbose_name='Рефлексия на экспонат',
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=1
    )

    class Meta:
        verbose_name = 'Рефлексия на экспонат'
        verbose_name_plural = 'Рефлексия  на экспонаты'

    def __str__(self):
        return self.text[1:20]


class Journey(models.Model):
    traveler = models.PositiveIntegerField()
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        null=True
    )
    now_exhibit = models.PositiveIntegerField()
