from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView,  LogoutView as BaseLogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm, MyPasswordChangeForm, UserChangeForm, UserDeleteForm, StaffCreateForm, StaffAccountsChangeForm
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
    
def staff(request):
    params = {
        'form':StaffCreateForm(),
        'data':[],
    }
    if (request.method == 'POST'):
        num = request.POST['username']
        try:
            item = User.objects.get(username=num)
            params['data'] = [item]
            params['form'] = StaffCreateForm(request.POST)
        except:
            params['data'] = User.objects.all()
    else:
        params['data'] = User.objects.all()
    return render(request, 'accounts/staff_search_user.html', params)

def StaffAccountsChange(request, num):
    obj = User.objects.get(username=num)
    if (request.method == 'POST'):
        user = StaffAccountsChangeForm(request.POST, instance=obj)
        user.save()
        return redirect(to='/accounts/staff_search_user')
    params = {
        'username':num,
        'form': StaffAccountsChangeForm(instance=obj),
    }
    return render(request, 'accounts/staff_accounts_change.html', params)