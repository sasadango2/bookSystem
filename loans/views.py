from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from books.models import Book
from .models import Loan, Reservation
from members.models import MemberProfile

@login_required
def loan_list(request):
    loans = request.user.loans.filter(status='borrowed').order_by('-loan_date')
    return render(request, 'loans/loan_list.html', {'loans': loans})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # 会員プロファイルを確認
    try:
        member_profile = request.user.member_profile
    except MemberProfile.DoesNotExist:
        messages.error(request, '会員登録が必要です。')
        return redirect('members:member_register')
    
    # 貸出可能かチェック
    if not member_profile.can_borrow:
        messages.error(request, '貸出上限に達しているか、アカウントが無効です。')
        return redirect('books:book_detail', id=book.id, slug=book.slug)
    
    if not book.is_available:
        messages.error(request, 'この書籍は現在貸出できません。')
        return redirect('books:book_detail', id=book.id, slug=book.slug)
    
    # 貸し出し処理
    loan = Loan.objects.create(
        user=request.user,
        book=book
    )
    
    # 在庫数を減らす
    book.available_copies -= 1
    book.save()
    
    messages.success(request, f'「{book.title}」を貸し出しました。')
    return redirect('loans:loan_list')

@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, user=request.user)
    
    if loan.status != 'borrowed':
        messages.error(request, 'この貸出記録は既に返却済みです。')
        return redirect('loans:loan_list')
    
    # 返却処理
    loan.return_date = timezone.now()
    loan.status = 'returned'
    loan.save()
    
    # 在庫数を増やす
    loan.book.available_copies += 1
    loan.book.save()
    
    messages.success(request, f'「{loan.book.title}」を返却しました。')
    return redirect('loans:loan_list')

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # 既に予約済みかチェック
    if Reservation.objects.filter(user=request.user, book=book, is_active=True).exists():
        messages.warning(request, 'この書籍は既に予約済みです。')
        return redirect('books:book_detail', id=book.id, slug=book.slug)
    
    # 予約作成
    reservation = Reservation.objects.create(
        user=request.user,
        book=book
    )
    
    messages.success(request, f'「{book.title}」を予約しました。')
    return redirect('loans:reservation_list')

@login_required
def reservation_list(request):
    reservations = request.user.reservations.filter(is_active=True).order_by('reservation_date')
    return render(request, 'loans/reservation_list.html', {'reservations': reservations})

@login_required
def loan_history(request):
    loans = request.user.loans.all().order_by('-loan_date')
    return render(request, 'loans/loan_history.html', {'loans': loans})

    