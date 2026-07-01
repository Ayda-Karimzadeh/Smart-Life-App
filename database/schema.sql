CREATE TABLE IF NOT EXISTS habits (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    icon            TEXT DEFAULT '⭐',
    category        TEXT DEFAULT 'Personal',
    frequency_type  TEXT DEFAULT 'daily',
    frequency_count INTEGER DEFAULT 7,
    created_at      TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS habit_logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id    INTEGER NOT NULL,
    log_date    TEXT NOT NULL,
    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
    UNIQUE (habit_id, log_date)
);

CREATE TABLE IF NOT EXISTS goals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT DEFAULT '',
    icon        TEXT DEFAULT '🎯',
    category    TEXT DEFAULT 'Personal',
    deadline    TEXT,
    created_at  TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS milestones (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id     INTEGER NOT NULL,
    name        TEXT NOT NULL,
    done        INTEGER DEFAULT 0,
    sort_order  INTEGER DEFAULT 0,
    FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT DEFAULT '',
    category    TEXT DEFAULT 'Personal',
    priority    TEXT DEFAULT 'Medium',
    due_date    TEXT,
    due_time    TEXT,
    done        INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS time_sessions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    category     TEXT DEFAULT 'Other',
    duration     INTEGER NOT NULL,
    session_date TEXT DEFAULT (date('now')),
    created_at   TEXT DEFAULT (datetime('now'))
);