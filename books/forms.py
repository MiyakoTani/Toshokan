from django import forms
from django.forms import ModelForm
from .models import Place,Book

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = (
            "place",
        )
        labels={
           "place":"本棚の場所",
           }
class BookForm1(forms.Form):
    isbn = forms.CharField(max_length=13, label = 'ISBN')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "isbn",
            "title",
            "author",
            "volume",
            "series",
            "publisher",
            "pubdate",
            "cover",
            "place",
        )

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "isbn",
            "title",
            "author",
            "volume",
            "series",
            "publisher",
            "pubdate",
            "cover",
            "place",
            "is_borrowed"
        )
        labels={
           "isbn":"ISBN",
            "title":"タイトル",
            "author":"著者",
            "volume":"ページ数",
            "series":"シリーズ",
            "publisher":"出版社",
            "pubdate":"出版日",
            "cover":"書影",
            "place":"本棚の場所",
            "is_borrowed":"チェックが入っていたら貸出中",
           }