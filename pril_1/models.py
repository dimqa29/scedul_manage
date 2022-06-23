from django.db import models
from django.urls import reverse

# Create your models here.
class ListCross(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='url Cross')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Cross'
        verbose_name_plural = 'Cross#'
        ordering = ['title']
