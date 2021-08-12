from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Tag(models.Model):

    name = models.CharField(max_length=250)
    article = models.ManyToManyField(Article, through='ArticleTag')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class ArticleTag(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Раздел')
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематика статей'
        ordering = ['-is_main']

    def __str__(self):
        return f'{self.article.title}, {self.tag.name}'
