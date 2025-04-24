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
            "titlekana",
            "author",
            "authorkana",
            "volume",
            "series",
            "publisher",
            "pubkana",
            "pubdate",
            "cover",
            "place",
            "description",
        )

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "isbn",
            "title",
            "titlekana",
            "author",
            "authorkana",
            "volume",
            "series",
            "publisher",
            "pubkana",
            "pubdate",
            "cover",
            "place",
            "description",
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
            "description":"概要",
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

        # dateやreturndateがNoneの場合をチェック
        if not returndate or not date:
            raise forms.ValidationError('貸出開始日と返却日を正しく入力してください。')

        # 貸出開始日と返却日を比較
        if returndate < date:
            raise forms.ValidationError('返却日は貸出開始日より後の日付でなければなりません。')

        # 返却日は貸出日から14日以内
        if (returndate - date).days > 14:
            raise forms.ValidationError('返却日は貸出日から14日以内でなければなりません。')

        return returndate
    
    def clean_date(self):
        today = timezone.localdate()  # タイムゾーンを考慮した今日の日付
        date = self.cleaned_data.get('date')

        # dateがNoneの場合をチェック
        if not date:
            raise forms.ValidationError('貸出日を正しく入力してください。')

        # 貸出日が本日以降であることをチェック
        if date < today:
            raise forms.ValidationError('貸出日は本日以降の日付でなければなりません。')

        return date