from django import template
from myapp.models import Notification

register = template.Library()

@register.inclusion_tag('layouts/show_notifications.html', takes_context=True)

def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(to_user=request_user).exclude(seen=True).order_by('-created_at')
    return {'notifications': notifications}