from datetime import date

from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    tagline = models.CharField(max_length=100, default='', verbose_name='Слоган')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(upload_to='movies/', verbose_name='Постер')
    year = models.PositiveSmallIntegerField(default=2019, verbose_name='Дата выхода')
    country = models.CharField(max_length=30, verbose_name='Страна')
    directors = models.ManyToManyField(Actor, verbose_name='режиссеры', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанры')
    world_premiere = models.DateField(verbose_name='Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField(verbose_name='Бюджет', default=0, help_text='указывать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField(verbose_name='Сборы в США', default=0,
                                              help_text='указывать сумму в долларах')
    fees_in_world = models.PositiveIntegerField(verbose_name='Сборы в мире', default=0,
                                                help_text='указывать сумму в долларах')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    value = models.SmallIntegerField(verbose_name='Значение', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    ip = models.CharField(max_length=15, verbose_name='IP адрес')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CharField, verbose_name='фильм')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100, verbose_name='Имя')
    text = models.TextField(max_length=5000, verbose_name='Сообщение')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Родитель')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фильм')

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
