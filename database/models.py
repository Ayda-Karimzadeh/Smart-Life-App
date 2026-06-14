from dataclasses import dataclass
from typing import Optional


# ─── Habit ────────────────────────────────────────────────────────────────────
@dataclass
class Habit:
    id: int
    name: str
    icon: str
    category: str
    frequency_type: str       # 'daily' یا 'weekly'
    frequency_count: int       # چند بار در هفته
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        """تبدیل یه ردیف از دیتابیس به آبجکت Habit"""
        return cls(
            id=row[0], name=row[1], icon=row[2],
            category=row[3], frequency_type=row[4],
            frequency_count=row[5], created_at=row[6]
        )


# ─── Goal ─────────────────────────────────────────────────────────────────────
@dataclass
class Goal:
    id: int
    name: str
    description: str
    icon: str
    category: str
    deadline: Optional[str]
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0], name=row[1], description=row[2],
            icon=row[3], category=row[4],
            deadline=row[5], created_at=row[6]
        )


# ─── Milestone ────────────────────────────────────────────────────────────────
@dataclass
class Milestone:
    id: int
    goal_id: int
    name: str
    done: bool
    sort_order: int = 0

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0], goal_id=row[1], name=row[2],
            done=bool(row[3]), sort_order=row[4]
        )


# ─── Task ─────────────────────────────────────────────────────────────────────
@dataclass
class Task:
    id: int
    name: str
    description: str
    category: str
    priority: str             # High / Medium / Low
    due_date: Optional[str]
    due_time: Optional[str]
    done: bool
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0], name=row[1], description=row[2],
            category=row[3], priority=row[4],
            due_date=row[5], due_time=row[6],
            done=bool(row[7]), created_at=row[8]
        )


# ─── TimeSession ──────────────────────────────────────────────────────────────
@dataclass
class TimeSession:
    id: int
    name: str
    category: str
    duration: int              # ثانیه
    session_date: str
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row[0], name=row[1], category=row[2],
            duration=row[3], session_date=row[4], created_at=row[5]
        )

    @property
    def duration_str(self):
        """تبدیل ثانیه به فرمت 'Xh Ym'"""
        h = self.duration // 3600
        m = (self.duration % 3600) // 60
        if h > 0:
            return f"{h}h {m}m"
        return f"{m}m"