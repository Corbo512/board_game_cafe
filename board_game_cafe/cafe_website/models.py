from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=255, blank=True, default='')

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class Game(models.Model):
    name = models.CharField(max_length=255)
    min_players = models.IntegerField(default=0)
    max_players = models.IntegerField(default=0)
    description = models.TextField(default='', blank=True)
    author = models.ManyToManyField(Author, blank=True)
    thumbnail = models.URLField(default='', blank=True)

    def __str__(self):
        return self.name

class Table(models.Model):
    number = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return f'Table {self.number} | {self.capacity} seats'

class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.user} - {self.game} - {self.table} - {self.start_time} - {self.end_time}'

