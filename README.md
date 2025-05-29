# 図書館アプリ

## 目次

1. [概要](#概要)
2. [アプリ用件](#アプリ用件)
3. [スキルシート](#スキルシート)
4. [動作環境](#動作環境)
5. [操作方法](#操作方法)
6. [設計図など](#設計図など)
7. [ツリー](#ツリー)

## 概要
ある会社のビル内に点在している書籍を管理し、貸出・返却を行うことを想定したアプリ

### アプリ用件
基本データ
- ビル専有フロア数：20フロア
- 社員数：約4,000人
- 本棚数：約50箇所
- 総冊数（推定）：約15,000冊
- ビル内の分散した場所に書籍を保管したままデータを管理し、貸出・返却を行う

## スキルシート
[スキルシート.pdf](https://github.com/user-attachments/files/20476029/default.pdf)

## 動作環境
- Windows 11 Pro 24H2
- Python 3.12.7
- Django 4.2.2
- MariaDB 11.6.2
- django-bootstrap5

## 操作方法
### 1. 管理者及びユーザーができること

#### 1.1 ログイン・新規作成
ログインページで自分の設定したユーザーネームとパスワードを入力して青色のLoginボタンをクリックでログインされ、マイページ・管理者ページに遷移する。ログイン時にユーザーネームやパスワードが分からない場合は下のリンクからメールアドレスを入力してパスワード変更やユーザーネームの送信ができる。
グレーのCreateボタンをクリックするとアカウント作成画面に遷移する。

ログイン画面  
![スクリーンショット 2025-05-28 113005](https://github.com/user-attachments/assets/6f6bd4ce-f015-47e8-9f09-f88186e32e38)

アカウント作成画面で情報を入力して青色のCreateボタンをクリックするとアカウントが作成され、マイページに遷移する。

アカウント作成画面  
![スクリーンショット 2025-05-28 115648](https://github.com/user-attachments/assets/6a1a447a-47f4-409c-898b-c70f8ec7197f)

マイページ  
![スクリーンショット 2025-05-28 114251](https://github.com/user-attachments/assets/f95d84e0-2be3-4f63-9fb4-8bc1ad0e07ec)

管理者ページ  
![スクリーンショット 2025-05-28 114436](https://github.com/user-attachments/assets/b7ee4bd8-f442-41ef-9743-52cc19028512)

#### 1.2 本を探す・貸出・予約
マイページまたは管理者ページのユーザーメニューから「本を探す」をクリックで検索ページに遷移、上部のテキストボックスから書籍の検索ができる。

検索ページ  
![スクリーンショット 2025-05-28 120619](https://github.com/user-attachments/assets/a573aaab-95ab-4556-a5e3-9845513112a9)

書影または借りる・予約ボタンをクリックで書籍の詳細ページに遷移。

書籍詳細ページ  
![スクリーンショット 2025-05-28 121108](https://github.com/user-attachments/assets/9438f9f4-59a7-4583-8bb1-9e3da7b58e9c)

借りる・予約ボタンをクリックで日付を選択し、青色のBorrowボタンで書籍を貸出・予約できる。

日付選択ページ  
![スクリーンショット 2025-05-28 121401](https://github.com/user-attachments/assets/8054b7a2-71fb-4af0-a0c6-df8d08cee08f)

貸出完了ページ  
![スクリーンショット 2025-05-28 121415](https://github.com/user-attachments/assets/74c2bfa4-f113-4cdb-bbd2-0898f192e50b)

#### 1.3 本棚
マイページまたは管理者ページのユーザーメニューから「本棚」をクリックで本棚ページに遷移。ランダムに本が表示されるため、読みたい本が決まっていないが読書がしたい時などの利用想定。

本棚ページ  
![スクリーンショット 2025-05-28 122311](https://github.com/user-attachments/assets/3cf118e7-9a47-4e2b-b287-cc1b76c18dce)

#### 1.4 返却・キャンセル
マイページまたは管理者ページ下部の「予約・貸出中の本」から返却・キャンセルボタンをクリックすると、確認メッセージが表示され、OKボタンで返却・キャンセルできる。

確認メッセージ  
![スクリーンショット 2025-05-28 122706](https://github.com/user-attachments/assets/0c4c6e73-91b4-4490-b402-a087acce1a13)

#### 1.5 貸出履歴・レビュー
マイページまたは管理者ページのユーザーメニューから「貸出履歴」をクリックで貸出履歴ページに遷移。
貸出履歴からレビューの投稿や自分のレビューを見ることができる。

貸出履歴  
![スクリーンショット 2025-05-28 122946](https://github.com/user-attachments/assets/e5e40794-575f-4b34-ba4b-58617443fbc5)

レビュー投稿ページ  
![スクリーンショット 2025-05-28 133222](https://github.com/user-attachments/assets/5c811399-0edb-4517-a757-0e82fb39a380)

自分のレビュー  
![スクリーンショット 2025-05-28 133235](https://github.com/user-attachments/assets/be735d87-fb52-4fee-a83a-e2305854d1a6)

#### 1.6 その他
その他にもユーザーはパスワード変更・アカウント情報の更新・アカウントの非アクティブ化ができる。


### 2. 管理者のみできること

#### 2.1 書籍の代理返却
管理者ページから「書籍の返却」をクリックで全ユーザーの現在貸出・予約中の書籍一覧が見られる。返却・キャンセルボタンで操作できる。

貸出中の本リスト  
![スクリーンショット 2025-05-28 135405](https://github.com/user-attachments/assets/a847b599-adfa-4de0-bf20-b3eb3f9bf7d5)

#### 2.2 書籍登録
管理者ページから「書籍登録」をクリックで書籍登録ページに遷移。ISBNで書籍を検索して情報の自動入力もできる(使用したAPIに登録されているもののみ)。

書籍登録ページ  
![スクリーンショット 2025-05-28 135640](https://github.com/user-attachments/assets/f22edb9d-7a8d-4ae4-9306-f169dde10eca)
![スクリーンショット 2025-05-28 135713](https://github.com/user-attachments/assets/962c6a4b-0084-4aad-ab4f-68889494cdbb)

#### 2.3 書籍管理
管理者ページから「書籍登録」をクリックで書籍登録ページに遷移。書籍情報の編集・書籍削除ができる。

書籍管理ページ  
![スクリーンショット 2025-05-28 140257](https://github.com/user-attachments/assets/344c53e8-e7a4-4f2a-9c81-b32f3f9faaec)

書籍編集ページ  
![スクリーンショット 2025-05-28 140318](https://github.com/user-attachments/assets/63ea957e-1a2f-4f47-a243-0fe1c58a92b2)  
![スクリーンショット 2025-05-28 140419](https://github.com/user-attachments/assets/5e227deb-e77d-4f35-bba9-caf37da46df3)

書籍削除ページ  
![スクリーンショット 2025-05-28 141034](https://github.com/user-attachments/assets/45bda2f1-d7da-4bd0-9bc2-a3c6db3c25dd)

#### 2.4 場所登録・削除
管理者ページから「場所登録」・「場所削除」をクリックで場所登録・削除ページに遷移。本棚の場所の登録・削除ができる。

場所登録ページ  
![スクリーンショット 2025-05-28 141241](https://github.com/user-attachments/assets/2c4cb64c-4636-45a5-8fa7-2b8d95ab573c)

場所削除ページ  
![スクリーンショット 2025-05-28 141721](https://github.com/user-attachments/assets/f24397af-61ef-46bc-9530-81e2c19c73a7)

場所削除確認ページ  
![スクリーンショット 2025-05-28 141733](https://github.com/user-attachments/assets/42ae3999-10bb-4715-9879-83548d9c408f)

#### 2.5 アカウント管理
アカウント情報の編集・非アクティブ化・管理者化ができる。

アカウント管理ページ  
![スクリーンショット 2025-05-28 142210](https://github.com/user-attachments/assets/b96f3a6a-2055-4ddf-b9d4-1f5c2f5baeed)

アカウント編集ページ  
![スクリーンショット 2025-05-28 142355](https://github.com/user-attachments/assets/a65a2e0b-f803-47bf-b97c-bf3162d09436)

## 設計図など

画面遷移図  
![画面遷移図 drawio](https://github.com/user-attachments/assets/a0131046-54f9-427d-a866-095064919742)

ユースケース図  
![ユースケース図 drawio](https://github.com/user-attachments/assets/48bd99da-69c4-4745-be8f-684c24941c70)

E-R図  
![E-R図 drawio](https://github.com/user-attachments/assets/ec5bd662-e1ef-4ad0-bc16-143897af8375)

[モックへのリンク](https://www.figma.com/proto/bYSFGTC9ZEoACJ4Q9PX7NS/%E4%BB%AE?node-id=7-187&p=f&t=bWhp48EfRlNgJFvS-1&scaling=contain&content-scaling=fixed&page-id=0%3A1)  

[テスト仕様書](https://github.com/user-attachments/files/20475841/default.xlsx)

[マニュアル](https://github.com/user-attachments/files/20475858/manual.pdf)

## ツリー

C:.\
│  .gitignore\
│  asgi.py\
│  manage.py\
│  python\
│  README.md\
│  settings.py\
│  urls.py\
│  wsgi.py\
│  __init__.py\
│\
├─.VSCodeCounter\
│  └─2025-05-09_14-35-37\
│          details.md\
│          diff-details.md\
│          diff.csv\
│          diff.md\
│          diff.txt\
│          results.csv\
│          results.json\
│          results.md\
│          results.txt\
│\
├─accounts\
│  │  admin.py\
│  │  apps.py\
│  │  bootstrap.txt\
│  │  forms.py\
│  │  models.py\
│  │  tests.py\
│  │  urls.py\
│  │  views.py\
│  │  __init__.py\
│  │\
│  ├─migrations\
│  │  │  0001_initial.py\
│  │  │  0002_alter_user_created_at_alter_user_email_and_more.py\
│  │  │  0003_user_borrow.py\
│  │  │  0004_remove_user_borrow.py\
│  │  │  __init__.py\
│  │  │\
│  │  └─__pycache__\
│  │          0001_initial.cpython-312.pyc\
│  │          0002_alter_user_created_at_alter_user_email_and_more.cpython-312.pyc\
│  │          0003_user_borrow.cpython-312.pyc\
│  │          0004_remove_user_borrow.cpython-312.pyc\
│  │          __init__.cpython-312.pyc\
│  │\
│  └─__pycache__\
│          admin.cpython-312.pyc\
│          apps.cpython-312.pyc\
│          forms.cpython-312.pyc\
│          models.cpython-312.pyc\
│          urls.cpython-312.pyc\
│          views.cpython-312.pyc\
│          __init__.cpython-312.pyc\
│\
├─books\
│  │  admin.py\
│  │  apps.py\
│  │  forms.py\
│  │  models.py\
│  │  tests.py\
│  │  update.py\
│  │  urls.py\
│  │  views.py\
│  │  __init__.py\
│  │\
│  ├─migrations\
│  │  │  0001_initial.py\
│  │  │  0002_place_is_active.py\
│  │  │  0003_book.py\
│  │  │  0004_book_isbn.py\
│  │  │  0005_alter_book_cover_alter_book_isbn_alter_book_pubdate_and_more.py\
│  │  │  0006_remove_place_is_active.py\
│  │  │  0007_alter_book_pubdate_alter_place_place.py\
│  │  │  0008_book_is_borrowed.py\
│  │  │  0009_alter_book_pubdate.py\
│  │  │  0010_lenging.py\
│  │  │  0011_rename_lenging_lending.py\
│  │  │  0012_alter_lending_date.py\
│  │  │  0013_lending_is_returned.py\
│  │  │  0014_review.py\
│  │  │  0015_alter_review_rating_alter_review_review_text.py\
│  │  │  0016_book_authorkana_book_pubkana_book_titlekana.py\
│  │  │  0017_alter_book_author_alter_book_authorkana_and_more.py\
│  │  │  0018_book_description.py\
│  │  │  0019_alter_lending_book_alter_lending_username.py\
│  │  │  0020_alter_review_rating.py\
│  │  │  __init__.py\
│  │  │\
│  │  └─__pycache__\
│  │          0001_initial.cpython-312.pyc\
│  │          0002_place_is_active.cpython-312.pyc\
│  │          0003_book.cpython-312.pyc\
│  │          0004_book_isbn.cpython-312.pyc\
│  │          0005_alter_book_cover_alter_book_isbn_alter_book_pubdate_and_more.cpython-312.pyc\
│  │          0006_remove_place_is_active.cpython-312.pyc\
│  │          0007_alter_book_pubdate_alter_place_place.cpython-312.pyc\
│  │          0008_book_is_borrowed.cpython-312.pyc\
│  │          0009_alter_book_pubdate.cpython-312.pyc\
│  │          0010_lenging.cpython-312.pyc\
│  │          0011_rename_lenging_lending.cpython-312.pyc\
│  │          0012_alter_lending_date.cpython-312.pyc\
│  │          0013_lending_is_returned.cpython-312.pyc\
│  │          0014_review.cpython-312.pyc\
│  │          0015_alter_review_rating_alter_review_review_text.cpython-312.pyc\
│  │          0016_book_authorkana_book_pubkana_book_titlekana.cpython-312.pyc\
│  │          0017_alter_book_author_alter_book_authorkana_and_more.cpython-312.pyc\
│  │          0018_book_description.cpython-312.pyc\
│  │          0019_alter_lending_book_alter_lending_username.cpython-312.pyc\
│  │          0020_alter_review_rating.cpython-312.pyc\
│  │          __init__.cpython-312.pyc\
│  │\
│  └─__pycache__\
│          admin.cpython-312.pyc\
│          apps.cpython-312.pyc\
│          forms.cpython-312.pyc\
│          models.cpython-312.pyc\
│          update.cpython-312.pyc\
│          urls.cpython-312.pyc\
│          views.cpython-312.pyc\
│          __init__.cpython-312.pyc\
│\
├─static\
│  └─css\
│          style.css\
│\
├─templates\
│  │  404.html\
│  │  500.html\
│  │  base.html\
│  │  bootstrap.html\
│  │  index.html\
│  │\
│  ├─accounts\
│  │      accounts_change.html\
│  │      accounts_delete.html\
│  │      borrowing_history.html\
│  │      forget.html\
│  │      my_review_detail.html\
│  │      page.html\
│  │      password_change.html\
│  │      password_change_done.html\
│  │      password_reset.html\
│  │      password_reset_complete.html\
│  │      password_reset_confirm.html\
│  │      password_reset_done.html\
│  │      signup.html\
│  │      staff_accounts_change.html\
│  │      staff_search_user.html\
│  │      username_reset.html\
│  │      username_reset_done.html\
│  │\
│  ├─books\
│  │      add_review.html\
│  │      bookdata.html\
│  │      book_delete.html\
│  │      book_detail.html\
│  │      book_manage.html\
│  │      book_search.html\
│  │      book_shelf.html\
│  │      book_update.html\
│  │      borrowed_books_list.html\
│  │      ISBN_search.html\
│  │      lending.html\
│  │      lending_done.html\
│  │      place_change.html\
│  │      place_delete.html\
│  │      place_make.html\
│  │\
│  └─mail\
│          message.txt\
│          message_username.txt\
│          subject.txt\
│          subject_username.txt\
│\
├─tosho_app\
│  │  asgi.py\
│  │  settings.py\
│  │  urls.py\
│  │  wsgi.py\
│  │  __init__.py\
│  │\
│  └─__pycache__\
│          settings.cpython-312.pyc\
│          urls.cpython-312.pyc\
│          wsgi.cpython-312.pyc\
│          __init__.cpython-312.pyc\
│\
└─__pycache__\
        settings.cpython-312.pyc\
        urls.cpython-312.pyc\
        wsgi.cpython-312.pyc\
        __init__.cpython-312.pyc







