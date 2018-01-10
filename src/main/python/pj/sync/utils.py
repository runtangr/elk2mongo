import datetime


def get_yest_str():
    yes_day = datetime.date.today() - datetime.timedelta(days=1)
    yest_str = yes_day.strftime("%Y%m%d")
    return yest_str
