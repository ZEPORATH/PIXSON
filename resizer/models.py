from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class Opencv(models.Model):
    imagem = models.ImageField(upload_to='documents/')

class Opencv2(models.Model):
    height = models.CharField(max_length=100,help_text="Enter height in px")
    width = models.CharField(max_length=100,help_text="Enter width in px")
    resize_method = models.CharField(max_length=255,help_text="Enter method for resizing")



