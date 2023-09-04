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


HTML_TAG = {
    '<u>': '</u>',  # подчеркнутый
    '<del>': '</del>',  # зачеркнуты текст
    '<em>': '</em>',  # курсив
    '<i>': '</i>',  # курсив
    '<strong>': '</strong>',  # жирный
    '<b>': '</b>',  # жирный
    '<a href =': '</a>',  # ссылки
}


def html_validator(text):
    for open_tag, close_tag in HTML_TAG.items():
        if open_tag in text:
            if close_tag not in text:
                raise ValidationError(
                    [f'Нет закрывающего тега: {close_tag}']
                )

        if close_tag in text:
            if open_tag not in text:
                raise ValidationError(
                    [f'Нет открывающего тега: {open_tag}']
                )
