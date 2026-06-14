CREATE TABLE IF NOT EXISTS habits (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    icon            TEXT DEFAULT '⭐',
    category        TEXT DEFAULT 'Personal',
    frequency_type  TEXT DEFAULT 'daily',     -- 'daily' یا 'weekly'
    frequency_count INTEGER DEFAULT 7,        -- چند بار در هفته (daily=7)
    created_at      TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS habit_logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id    INTEGER NOT NULL,
    log_date    TEXT NOT NULL,                -- تاریخ انجام (YYYY-MM-DD)
    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
    UNIQUE (habit_id, log_date)               -- جلوگیری از ثبت تکراری در یک روز
);

CREATE TABLE IF NOT EXISTS goals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT DEFAULT '',
    icon        TEXT DEFAULT '🎯',
    category    TEXT DEFAULT 'Personal',
    deadline    TEXT,                         -- تاریخ مهلت (YYYY-MM-DD)
    created_at  TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS milestones (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id     INTEGER NOT NULL,
    name        TEXT NOT NULL,
    done        INTEGER DEFAULT 0,            -- 0 = نشده, 1 = شده
    sort_order  INTEGER DEFAULT 0,
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT DEFAULT '',
    category    TEXT DEFAULT 'Personal',
    priority    TEXT DEFAULT 'Medium',        -- 'High' / 'Medium' / 'Low'
    due_date    TEXT,                         -- YYYY-MM-DD
    due_time    TEXT,                         -- HH:MM
    done        INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS time_sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    category    TEXT DEFAULT 'Other',         -- Study / Work / Fitness / Personal
    duration    INTEGER NOT NULL,             -- مدت زمان به ثانیه
    session_date TEXT DEFAULT (date('now')),
    created_at  TEXT DEFAULT (datetime('now'))
);