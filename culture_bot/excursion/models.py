from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import file_size_validator


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
        validators=[file_size_validator, ]
    )

    cover = models.ImageField(
        upload_to='excursion/cover/',
        blank=True,
        verbose_name='Обложка маршрута',
        help_text='Добавьте обложку маршрута',
        validators=[file_size_validator, ]
    )

    where_start = models.TextField(
        verbose_name='Как пройти к старту',
    )

    question_end = models.TextField(
        verbose_name='Вопрос в конце маршрута',
        blank=True,
        null=True,
    )

    show = models.BooleanField(
        verbose_name='Показывать маршрут?',
        default=True
    )

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

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

    order = models.PositiveIntegerField(default=0,
                                        verbose_name='порядок в маршруте',
                                        help_text=('при добавление нового экспоната ему '
                                                   'присваивается последний номер, '
                                                   'при редактирование его можно будет поменять'))

    def save(self):
        if self.pk is None:
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
        null=True,
        verbose_name='Описание фотографии',
    )

    photo = models.ImageField(
        upload_to='excursion/exhibit/',
        blank=True,
        verbose_name='Фотографии экспонатов',
        help_text='Добавьте картинку экспоната',
        validators=[file_size_validator, ]
    )


class DescriptionExhibit(models.Model):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='description_exhibit'
    )
    text = models.TextField(
        verbose_name='Текст сообщения',
        help_text=('каждая область - это отдельное сообщение '
                   'которые будут идти с задержкой пропорционально длине текста, ')
    )


class AudioExhibit(models.Model):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='audio_exhibit',
        validators=[file_size_validator]
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Описание аудио',
    )

    audio = models.FileField(upload_to='audios/')


class VideoExhibit(models.Model):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='video_exhibit',
        validators=[file_size_validator]
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Описание видео',
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
    traveler = models.PositiveIntegerField(verbose_name='Путешественник',)
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Маршрут',
    )
    now_exhibit = models.PositiveIntegerField(verbose_name='Номер текущего экспоната')

    class Meta:
        verbose_name = 'Начатое путешествие'
        verbose_name_plural = 'Начатые путешествия'
