from django.db import models

# Create your models here.
class Place(models.Model):
    place = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.place

class Book(models.Model):
    isbn = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100)
    author= models.CharField(max_length=100)
    volume= models.CharField(max_length=100, blank=True, null=True)
    series= models.CharField(max_length=100, blank=True, null=True)
    publisher= models.CharField(max_length=100, blank=True, null=True)
    pubdate= models.IntegerField(max_length=10, blank=True, null=True)
    cover= models.CharField(max_length=100, blank=True, null=True)
    place=models.ForeignKey(Place, on_delete=models.PROTECT)
    is_borrowed = models.BooleanField(
        default=False,
    )
    def __str__(self):
        return str(self.id) +' '+ self.title+ ' ' + str(self.place)