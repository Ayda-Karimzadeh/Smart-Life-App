from dataclasses import dataclass
from typing import Optional


@dataclass
class Habit:
    id: int
    name: str
    icon: str
    category: str
    frequency_type: str
    frequency_count: int
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], name=row[1], icon=row[2],
                   category=row[3], frequency_type=row[4],
                   frequency_count=row[5], created_at=row[6])


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
        return cls(id=row[0], name=row[1], description=row[2],
                   icon=row[3], category=row[4],
                   deadline=row[5], created_at=row[6])


@dataclass
class Milestone:
    id: int
    goal_id: int
    name: str
    done: bool
    sort_order: int = 0

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], goal_id=row[1], name=row[2],
                   done=bool(row[3]), sort_order=row[4])


@dataclass
class Task:
    id: int
    name: str
    description: str
    category: str
    priority: str
    due_date: Optional[str]
    due_time: Optional[str]
    done: bool
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], name=row[1], description=row[2],
                   category=row[3], priority=row[4],
                   due_date=row[5], due_time=row[6],
                   done=bool(row[7]), created_at=row[8])


@dataclass
class TimeSession:
    id: int
    name: str
    category: str
    duration: int
    session_date: str
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], name=row[1], category=row[2],
                   duration=row[3], session_date=row[4], created_at=row[5])

    @property
    def duration_str(self):
        h = self.duration // 3600
        m = (self.duration % 3600) // 60
        return f"{h}h {m}m" if h else f"{m}m"