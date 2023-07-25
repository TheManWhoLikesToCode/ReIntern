from datetime import datetime

def calculate_days_until_friday():
    today = datetime.today().weekday()
    friday = 4  # Monday is 0, Sunday is 6
    days_until = (friday - today) % 7
    return days_until
