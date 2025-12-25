from django.db import models
from django.core.exceptions import ValidationError

# Валидация для цены (неотрицательное число)
def validate_positive_or_zero(value):
    if value < 0:
        raise ValidationError(f'{value} должно быть положительным или 0')

class Rubric(models.Model):
    name = models.CharField(max_length=50, verbose_name='Рубрика')

    def __str__(self):
        return self.name

class Bb(models.Model):
    KINDS = (
        ('Купля-продажа', (
            ('b', 'Куплю'),
            ('s', 'Продам'),
        )),
        ('Обмен', (
            ('c', 'Обменяю'),
        ))
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
        verbose_name='Тип объявления',
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
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
        validators=[validate_positive_or_zero],
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    # Функциональное поле
    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price})'
        return f'{self.title}'

    title_and_price.short_description = 'Название и цена'

    # Классный метод для обновления заголовков
    @classmethod
    def update_titles(cls):
        for bb in cls.objects.all():
            bb.title = f"{bb.title} ({bb.id})"
            bb.save()

    # Классный метод для удаления записей с нечётной цифрой в заголовке
    @classmethod
    def delete_odd_titles(cls):
        for bb in cls.objects.all():
            digits = [int(c) for c in bb.title if c.isdigit()]
            if any(d % 2 != 0 for d in digits):
                bb.delete()

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']
