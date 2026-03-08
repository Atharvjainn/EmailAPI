from datetime import datetime
import re

today = datetime.now().date()

def clean_email(text):
    return re.sub(r'\n+', '\n', text).strip()

def calculate_urgency(item):
    days_remaining = (item.deadline - today).days

    if days_remaining < 0:
        return 10  # overdue = critical
    elif days_remaining <= 2:
        return 9
    elif days_remaining <= 7:
        return 8
    elif days_remaining <= 14:
        return 6
    elif days_remaining <= 30:
        return 4
    else:
        return 2