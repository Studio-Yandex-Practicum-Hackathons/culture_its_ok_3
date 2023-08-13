from django.db import models


class Route(models.Model):
    title = models.CharField(max_length=50,
                             verbose_name="Название маршрута",)
    description = models.TextField(verbose_name="Описание экспоната",)
    route_map = models.ImageField(
        upload_to='excursion/router_map/',
        blank=True,
        verbose_name="Карта маршрута",
        help_text="Добавьте карту маршрута",
    )
    rating = models.IntegerField(verbose_name="Рейтинг",)

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        return self.title


class Exhibit(models.Model):
    route = models.ForeignKey(
        Route,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="exhibit",
        verbose_name="Маршрут",
    )
    name = models.CharField(max_length=200,
                            verbose_name="Название экспоната", )
    description = models.TextField(verbose_name="Описание экспоната",)
    image = models.ImageField(
        upload_to='excursion/exhibit/',
        blank=True,
        verbose_name="Картинка",
        help_text="Добавьте картинку экспоната",
    )
    address = models.CharField(max_length=200,
                               verbose_name="Адрес",)
    rating = models.IntegerField(verbose_name="Рейтинг",)

    # хотим ли мы создавать отдельную модель художников?
    author = models.CharField(max_length=50, verbose_name="Художник",)

    class Meta:
        verbose_name = "Экспонат"
        verbose_name_plural = "Экспонаты"

    def __str__(self):
        return self.name


class Reviews(models.Model):
    # хотим ли мы хранить данные и создавать
    # отдельную модель пользователя
    # или ограничимся его подписью
    author = models.CharField(max_length=20,
                              verbose_name="Комментатор",)
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    contact = models.CharField(max_length=50)


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
