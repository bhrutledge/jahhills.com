from datetime import date, timedelta


def from_today(days=0):
    return date.today() + timedelta(days)


date_format = '%Y-%m-%d'.format
