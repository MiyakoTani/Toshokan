from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView,  LogoutView as BaseLogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import SignUpForm, LoginForm, MyPasswordChangeForm, UserChangeForm, UserDeleteForm, StaffAccountsChangeForm, ForgetForm, UsernameForm
from .models import User



class IndexView(BaseLoginView):
    """ ホームビュー """
    form_class = LoginForm
    template_name = "index.html"


class SignupView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignUpForm # 作成した登録用フォームを設定
    template_name = "accounts/signup.html" 
    success_url = reverse_lazy("accounts:index") # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        user = form.save()
        login(self.request, user)
        return response

# LogoutView
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")

class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'

    # contextデータ作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Change Password"
        return context


'''パスワード変更完了'''
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

'''ユーザー編集機能'''
class UserChangeView(UpdateView):
    form_class = UserChangeForm
    template_name = "accounts/accounts_change.html"
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        return self.request.user
    
'''ユーザー削除機能'''
class UserDeleteView(UpdateView):
    form_class = UserDeleteForm
    template_name = "accounts/accounts_delete.html"
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        return self.request.user
    
def staff(request, page=1):
    params = {
        'data':[],
        'data_p':[],
        'data_list':[],
    }

    page_cnt = 5 #一画面あたり10コ表示する
    onEachSide = 3 #選択ページの両側には3コ表示する
    onEnds = 2 #左右両端には2コ表示する
    if (request.method == 'POST'):
        num = request.POST['username']
        try:
            item = User.objects.get(username=num)
            params['data_p'] = [item]
        except:
            params['data'] = User.objects.order_by('username').all()
            # paginatorのオブジェクトをつくってる
            data_page = Paginator(params['data'], page_cnt)
            
            # paginatorのオブジェクトからページを指定した状態のオブジェクトつくってる
            params['data_p'] = data_page.get_page(page)

            # 指定したページのオブジェクトからページリンク先のリストを作っている
            params['data_list'] = params['data_p'].paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds) 
    else:
        params['data'] = User.objects.order_by('username').all()
        # paginatorのオブジェクトをつくってる
        data_page = Paginator(params['data'], page_cnt)
        
        # paginatorのオブジェクトからページを指定した状態のオブジェクトつくってる
        params['data_p'] = data_page.get_page(page)

        # 指定したページのオブジェクトからページリンク先のリストを作っている
        params['data_list'] = params['data_p'].paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds) 
    
            
    return render(request,'accounts/staff_search_user.html', params)

def StaffAccountsChange(request, num):
    obj = User.objects.get(username=num)
    if (request.method == 'POST'):
        user = StaffAccountsChangeForm(request.POST, instance=obj)
        user.save()
        return redirect(to='/staff_search_user/1')
    params = {
        'username':num,
        'form': StaffAccountsChangeForm(instance=obj),
    }
    return render(request, 'accounts/staff_accounts_change.html', params)

class ForgetView(TemplateView):
    template_name = 'accounts/forget.html'

class PasswordResetView(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    # 送信元のGmailアカウント情報
    subject_template_name = 'mail/subject.txt'
    email_template_name = 'mail/message.txt'
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class PasswordResetDoneView(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirmView(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'

class PasswordResetCompleteView(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_complete.html'

class UsernameResetView(PasswordResetView):
    """ユーザーネーム変更用URLの送付ページ"""
    # 送信元のGmailアカウント情報
    subject_template_name = 'mail/subject_username.txt'
    email_template_name = 'mail/message_username.txt'
    template_name = 'accounts/username_reset.html'
    success_url = reverse_lazy('accounts:username_reset_done')

class UsernameResetDoneView(TemplateView):
    """ユーザーネーム変更用URLを送りましたページ"""
    template_name = 'accounts/username_reset_done.html'

