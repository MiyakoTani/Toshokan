from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from .models import Place,Book,Lending,Review

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
           }

from django.utils import timezone
import datetime

class LendingForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ('date', 'returndate')
        labels = {
            'date': '貸出開始日',
            'returndate': '返却日',
        }
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
            'returndate': forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初期値としてreturndateをdateから14日後に設定
        if self.instance and not self.instance.returndate:
            self.fields['returndate'].initial = self.instance.date + timezone.timedelta(days=14)

    def clean_returndate(self):
        returndate = self.cleaned_data.get('returndate')
        date = self.cleaned_data.get('date')


        if returndate < date:
            raise forms.ValidationError('返却日は貸出開始日より後の日付でなければなりません。')

        # 返却日は貸出日から14日以内とする
        if (returndate - date).days > 14:
            raise forms.ValidationError('返却日は貸出日から14日以内でなければなりません。')

        return returndate
    
    def clean_date(self):
        today = datetime.date.today()
        date = self.cleaned_data.get('date')

        
        if date < today:
            raise forms.ValidationError('貸出日は本日以降の日付でなければなりません。')

        return date
