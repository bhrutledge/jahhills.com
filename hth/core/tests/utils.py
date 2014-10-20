from datetime import date, timedelta


def today_str(days=0):
    return (date.today() + timedelta(days=days)).strftime('%Y-%m-%d')
