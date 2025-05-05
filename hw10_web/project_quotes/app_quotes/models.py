from django.db import models
from django.contrib.auth.models import User


# Модель для тегів, які можна прикріплювати до цитат
class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f'{self.name}'


# Модель для збереження інформації про авторів цитат
class Author(models.Model):
    fullname = models.CharField(null=False, unique=True)
    born_date = models.CharField()
    born_location = models.CharField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.fullname}'


# Модель для збереження самих цитат
class Quote(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    quote = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.quote}'
