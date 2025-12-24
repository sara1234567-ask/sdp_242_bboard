from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models


def get_min_length():
    min_length = 4
    # Вычисления
    return

def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечётное',
                              code='odd',
                              params={'value': val})


class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError(
                'Введённое число должно находиться в диапазоне'
                'от %(min)s до %(max)s',
                code='out_of_range',
                params={'min': self.min_value, 'max': self.max_value},
            )



class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ('name',)


class Bb(models.Model):
    # KINDS = (
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    KINDS = (
        ('Купля-продажа', (
            ('b', 'Куплю'),
            ('s', 'Продам'),
        )),
        ('Обмен', (
            ('c', 'Обменяю'),
        ))
    )

    # KINDS = (
    #     (None, 'Выберите тип публикуемого объявления'),
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
        verbose_name='Тип объявления',
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
        validators=[
            validators.RegexValidator(regex=r'^.{4,}$',),
            # validators.MinLengthValidator(get_min_length),
        ],
        error_messages={'invalid': 'Введите 4 или более символов'}
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Цена',
        validators=[validate_even],
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    rubric = models.ForeignKey(
        # Rubric,
        'Rubric',
        # 'bboard.Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    # def save(self, *args, **kwargs):
    #     if self.is_model_correct():
    #         super().save(*args, **kwargs)
    #
    # def delete(self, *args, **kwargs):
    #     if self.need_to_delete():
    #         super().delete(*args, **kwargs)

    # Функциональное поле
    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price})'
        return f'{self.title}'

    title_and_price.short_description = 'Название и цена'

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError(
                'Укажите описание продаваемого товара'
            )

        if self.price and self.price < 0:
            errors['price'] = ValidationError(
                'Укажите неотрицательное значение цены'
            )

        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']
