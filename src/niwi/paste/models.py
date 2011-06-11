from django.db import models

class Paste(models.Model):
    text = models.TextField()
    lexer = models.CharField(max_length=5)
    title = models.CharField(max_length=100, blank=True)
    group = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'paste'


class RestrictedLog(models.Model):
    host = models.CharField(max_length=100, unique=True)
    stamp = models.DateTimeField(max_length=100)
