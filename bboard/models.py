from django.db import models

from django.db import models

class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ('name',)


class Bb(models.Model):
    KINDS = (
        ('Купля-продажа', (
            ('b', 'Куплю'),
            ('s', 'Продам')
        )),
        ('Обмен', (
            ('c', 'Обменяю'),
        ))
    )



    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
        verbose_name='Тип объявления'
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
    )
    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    rubric = models.ForeignKey(
        #Rubric,
        'Rubric',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',

    )

    def __str__(self):
        return f'Объявление: {self.title}'

    #def save(self):
        if self.is_model_correct():
            super().save()

    #def delete(self):
        if self.need_to_delete():
            super().delete()

    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price})'
        return f'{self.title}'

    title_and_price.short_description = 'название и цена'



    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-published',)
