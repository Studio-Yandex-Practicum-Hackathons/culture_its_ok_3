from django.db import models


class Route(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Название маршрута",
    )
    description = models.TextField(
        verbose_name="Описание экспоната",
    )
    route_map = models.ImageField(
        upload_to='excursion/router_map/',
        blank=True,
        verbose_name="Карта маршрута",
        help_text="Добавьте карту маршрута",
    )
    rating = models.IntegerField(
        verbose_name="Рейтинг",
        default=0,
    )

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        return self.title


class Exhibit(models.Model):
    route = models.ForeignKey(
        Route,
        null=True,
        on_delete=models.SET_NULL,
        related_name="exhibit",
        verbose_name="Маршрут",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название экспоната",
    )
    description = models.TextField(
        verbose_name="Описание экспоната",
    )
    address = models.CharField(
        max_length=200,
        verbose_name="Адрес",
    )
    rating = models.IntegerField(
        verbose_name="Рейтинг",
    )
    author = models.CharField(
        max_length=50,
        verbose_name="Художник",
    )

    question_for_reflection = models.TextField(
        verbose_name="Вопрос для рефлексии",
    )

    answer_for_reflection = models.TextField(
        verbose_name="Ответ для рефлексии",
    )

    order = models.PositiveIntegerField()

    def save(self):
        order = Route.objects.get(title=self.route.title).exhibit.count()
        self.order = order + 1
        super(Exhibit, self).save()

    class Meta:
        verbose_name = "Экспонат"
        verbose_name_plural = "Экспонаты"

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
        null=True
    )

    photo = models.ImageField(
        upload_to='excursion/exhibit/',
        blank=True,
        verbose_name="Фотографии экспонатов",
        help_text="Добавьте картинку экспоната",
    )


class Reviews(models.Model):
    author = models.CharField(
        max_length=20,
        verbose_name="Комментатор",
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    contact = models.CharField(
        max_length=50
    )


class ReviewOnRoute(Reviews):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="review_on_route",
        verbose_name="Комментируемый маршрут",
    )

    class Meta:
        verbose_name = "Комментарий на маршрут"
        verbose_name_plural = "Комментарии на маршруты"

    def __str__(self):
        return self.text[1:20]


class ReviewOnExhibit(Reviews):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name="review_on_exhibit",
        verbose_name="Комментируемый экспонат",
    )

    class Meta:
        verbose_name = "Комментарий на экспонат"
        verbose_name_plural = "Комментарии на экспонаты"

    def __str__(self):
        return self.text[1:20]


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний ID пользователя',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя',
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(
        to='Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Journey(models.Model):
    traveler = models.PositiveIntegerField()
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        null=True
    )
    now_exhibit = models.PositiveIntegerField()
