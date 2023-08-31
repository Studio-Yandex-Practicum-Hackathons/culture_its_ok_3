from django.core.exceptions import ValidationError

from .const import MAX_LINEAR_SIZE, MAX_PROPORTIONS, MAX_SIZE_FILE


def file_size_validator(value):
    if value.size > MAX_SIZE_FILE:
        raise ValidationError(f'Слишком большой файл, максимальный размер {MAX_SIZE_FILE} байт')


def linear_image_dimensions_validator(image):
    height = image.height
    width = image.width
    if height + width < MAX_LINEAR_SIZE:
        raise ValidationError(f'Cумма ширины и высоты не должна превышать {MAX_LINEAR_SIZE}')


def aspect_ratio_validator(image):
    height = image.height
    width = image.width
    if (height/width < MAX_PROPORTIONS
            or width/height < MAX_PROPORTIONS):
        raise ValidationError(
            [f'Соотношение сторон не должно превышать {MAX_PROPORTIONS}']
        )
