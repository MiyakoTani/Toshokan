from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.db import models
from django.contrib import messages
from .forms import PlaceForm, BookForm, BookForm1
from .models import Place,Book
from . import forms

class Place_make_View(CreateView):
    form_class = PlaceForm
    template_name = "books/place_make.html"
    success_url = reverse_lazy("books:place_make")
    
def PlaceDelete(request, page=1):
    params = {
        'data':[],
        'data_p':[],
        'data_list':[],
    }

    page_cnt = 5 #一画面あたり10コ表示する
    onEachSide = 3 #選択ページの両側には3コ表示する
    onEnds = 2 #左右両端には2コ表示する
    if (request.method == 'POST'):
        num = request.POST['place']
        try:
            item = Place.objects.get(place=num)
            params['data_p'] = [item]
        except:
            params['data'] = Place.objects.order_by('place').all()
            # paginatorのオブジェクトをつくってる
            data_page = Paginator(params['data'], page_cnt)
            
            # paginatorのオブジェクトからページを指定した状態のオブジェクトつくってる
            params['data_p'] = data_page.get_page(page)

            # 指定したページのオブジェクトからページリンク先のリストを作っている
            params['data_list'] = params['data_p'].paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds) 
    else:
        params['data'] = Place.objects.order_by('place').all()
        # paginatorのオブジェクトをつくってる
        data_page = Paginator(params['data'], page_cnt)
        
        # paginatorのオブジェクトからページを指定した状態のオブジェクトつくってる
        params['data_p'] = data_page.get_page(page)

        # 指定したページのオブジェクトからページリンク先のリストを作っている
        params['data_list'] = params['data_p'].paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds) 
    
            
    return render(request,'books/place_delete.html', params)

class PlaceDeleteView(DeleteView):
    template_name = "books/place_change.html"
    model = Place
    success_url = reverse_lazy('books:place_delete', args=[1])

import requests
import json
    

class BookCreateView(CreateView):
    form_class = BookForm
    template_name = "books/book_create.html"
    success_url = reverse_lazy("books:book_create")

def ISBNAPIGet(request):
    if (request.method == 'POST'):
        isbn=request.POST['isbn']
        url = "https://api.openbd.jp/v1/get"

        headers= {
        
        }
        params={
            "isbn":isbn
        }

        result = requests.get(url, headers=headers, params=params)

        res = result.json()

        # (res["onix"]["RecordReference"])
        data = {
            "isbn":[],
            "title":[],
            "author":[],
            "volume":[],
            "series":[],
            "publisher":[],
            "pubdate":[],
            "cover":[],
        }
        data['isbn']=\
        (res[0]["summary"]["isbn"])
        data['title']=(res[0]["summary"]["title"])
        data['author']=(res[0]["summary"]["author"])
        data['volume']=(res[0]["summary"]["volume"])
        data['series']=(res[0]["summary"]["series"])
        data['publisher']=(res[0]["summary"]["publisher"])
        data['pubdate']=(res[0]["summary"]["pubdate"])
        data['cover']=(res[0]["summary"]["cover"])
    else:
        url = "https://api.openbd.jp/v1/get"

        headers= {
        
        }
        params={
            "isbn":9784780802047
        }

        result = requests.get(url, headers=headers, params=params)

        res = result.json()

        # (res["onix"]["RecordReference"])
        data = {
            "isbn":[],
            "title":[],
            "author":[],
            "volume":[],
            "series":[],
            "publisher":[],
            "pubdate":[],
            "cover":[],
        }
        data['isbn']=\
        (res[0]["summary"]["isbn"])
        data['title']=(res[0]["summary"]["title"])
        data['author']=(res[0]["summary"]["author"])
        data['volume']=(res[0]["summary"]["volume"])
        data['series']=(res[0]["summary"]["series"])
        data['publisher']=(res[0]["summary"]["publisher"])
        data['pubdate']=(res[0]["summary"]["pubdate"])
        data['cover']=(res[0]["summary"]["cover"])
    return render(request, 'books/bookdata.html', data)

class BookCreateView(CreateView):
    form_class = BookForm
    template_name = "books/book_create.html"
    success_url = reverse_lazy("books:book_create")

import requests

def get_book_data(isbn):
    url = "https://api.openbd.jp/v1/get"
    params = {"isbn": isbn}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data and "summary" in data[0]:
            summary = data[0]["summary"]
            return {
                "isbn": summary.get("isbn", ""),
                "title": summary.get("title", ""),
                "author": summary.get("author", ""),
                "publisher": summary.get("publisher", ""),
                "pubdate": summary.get("pubdate", ""),
                "cover": summary.get("cover", "")
            }
    return None

class BookCreateView1(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/ISBN_search.html'

    def get_initial(self):
        initial = super().get_initial()
        
        # URLのGETパラメータからISBNを取得
        isbn = self.request.GET.get('isbn')
        if isbn:
            # ISBNがある場合、APIからデータを取得して初期値として設定
            book_data = get_book_data(isbn)
            if book_data:
                initial.update(book_data)
        
        return initial

    def form_valid(self, form):
        # フォームが有効な場合、データを保存
        
        cleaned_data = form.cleaned_data
        book = Book.objects.create(
            isbn=cleaned_data['isbn'],
            title=cleaned_data['title'],
            author=cleaned_data['author'],
            publisher=cleaned_data.get('publisher', ''),
            pubdate=cleaned_data.get('pubdate', None),
            cover=cleaned_data.get('cover', ''),
            place=cleaned_data.get('place', '')  # 場所情報も保存
        )
        
        return reverse("accounts:index")  # 保存後、詳細ページへリダイレクト