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

    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.delete()
            return HttpResponseRedirect(self.success_url)
        except models.ProtectedError as e:
            messages.error(request, f'「{obj}」の本棚にはまだ本があります。')

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

from django.http import HttpResponseRedirect
from django.urls import reverse

class BookCreateView1(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/ISBN_search.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        isbn = request.GET.get('isbn')  # ISBNがGETリクエストに含まれている場合

        if isbn:
            # ISBNが指定されている場合、APIからデータを取得してフォームにセット
            try:
                book_data = get_book_data(isbn)
            except:
                # リクエストエラーが発生した場合、ログに記録してNoneを返す
                messages.error(request, '書籍が見つかりませんでした。手動でデータを入力してください。')
            # APIから取得したデータをフォームに反映
            form = self.form_class(initial=book_data)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        # フォームが有効な場合、データを保存
        if form.is_valid():
            form.save()  # Bookオブジェクトを保存
            return HttpResponseRedirect(reverse('books:book_detail', kwargs={'pk': form.instance.pk}))  # 保存後に詳細ページにリダイレクト

        # フォームが無効な場合は再度表示
        return render(request, self.template_name, {'form': form})
    
from django.http import Http404
from django.views.generic import DetailView

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_object(self):
        # URLから取得するPKで書籍を取得
        pk = self.kwargs.get('pk')
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404