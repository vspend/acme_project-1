

# birthday/models.py
from django.db import models
from .validators import real_age
from django.urls import reverse
from users.models import MyUser

class Tag(models.Model):
    tag = models.CharField('Тег', max_length=20)
    # Переопределяем метод:
    def __str__(self):
        return self.tag


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    
    birthday = models.DateField('Дата рождения', validators=(real_age,)) 
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
    ) 


    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk}) 

class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday, 
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',) 



