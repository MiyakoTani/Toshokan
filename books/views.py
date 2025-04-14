from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime, requests
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.db import models
from django.contrib import messages
from .forms import PlaceForm, BookForm, BookUpdateForm, LendingForm
from .models import Place,Book,Lending,Review
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

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        isbn = request.GET.get('isbn')  # ISBNがGETリクエストに含まれている場合

        if isbn:
            # ISBNが指定されている場合、APIからデータを取得してフォームにセット
            try:
                book_data = get_book_data(isbn)
                # APIから取得したデータをフォームに反映
                form = self.form_class(initial=book_data)
            except:
                # リクエストエラーが発生した場合、ログに記録してNoneを返す
                messages.error(request, '書籍が見つかりませんでした。手動でデータを入力してください。')
            

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        # フォームが有効な場合、データを保存
        if form.is_valid():
            form.save()  # Bookオブジェクトを保存
            return HttpResponseRedirect(reverse('books:book_detail', kwargs={'pk': form.instance.pk}))  # 保存後に詳細ページにリダイレクト
        else:
        # フォームが無効な場合は再度表示
            return render(request, self.template_name, {'form': form})

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews = Review.objects.filter(book=book).order_by('-created_at')
        context['reviews'] = reviews
        return context
        
def book_manage(request, page=1):
    params = {
        'data': [],
        'data_p': [],
        'data_list': [],
    }

    page_cnt = 8  # 一画面あたり5コ表示する
    onEachSide = 3  # 選択ページの両側には3コ表示する
    onEnds = 2  # 左右両端には2コ表示する

    # フィルタリングのための検索パラメータを取得
    id_filter = request.POST.get('id', '')
    title_filter = request.POST.get('title', '')
    place_filter = request.POST.get('place', '')

    # フィルタリングの条件を作成
    query_filter = Book.objects.all()

    if id_filter:
        query_filter = query_filter.filter(id=id_filter)
    if title_filter:
        query_filter = query_filter.filter(title__icontains=title_filter)  # 部分一致
    if place_filter:
        query_filter = query_filter.filter(place__place__icontains=place_filter)  # 部分一致

    # 検索結果があれば、そのデータを使用し、なければすべてのデータを表示
    if query_filter.exists():
        params['data'] = query_filter
    else:
        params['data'] = Book.objects.order_by('id').all()

    # paginatorのオブジェクトをつくってる
    data_page = Paginator(params['data'], page_cnt)

    # paginatorのオブジェクトからページを指定した状態のオブジェクトつくってる
    params['data_p'] = data_page.get_page(page)

    # 指定したページのオブジェクトからページリンク先のリストを作っている
    params['data_list'] = params['data_p'].paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds)

    return render(request, 'books/book_manage.html', params)

class BookDeleteView(DeleteView):
    template_name = "books/book_delete.html"
    model = Book
    success_url = reverse_lazy('books:book_manage', args=[1])

class BookUpdateView(UpdateView):
    form_class = BookUpdateForm
    model = Book
    template_name = "books/book_update.html"
    success_url = reverse_lazy('books:book_manage', args=[1])

def book_search(request, page=1):
    params = {
        'data': [],
        'data_p': [],
        'data_list': [],
        'place' : [],
    }

    page_cnt = 5  # 一画面あたり5コ表示する
    onEachSide = 3  # 選択ページの両側には3コ表示する
    onEnds = 2  # 左右両端には2コ表示する

    # フィルタリングのための検索パラメータを取得
    title_filter = request.POST.get('title', '')
    author_filter = request.POST.get('author', '')
    publisher_filter = request.POST.get('publisher', '')
    pubdate_filter = request.POST.get('pubdate', '')
    place_filter = request.POST.get('place', '')

    # フィルタリングの条件を作成
    query_filter = Book.objects.all()

    if title_filter:
        query_filter = query_filter.filter(title__icontains=title_filter)  # 部分一致
    if author_filter:
        query_filter = query_filter.filter(author__icontains=author_filter)  # 部分一致
    if publisher_filter:
        query_filter = query_filter.filter(publisher__icontains=publisher_filter)  # 部分一致
    if pubdate_filter:
        query_filter = query_filter.filter(pubdate__icontains=pubdate_filter)  # 部分一致
    if place_filter:
        query_filter = query_filter.filter(place__place__icontains=place_filter)  # 部分一致

    params['place'] = Place.objects.all()

    # 検索結果があれば、そのデータを使用し、なければすべてのデータを表示
    if query_filter.exists():
        params['data'] = query_filter
    else:
        params['data'] = Book.objects.order_by('id').all()

    # paginatorのオブジェクトをつくってる
    data_page = Paginator(params['data'], page_cnt)

    # paginatorのオブジェクトからページを指定した状態のオブジェクトつくってる
    params['data_p'] = data_page.get_page(page)

    # 指定したページのオブジェクトからページリンク先のリストを作っている
    params['data_list'] = params['data_p'].paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds)

    return render(request, 'books/book_search.html', params)

def book_shelf(request, page=1):
    params = {
        'data': [],
        'data_p': [],
        'data_list': [],
    }

    page_cnt = 30  # 一画面あたり5コ表示する
    onEachSide = 3  # 選択ページの両側には3コ表示する
    onEnds = 2  # 左右両端には2コ表示する

    params['data'] = Book.objects.order_by('?').filter(is_borrowed=False)


    # paginatorのオブジェクトをつくってる
    data_page = Paginator(params['data'], page_cnt)

    # paginatorのオブジェクトからページを指定した状態のオブジェクトつくってる
    params['data_p'] = data_page.get_page(page)

    # 指定したページのオブジェクトからページリンク先のリストを作っている
    params['data_list'] = params['data_p'].paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds)

    return render(request, 'books/book_shelf.html', params)

from django.db.models import Q

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = LendingForm(request.POST)
        if form.is_valid():
            requested_start = form.cleaned_data['date']
            requested_end = form.cleaned_data['returndate']
            overlap_exists = Lending.objects.filter(
                book=book,
                returndate__gte=form.cleaned_data['date'],
                date__lte=form.cleaned_data['returndate']
            ).exists()

            # 他のLendingと期間が重複しているかチェック
            overlap_exists = Lending.objects.filter(
                book=book,
                is_returned=False,
                returndate__gte=requested_start,
                date__lte=requested_end
            ).exists()
            
            if overlap_exists:
                messages.error(request, f'この期間にはすでに予約または貸出があります。')
                return redirect(reverse('books:borrow', kwargs={'pk': pk}))
                    
            
            # 問題なければ貸出または予約処理
            lending = form.save(commit=False)
            lending.book = book
            lending.username = request.user
            lending.save()

            # 本日借りる場合は貸出状態に
            if lending.date == datetime.date.today():
                book.is_borrowed = True
                book.save()

            return render(request, 'books/lending_done.html', {'lending': lending, 'book': book})
    else:
        form = LendingForm()

    return render(request, 'books/lending.html', {'form': form, 'book': book})

class LendingDoneView(TemplateView):
    template_name = "books/lending_done.html"

@login_required
def cancel_reservation(request, lending_id):
    lending = get_object_or_404(Lending, pk=lending_id, username=request.user)

    if lending.date > datetime.date.today():  # 未来の予約のみキャンセル可能
        lending.delete()

    return redirect('accounts:index')

@login_required
def return_book(request, lending_id):
    # Lendingオブジェクトを取得
    lending = get_object_or_404(Lending, id=lending_id)
    
    # Lendingのis_returnedをTrueにする
    lending.is_returned = True
    lending.returndate = datetime.date.today()
    lending.save()

    # 対応するBookのis_borrowedをFalseにする
    book = lending.book
    book.is_borrowed = False
    book.save()

    # 返却後、マイページにリダイレクト
    return redirect('accounts:index')

@login_required
def add_review(request, book_id):
    # レビューを追加する本を取得
    book = get_object_or_404(Book, id=book_id)
    
    # すでにその本を借りているか確認
    lending = Lending.objects.filter(book=book, username=request.user)
    if not lending:
        return redirect('accounts:borrowing_history')  # まだ借りていない本にはレビューできない

    # レビューを追加する
    if request.method == 'POST':
        # レビュー内容と評価をフォームから取得
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')  # ここで星の評価を受け取る
        
        # レビューを保存
        review = Review.objects.create(
            user=request.user,
            book=book,
            review_text=review_text,
            rating=rating
        )

        return redirect('accounts:borrowing_history')  # レビュー投稿後、貸出履歴ページに戻る

    return render(request, 'books/add_review.html', {'book': book})

def borrowed_books_list(request, page=1):
    # 貸出中のデータを取得
    params = {
        'data': [],
        'data_p': [],
        'data_list': [],
        'today' :[],
    }

    page_cnt = 5  # 一画面あたり5コ表示する
    onEachSide = 3  # 選択ページの両側には3コ表示する
    onEnds = 2  # 左右両端には2コ表示する
    
    params['today'] = datetime.date.today()
    # フィルタリングのための検索パラメータを取得
    title_filter = request.POST.get('title', '')
    author_filter = request.POST.get('author', '')
    username_filter = request.POST.get('username', '')
    place_filter = request.POST.get('place', '')
    status_filter = request.POST.get('status', '')
    today = datetime.date.today()

    # フィルタリングの条件を作成
    query_filter = Lending.objects.order_by('returndate').filter(is_returned=False)

    if title_filter:
        query_filter = query_filter.filter(book__title__icontains=title_filter)  # 部分一致
    if author_filter:
        query_filter = query_filter.filter(book__author__icontains=author_filter)  # 部分一致
    if username_filter:
        query_filter = query_filter.filter(username__username__icontains=username_filter)  # 部分一致
    if place_filter:
        query_filter = query_filter.filter(book__place__place__icontains=place_filter)  # 部分一致
    if status_filter == 'expired':
        query_filter = query_filter.filter(returndate__lt=today, date__lte=today)
    elif status_filter == 'reserved':
        query_filter = query_filter.filter(date__gt=today)
    elif status_filter == 'borrowed':
        query_filter = query_filter.filter(date__lte=today, returndate__gte=today)

    # 検索結果があれば、そのデータを使用し、なければすべてのデータを表示
    if query_filter.exists():
        params['data'] = query_filter
    else:
        params['data'] = Lending.objects.order_by('returndate').filter(is_returned=False)

    # paginatorのオブジェクトをつくってる
    data_page = Paginator(params['data'], page_cnt)

    # paginatorのオブジェクトからページを指定した状態のオブジェクトつくってる
    params['data_p'] = data_page.get_page(page)

    # 指定したページのオブジェクトからページリンク先のリストを作っている
    params['data_list'] = params['data_p'].paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds)
    return render(request, 'books/borrowed_books_list.html', params)