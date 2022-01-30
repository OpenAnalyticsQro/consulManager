from datetime import date

def get_week(year=2022, month=1, day=1):
    _date = date(year=year,month=month, day=day)
    return f"SEMANA-{_date.isocalendar()[1]}-{year}"

def get_valid_date(day=1, month=1, year=2022):
    return f"{year}-{month:02}-{day:02}"