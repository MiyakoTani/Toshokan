from django.contrib import admin
from .models import Place, Book, Lending, Review
# Register your models here.
admin.site.register(Place)
admin.site.register(Book)
admin.site.register(Lending)
admin.site.register(Review)