from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='Родитель')
    position = models.PositiveIntegerField(null=True, blank=True, verbose_name='Номер позиции')
    users = models.ManyToManyField(User, null=True, blank=True, related_name='categories', verbose_name='Менеджеры')
    last_position = models.PositiveIntegerField(default=0, verbose_name='Последняя позиция')
    
    def get_level(self):
        level = 0
        parents = []
        parent = self.parent
        while parent:
            level += 1
            parents.append(str(parent))
            parent = parent.parent
        return [parents, level]

    def get_level2(self):
        level = 0
        parents = []
        parent = self.parent
        while parent:
            level += 1
            parents.append(str(parent))
            parent = parent.parent
        return [reversed(parents), level]

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        if self.parent:
            return self.name + " > " + str(self.parent.name)
        else:
            return self.name
