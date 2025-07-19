from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import MemberProfile, LibraryNotification
from .forms import MemberProfileForm
import uuid

@login_required
def member_profile(request):
    try:
        profile = request.user.member_profile
    except MemberProfile.DoesNotExist:
        return redirect('members:member_register')
    
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=profile)
        if form.is_valid():
            updated_profile = form.save()
            
            # 管理者を選択した場合はDjango管理画面にアクセス可能にする
            if updated_profile.membership_type == 'admin':
                request.user.is_staff = True
                request.user.is_superuser = True
                request.user.save()
            else:
                # 管理者以外の場合は権限を削除
                request.user.is_staff = False
                request.user.is_superuser = False
                request.user.save()
            
            messages.success(request, 'プロファイルを更新しました。')
            return redirect('members:member_profile')
    else:
        form = MemberProfileForm(instance=profile)
    
    return render(request, 'members/profile.html', {
        'form': form,
        'profile': profile
    })

def member_register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = MemberProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.member_id = f"M{uuid.uuid4().hex[:8].upper()}"
            profile.phone = ""  # デフォルト値
            profile.address = ""  # デフォルト値
            
            # 管理者を選択した場合はDjango管理画面にアクセス可能にする
            if profile.membership_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
            
            profile.save()
            
            login(request, user)
            messages.success(request, '会員登録が完了しました。')
            return redirect('members:member_profile')
    else:
        user_form = UserCreationForm()
        profile_form = MemberProfileForm()
    
    return render(request, 'members/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'members/notifications.html', {
        'notifications': notifications
    })

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(LibraryNotification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('members:notification_list')