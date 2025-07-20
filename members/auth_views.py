from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class CustomLoginView(LoginView):
    """
    カスタムログインビュー
    管理者の場合は /admin に、一般ユーザーは / にリダイレクト
    """
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        
        # 管理者（is_staff または is_superuser）の場合は管理画面へ
        if user.is_staff or user.is_superuser:
            messages.success(self.request, f'管理者として {user.username} さんがログインしました。')
            return '/admin/'
        
        # 一般ユーザーの場合はホームページへ
        messages.success(self.request, f'{user.username} さん、ようこそ！')
        return '/'
    
    def form_valid(self, form):
        """ログイン成功時の処理"""
        user = form.get_user()
        login(self.request, user)
        
        # 会員プロファイルの確認と権限同期
        try:
            profile = user.member_profile
            # プロファイルが管理者タイプの場合、Django権限も同期
            if profile.membership_type == 'admin':
                if not user.is_staff:
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
        except:
            # プロファイルが存在しない場合は何もしない
            pass
        
        return redirect(self.get_success_url())
