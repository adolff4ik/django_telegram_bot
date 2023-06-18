from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    content = models.TextField(null=True)
    keyword = models.CharField(max_length=50,null=True)
    pubdate = models.DateTimeField()
    link = models.URLField(max_length=200)
    cock = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CategoryNum(models.Model):
    name = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    num = models.IntegerField()

    def __str__(self):
        return f"{self.name.name} ({self.num})"