"""Shared calendar helpers — week starts on Saturday."""

from datetime import date, timedelta

WEEKDAY_KEYS = ["sat", "sun", "mon", "tue", "wed", "thu", "fri"]
WEEKDAY_LABELS_SHORT = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]


def get_weekday_labels_short() -> list[str]:
    """Return localized short weekday labels without coupling this module to DB init."""
    try:
        from core.language_manager import get_language_manager

        manager = get_language_manager()
        labels = []
        for key in WEEKDAY_KEYS:
            translated = manager.translate(f"{key}_short")
            labels.append(translated if translated != f"{key}_short" else WEEKDAY_LABELS_SHORT[WEEKDAY_KEYS.index(key)])
        return labels
    except Exception:
        return WEEKDAY_LABELS_SHORT.copy()


def start_of_week(d: date | None = None) -> date:
    today = d or date.today()
    weekday = (today.weekday() + 2) % 7  # Sat=0 … Fri=6
    return today - timedelta(days=weekday)


def end_of_week(d: date | None = None) -> date:
    return start_of_week(d) + timedelta(days=6)
