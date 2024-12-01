from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Game(models.Model):
    name = models.CharField(max_length=255)
    min_players = models.IntegerField(default=0)
    max_players = models.IntegerField(default=0)
    description = models.TextField(default='')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Table(models.Model):
    number = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return f'No. {self.number}, max capacity: {self.capacity}'

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    notes = models.TextField(default='')

    def __str__(self):
        return f'{self.user} - {self.game} - Table no. {self.table} - {self.start_time} - {self.end_time}'

