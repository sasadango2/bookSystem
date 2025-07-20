from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    """日付に指定した日数を追加する"""
    if isinstance(value, str):
        # 文字列の場合は日付に変換
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return value
    
    if hasattr(value, 'date'):
        # datetimeオブジェクトの場合
        value = value.date()
    
    try:
        return value + timedelta(days=int(days))
    except (ValueError, TypeError):
        return value
