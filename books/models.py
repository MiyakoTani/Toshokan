from django.db import models
from datetime import date
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from accounts.models import User

# Create your models here.
class Place(models.Model):
    place = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.place

class Book(models.Model):
    isbn = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100)
    titlekana = models.CharField(max_length=100, blank=True, null=True)
    author= models.CharField(max_length=100)
    authorkana = models.CharField(max_length=100, blank=True, null=True)
    volume= models.CharField(max_length=100, blank=True, null=True)
    series= models.CharField(max_length=100, blank=True, null=True)
    publisher= models.CharField(max_length=100, blank=True, null=True)
    pubkana = models.CharField(max_length=100, blank=True, null=True)
    pubdate= models.IntegerField(blank=True, null=True)
    cover= models.CharField(max_length=100, blank=True, null=True)
    place=models.ForeignKey(Place, on_delete=models.PROTECT)
    is_borrowed = models.BooleanField(
        default=False,
    )
    def __str__(self):
        return str(self.id) +' '+ self.title+ ' ' + str(self.place)
    
class Lending(models.Model):
    date=models.DateField(default=date.today)
    returndate=models.DateField()
    book=models.ForeignKey(Book, on_delete=models.PROTECT)
    username=models.ForeignKey(User, on_delete=models.PROTECT)
    is_returned = models.BooleanField(
        default=False,
    )
    def __str__(self):
        return str(self.id) +' '+ self.book.title + ' ' + str(self.username.username)
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=1000)
    rating = models.PositiveIntegerField(default=5)  # 評価(1～5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating} : Review by {self.user.username} on {self.book.title}"