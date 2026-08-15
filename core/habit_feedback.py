"""Feedback messages after habit check/uncheck."""

from database.repository import habit_repo
from core.streak_engine import daily_streak
from core.language_manager import tr

STREAK_MILESTONES = (3, 7, 14, 30)


def get_habit_toggle_feedback(habit_id: int, habit_name: str, was_done: bool):
    """
    Return toast payload after toggling a habit.

    Returns:
        (title, message, icon, kind) or (None, None, None, None) if no toast.
    """
    display_name = tr(habit_name)

    if was_done:
        return (
            tr("habit_unchecked"),
            tr("habit_unchecked_desc").format(name=display_name),
            "↩",
            "info",
        )

    habits = habit_repo.get_all_habits()
    if habits and all(habit_repo.is_habit_done_today(h.id) for h in habits):
        return (
            tr("perfect_day"),
            tr("perfect_day_desc"),
            "⭐",
            "perfect",
        )

    streak = daily_streak(habit_id)
    if streak in STREAK_MILESTONES:
        return (
            tr("streak_milestone_title").format(streak=streak),
            tr("streak_milestone_desc").format(name=display_name, streak=streak),
            "🔥",
            "milestone",
        )

    return (
        tr("habit_completed"),
        tr("habit_completed_desc").format(name=display_name),
        "✅",
        "success",
    )
