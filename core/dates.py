"""Shared calendar helpers — week starts on Saturday."""

from datetime import date, timedelta

WEEKDAY_LABELS_SHORT = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]


def start_of_week(d: date | None = None) -> date:
    today = d or date.today()
    weekday = (today.weekday() + 2) % 7  # Sat=0 … Fri=6
    return today - timedelta(days=weekday)


def end_of_week(d: date | None = None) -> date:
    return start_of_week(d) + timedelta(days=6)
