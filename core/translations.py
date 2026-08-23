"""
translations.py
─────────────────────────────────────────────────────────────
Translation system for bilingual support (English / Persian)
"""

TRANSLATIONS = {
    # =====================================================================
    # English
    # =====================================================================
    "en": {

        # =========================================================
        # App
        # =========================================================
        "app_name": "Smart Life Dashboard",
        "app_short_name": "Smart Life",
        "loading": "Loading your data...",
        "initializing_db": "Initializing database...",
        "starting_app": "Starting app...",

        # =========================================================
        # Sidebar
        # =========================================================
        "dashboard": "Dashboard",
        "habits": "Habits",
        "goals": "Goals",
        "tasks": "Tasks",
        "time_tracking": "Time Tracking",
        "analytics": "Analytics",
        "settings": "Settings",

        # =========================================================
        # Header / Common
        # =========================================================
        "streak": "Streak",
        "days": "days",
        "score": "Score",
        "week": "Week",

        "add": "Add",
        "edit": "Edit",
        "delete": "Delete",
        "cancel": "Cancel",
        "save": "Save",
        "save_changes": "Save Changes",
        "confirm": "Confirm",
        "close": "Close",

        "name": "Name",
        "description": "Description",
        "category": "Category",
        "icon": "Icon",
        "deadline": "Deadline",
        "priority": "Priority",
        "due_date": "Due Date",
        "due_time": "Due Time",

        # =========================================================
        # Habits
        # =========================================================
        "add_habit": "Add New Habit",
        "edit_habit": "Edit Habit",
        "delete_habit": "Delete Habit",
        "delete_habit_confirm":
            "Are you sure you want to delete '{name}'?",

        "habit_name": "Habit Name",
        "frequency": "Frequency",
        "times_per_week": "Times / week",
        "daily": "Daily",
        "weekly": "Weekly",
        "add_habit_btn": "Add Habit",

        "habit_completed": "Nice work!",
        "habit_completed_desc": "\"{name}\" is done for today.",
        "habit_unchecked": "Marked as undone",
        "habit_unchecked_desc": "\"{name}\" is unchecked for today.",

        "streak_milestone_title": "{streak}-Day Streak!",
        "streak_milestone_desc":
            "Amazing — \"{name}\" for {streak} days in a row!",

        # Suggested Habits
        "habit_meditation": "Morning Meditation",
        "habit_exercise": "Exercise",
        "habit_reading": "Reading",
        "habit_water": "Drink 8 Glasses",
        "habit_sleep": "Sleep by 11 PM",
        "habit_skill": "Practice a Skill",
        "habit_journal": "Journaling",
        "habit_walk": "Morning Walk",

        # =========================================================
        # Tasks
        # =========================================================
        "add_task": "Add New Task",
        "edit_task": "Edit Task",
        "delete_task": "Delete Task",
        "delete_task_confirm":
            "Are you sure you want to delete '{name}'?",

        "task_name": "Task Name",
        "add_task_btn": "Add Task",

        "filter_all_tasks": "All Tasks",
        "filter_today": "Today",
        "filter_this_week": "This Week",

        "pending_tasks": "Pending Tasks",
        "completed": "Completed",
        "tasks_pending": "Tasks Pending",
        "to_be_completed": "To be completed",

        "great_progress": "Great progress!",
        "focus_on_these": "Focus on these",
        "needs_attention": "Needs attention",

        # =========================================================
        # Goals
        # =========================================================
        "add_goal": "Add New Goal",
        "edit_goal": "Edit Goal",
        "delete_goal": "Delete Goal",
        "delete_goal_confirm":
            "Are you sure you want to delete '{name}'? "
            "This will also delete its milestones.",

        "goal_name": "Goal Name",
        "add_goal_btn": "Add Goal",
        "add_new_goal": "+ Add New Goal",

        "add_milestone": "Add Milestone",
        "add_milestone_btn": "Add Milestone",

        "milestones": "Milestones",
        "milestones_completed": "{done} of {total} completed",
        "no_milestones": "No milestones yet",

        "goals_in_progress": "In Progress",
        "average_progress": "Average Progress",
        "across_all_goals": "Across all goals",
        "completed_this_year": "This year",
        "progress_rate": "Progress Rate",
        "vs_last_month": "vs last month",

        # =========================================================
        # Time Tracking / Timer
        # =========================================================
        "start_timer": "Start Timer",
        "stop_timer": "Stop Timer",
        "start_focus_session": "Start Focus Session",

        "edit_session": "Edit Session",
        "delete_session": "Delete Session",
        "delete_session_confirm": "Delete '{name}'?",

        "session_name": "Session Name",
        "session_name_placeholder": "e.g. Morning Workout",
        "duration": "Duration",
        "duration_minutes": "Duration",
        "custom_duration": "Custom",
        "reset": "Reset",

        "total_time_today": "Total time today",
        "recent_sessions": "Recent Sessions",

        "hours": "hours",
        "minutes": "minutes",
        "seconds": "seconds",

        "study": "Study",
        "work": "Work",
        "fitness": "Fitness",
        "personal": "Personal",
        "other": "Other",

        "session_complete": "Session Complete!",
        "session_finished": "finished!",

        # =========================================================
        # Dashboard
        # =========================================================
        "welcome_first_time":
            "Welcome! Your habits are ready — check your first ones "
            "to see your progress here.",

        "getting_started": "Getting Started",

        "todays_overview": "Today's Overview",
        "daily_overview": "Today's Overview",
        "daily_score": "Daily Score",
        "weekly_avg": "Weekly Avg",

        "todays_habits": "Today's Habits",
        "todays_tasks": "Today's Tasks",

        "habit_streaks": "Habit Streaks",

        "daily_progress": "Daily Progress",
        "habit_completion_today": "Habit completion today",
        "habits_completed": "Habits Completed",
        "keep_it_up": "Keep it up!",

        "active_goals": "Active Goals",
        "in_progress": "In progress",

        "focus_time": "Focus Time",
        "focus_time_today": "Focus Time Today",
        "focus_hours": "Focus Hours",
        "tracked_sessions": "Tracked sessions",

        "completed_today": "Completed today",
        "not_completed_yet": "Not completed yet",

        "no_tasks_due_today": "No tasks due today",

        "view_all": "View All →",
        "show_less": "Show Less",

        "habits_ready": "habits ready",
        "tap_habit_to_mark_done": "Tap a habit to mark it done",
        "lets_begin": "Let's begin",

        "day_streak": "day streak",
        "level": "Level",
        "achiever": "Achiever",
        "level_achiever": "Level Achiever",

        "good_morning": "Good morning",
        "good_afternoon": "Good afternoon",
        "good_evening": "Good evening",

        "amazing_keep_going":
            "You're doing amazing! Keep pushing forward on your journey to greatness.",

        "every_small_step":
            "Every small step counts. Mark a habit done today to start your streak.",

        "go_to_habits_check_off":
            "Go to Habits and check off what you did today",

        "add_task_or_timer":
            "Add a task or start a focus timer",

        "stats_fill_automatically":
            "Come back here — your stats will fill in automatically",

        # =========================================================
        # Days
        # =========================================================
        "sat": "Sat",
        "sun": "Sun",
        "mon": "Mon",
        "tue": "Tue",
        "wed": "Wed",
        "thu": "Thu",
        "fri": "Fri",

        # =========================================================
        # Analytics
        # =========================================================
        "weekly_activity": "Weekly Activity",
        "time_distribution": "Time Distribution",

        "habit_score": "Habit Score",
        "todays_completion": "Today's completion",

        "goal_progress": "Goal Progress",

        "task_completion": "Task Completion",
        "all_time": "All time",

        "longest_streak": "Longest Streak",
        "days_active": "Days active",
        "best": "Best",

        "focused_today": "Focused Today",
        "vs_yesterday": "+30 min vs yesterday",
        "this_week": "This Week",
        "last_week": "Last Week",

        "across_all_categories": "Across all categories",
        "top_category": "Top Category",
        "most_time_spent": "Most time spent",
        "daily_average": "Daily Average",

        "empty_analytics_title": "Your Progress Awaits",
        "empty_analytics_desc":
            "Start tracking to see your growth patterns and insights.",

        "no_data_available": "No data available",
        "no_data_yet": "No data yet",

        # Trends
        "habit_score_trend": "Habit Score Trend",
        "weekly_focus_time": "Weekly Focus Time",
        "weekly_focus": "Weekly Focus",

        # Radar / Comparison
        "performance_radar": "Performance Radar",
        "focus_weekly_vs_last": "Focus: This Week vs Last Week",

        # Performance Banner
        "outstanding_performance": "Outstanding Performance!",
        "outstanding_performance_desc":
            "You've completed all your habits today. Keep it up!",

        "great_work_today": "Great Work Today!",
        "great_work_today_desc":
            "You've completed {pct}% of your habits today.",

        "good_progress_msg": "Good Progress!",
        "good_progress_desc":
            "Keep going and take it one step at a time.",

        "lets_get_moving": "Let's Get Moving!",
        "lets_get_moving_desc":
            "There's still time to complete some of your habits today.",

        "welcome_analytics": "Welcome to Analytics!",
        "welcome_analytics_desc":
            "Your stats and performance insights will appear here "
            "as you start tracking.",

        # =========================================================
        # Insights
        # =========================================================
        "key_insight": "Key Insight",
        "key_insights": "Key Insights",

        "insight_streak":
            "Your {habit} streak is {streak} days. Keep it going!",

        "insight_goal_almost_done":
            "You're {progress}% through {goal}. You're almost there!",

        "no_insight_yet":
            "Keep using Smart Life and we'll show you something "
            "worth noticing here.",

        "day_streak_insight": "{streak} Day Streak",
        "streak_insight_desc":
            "You've completed \"{name}\" for {streak} days in a row.",

        "goal_almost_done": "Goal Almost Complete",
        "goal_almost_done_desc":
            "\"{name}\" is {pct}% complete.",

        "perfect_day": "Perfect Day",
        "perfect_day_desc":
            "You've completed all your habits today. Amazing!",

        "deep_focus_session": "Deep Focus",
        "deep_focus_desc":
            "You've focused for {hours} hours today.",

        # =========================================================
        # Categories
        # =========================================================
        "all": "All",
        "fitness": "Fitness",
        "health": "Health",
        "mindfulness": "Mindfulness",
        "personal_growth": "Personal Growth",
        "learning": "Learning",
        "finance": "Finance",
        "study": "Study",
        "work": "Work",
        "personal": "Personal",
        "wellness": "Wellness",
        "skills": "Skills",
        "digital_wellness": "Digital Wellness",
        "career": "Career",
        "other": "Other",

        "cat_mindfulness": "Mindfulness",
        "cat_fitness": "Fitness",
        "cat_health": "Health",
        "cat_personal_growth": "Personal Growth",
        "cat_skills": "Skills",
        "cat_digital_wellness": "Digital Wellness",
        "cat_career": "Career",
        "cat_work": "Work",
        "cat_personal": "Personal",
        "cat_learning": "Learning",
        "cat_wellness": "Wellness",
        "cat_finance": "Finance",
        "cat_study": "Study",
        "cat_other": "Other",

        # =========================================================
        # Priorities
        # =========================================================
        "prio_high": "High",
        "prio_medium": "Medium",
        "prio_low": "Low",

        # =========================================================
        # Deadline / Progress
        # =========================================================
        "days_overdue": "days overdue",
        "due_today": "Due today",
        "days_left": "days left",
        "progress": "Progress",

        # =========================================================
        # Empty States
        # =========================================================
        "no_habits_yet":
            "No habits yet — add some in the Habits page",

        "no_habits_add":
            "No habits yet — add some in the Habits page!",

        "no_tasks_today":
            "No tasks due today",

        "no_tasks_add":
            "No tasks yet — add your first task!",

        "no_goals_yet":
            "No goals yet",

        "no_goals_add":
            "No goals yet — add your first goal!",

        "no_sessions_today":
            "No sessions today",

        "empty_habits_title":
            "Start Your Journey",

        "empty_habits_desc":
            "Build consistency with daily habits. Small steps lead to big changes!",

        "empty_goals_title":
            "Set Your Targets",

        "empty_goals_desc":
            "Define what you want to achieve. Break big dreams into milestones.",

        "empty_tasks_title":
            "Stay Organized",

        "empty_tasks_desc":
            "Track your to-dos and priorities. Focus on what matters most.",

        "empty_timer_title":
            "Track Your Focus",

        "empty_timer_desc":
            "Measure your productive time. Every minute counts toward your goals.",

        # =========================================================
        # Placeholders
        # =========================================================
        "ph_habit_name": "e.g. Morning Meditation",
        "ph_task_name": "e.g. Complete project proposal",
        "ph_task_desc": "Short description...",
        "ph_goal_name": "e.g. Learn Full-Stack Web Development",
        "ph_goal_desc": "Short description...",
        "ph_milestone": "e.g. Complete React fundamentals",

        # =========================================================
        # Onboarding
        # =========================================================
        "choose_language": "Choose your language",
        "choose_language_sub":
            "You can change it later from Settings.",

        "welcome": "Welcome to\nSmart Life Dashboard",

        "onboarding_desc":
            "A personal dashboard for managing your habits, goals and time.\n"
            "Let's get started — just 3 steps!",

        "your_name": "What's your name?",
        "name_placeholder": "e.g. Sara",

        "select_habits": "Which habits do you want to start?",
        "select_habits_sub":
            "Select at least one — you can change them later",

        "select_goals": "Do you have a big goal?",
        "select_goals_sub":
            "You can select more than one or skip",

        "ready": "Ready, {name}!",
        "ready_title": "Ready, {name}!",

        "ready_sub":
            "Your habits and goals are saved.\n"
            "One small step each day — big results!",

        "ready_desc":
            "Your habits and goals have been saved.\n"
            "Small steps every day create big results!",

        "back": "← Back",
        "next": "Next →",
        "lets_start": "Let's Start →",
        "lets_go": "Let's Go! 🚀",
        "continue": "Continue →",

        "select_habit_error": "Select a habit",
        "select_habit_error_desc":
            "Select at least one habit to get started.",

        # =========================================================
        # Demo Data
        # =========================================================
        "demo_data_title": "Try Demo Data?",
        "demo_data_desc":
            "Load sample habits, goals, and tasks to see how the app works. "
            "You can clear it anytime from settings.",

        "load_demo": "Load Demo Data",
        "skip_demo": "Start Fresh",

        "demo_data_prompt_desc":
            "Load sample habits, goals, tasks, and time sessions to explore the app.",

        "demo_data_yes_btn": "Yes, load demo data",
        "demo_data_no_btn": "No, start fresh",

        "demo_data_error_title": "Demo Data Error",
        "demo_data_error_desc":
            "Something went wrong while loading demo data.",

        "demo_goal_description": "Work towards: {name}",

        # =========================================================
        # Suggested Goals
        # =========================================================
        "goal_learn_something": "Learn Something New",
        "goal_get_fit": "Get Fit",
        "goal_save_money": "Save Money",
        "goal_read_books": "Read 12 Books",
        "goal_side_project": "Build a Side Project",
        "goal_new_language": "Learn a New Language",

        # =========================================================
        # Suggested Milestones
        # =========================================================
        "ms_choose_topic": "Choose a Topic",
        "ms_beginner_lessons": "Complete Beginner Lessons",
        "ms_practice_consistently": "Practice Consistently",
        "ms_build_small_project": "Build a Small Project",
        "ms_master_basics": "Master the Basics",

        "ms_create_workout_plan": "Create a Workout Plan",
        "ms_complete_first_month": "Complete the First Month",
        "ms_improve_endurance": "Improve Endurance",
        "ms_reach_first_fitness_goal": "Reach Your First Fitness Goal",
        "ms_keep_consistency": "Maintain Consistency",

        "ms_set_saving_target": "Set a Savings Target",
        "ms_save_first_amount": "Save Your First Amount",
        "ms_save_25_percent": "Save 25% of Your Target",
        "ms_save_50_percent": "Save 50% of Your Target",
        "ms_reach_saving_goal": "Reach Your Savings Goal",

        "ms_finish_first_book": "Finish Your First Book",
        "ms_finish_three_books": "Finish 3 Books",
        "ms_finish_six_books": "Finish 6 Books",
        "ms_finish_nine_books": "Finish 9 Books",
        "ms_finish_twelve_books": "Finish 12 Books",

        "ms_choose_project_idea": "Choose a Project Idea",
        "ms_plan_project": "Plan the Project",
        "ms_build_mvp": "Build the MVP",
        "ms_launch_first_version": "Launch the First Version",
        "ms_improve_from_feedback": "Improve Based on Feedback",

        "ms_learn_alphabet": "Learn the Alphabet",
        "ms_learn_500_words": "Learn 500 Words",
        "ms_first_conversation": "Have Your First Conversation",
        "ms_reach_a2": "Reach A2 Level",
        "ms_reach_b1": "Reach B1 Level",

        # =========================================================
        # Settings
        # =========================================================
        "settings_title": "Settings",
        "language": "Language",
        "english": "English",
        "persian": "Persian (فارسی)",

        "theme": "Theme",
        "dark": "Dark",
        "light": "Light",

        "data": "Data",
        "clear_demo": "Clear Demo Data",
        "clear_demo_desc":
            "Remove all sample data added during onboarding",

        # =========================================================
        # Demo Tasks
        # =========================================================
        "task_finish_python_exercise": "Finish Python exercise",
        "task_python_exercise_desc": "Chapter 3 practice problems",

        "task_go_for_run": "Go for a run",
        "task_go_for_run_desc": "30 minutes jogging",

        "task_reply_emails": "Reply to emails",
        "task_reply_emails_desc": "Clear out the inbox",

        "task_book_dentist": "Book dentist appointment",
        "task_book_dentist_desc": "Overdue — call the clinic",

        "task_read_chapter": "Read chapter 5",
        "task_read_chapter_desc": "Continue reading current book",

        "task_grocery_shopping": "Weekly grocery shopping",
        "task_grocery_shopping_desc": "Milk, eggs, vegetables",

        # =========================================================
        # Demo Time Sessions
        # =========================================================
        "session_python_study": "Python Study",
        "session_deep_work": "Deep Work Block",
        "session_evening_run": "Evening Run",
        "session_journaling": "Journaling",
        "session_book_reading": "Book Reading",

        # =========================================================
        # Habit Statistics
        # =========================================================
        "days_count": "{count} days",
        "weeks_count": "{count} weeks",
        "longest": "Longest",
        "across_all_habits": "Across all habits",
        "building_consistency": "Building consistency",
        "at_risk": "At Risk",
        "broken": "Broken",
        "weeks": "weeks",
        "of": "of",
        # =========================================================
        # =========================================================
        # Demo Time Sessions
        # =========================================================
        "session_python_study": "Python Study",
        "session_reading": "Reading",
        "session_deep_work": "Deep Work Block",
        "session_python_project": "Python Project",
        "session_learning": "Learning",
        "session_week_review": "Weekly Review",
        "session_planning": "Planning",
    },

    # =====================================================================
    # Persian
    # =====================================================================
    "fa": {
        # =========================================================
        # Demo Time Sessions
        # =========================================================
        "session_python_study": "مطالعه پایتون",
        "session_reading": "مطالعه",
        "session_deep_work": "کار عمیق",
        "session_python_project": "پروژه پایتون",
        "session_learning": "یادگیری",
        "session_week_review": "مرور هفتگی",
        "session_planning": "برنامه‌ریزی",

        # =========================================================
        # App
        # =========================================================
        "app_name": "داشبورد زندگی هوشمند",
        "app_short_name": "زندگی هوشمند",
        "loading": "در حال بارگذاری داده‌ها...",
        "initializing_db": "راه‌اندازی دیتابیس...",
        "starting_app": "شروع برنامه...",

        # =========================================================
        # Sidebar
        # =========================================================
        "dashboard": "داشبورد",
        "habits": "عادت‌ها",
        "goals": "اهداف",
        "tasks": "تسک‌ها",
        "time_tracking": "پیگیری زمان",
        "analytics": "آمار",
        "settings": "تنظیمات",

        # =========================================================
        # Header / Common
        # =========================================================
        "streak": "روزهای متوالی",
        "days": "روز",
        "score": "امتیاز",
        "week": "هفته",

        "add": "افزودن",
        "edit": "ویرایش",
        "delete": "حذف",
        "cancel": "لغو",
        "save": "ذخیره",
        "save_changes": "ذخیره تغییرات",
        "confirm": "تأیید",
        "close": "بستن",

        "name": "نام",
        "description": "توضیحات",
        "category": "دسته‌بندی",
        "icon": "آیکون",
        "deadline": "مهلت",
        "priority": "اولویت",
        "due_date": "تاریخ سررسید",
        "due_time": "زمان سررسید",

        # =========================================================
        # Habits
        # =========================================================
        "add_habit": "افزودن عادت جدید",
        "edit_habit": "ویرایش عادت",
        "delete_habit": "حذف عادت",
        "delete_habit_confirm":
            "آیا مطمئن هستید که می‌خواهید «{name}» را حذف کنید؟",

        "habit_name": "نام عادت",
        "frequency": "تکرار",
        "times_per_week": "بار در هفته",
        "daily": "روزانه",
        "weekly": "هفتگی",
        "add_habit_btn": "افزودن عادت",

        "habit_completed": "آفرین!",
        "habit_completed_desc":
            "«{name}» برای امروز انجام شد.",
        "habit_unchecked": "انجام‌نشده شد",
        "habit_unchecked_desc":
            "«{name}» برای امروز انجام‌نشده علامت خورد.",

        "streak_milestone_title":
            "{streak} روز تداوم!",
        "streak_milestone_desc":
            "عالیه — «{name}» {streak} روز پشت‌سرهم!",

        # Suggested Habits
        "habit_meditation": "مدیتیشن صبحگاهی",
        "habit_exercise": "ورزش",
        "habit_reading": "مطالعه",
        "habit_water": "نوشیدن ۸ لیوان آب",
        "habit_sleep": "خواب قبل از ۱۱ شب",
        "habit_skill": "تمرین یک مهارت",
        "habit_journal": "نوشتن روزانه",
        "habit_walk": "پیاده‌روی صبحگاهی",

        # =========================================================
        # Tasks
        # =========================================================
        "add_task": "افزودن تسک جدید",
        "edit_task": "ویرایش تسک",
        "delete_task": "حذف تسک",
        "delete_task_confirm":
            "آیا مطمئن هستید که می‌خواهید «{name}» را حذف کنید؟",

        "task_name": "نام تسک",
        "add_task_btn": "افزودن تسک",

        "filter_all_tasks": "همه تسک‌ها",
        "filter_today": "امروز",
        "filter_this_week": "این هفته",

        "pending_tasks": "تسک‌های در انتظار",
        "completed": "تکمیل‌شده",
        "tasks_pending": "تسک‌های در انتظار",
        "to_be_completed": "باید انجام شود",

        "great_progress": "پیشرفت عالی!",
        "focus_on_these": "روی این‌ها تمرکز کن",
        "needs_attention": "نیاز به توجه دارد",

        # =========================================================
        # Goals
        # =========================================================
        "add_goal": "افزودن هدف جدید",
        "edit_goal": "ویرایش هدف",
        "delete_goal": "حذف هدف",
        "delete_goal_confirm":
            "آیا مطمئن هستید که می‌خواهید «{name}» را حذف کنید؟ "
            "تمام مایلستون‌های آن نیز حذف خواهند شد.",

        "goal_name": "نام هدف",
        "add_goal_btn": "افزودن هدف",
        "add_new_goal": "+ افزودن هدف جدید",

        "add_milestone": "افزودن مایلستون",
        "add_milestone_btn": "افزودن مایلستون",

        "milestones": "مایلستون‌ها",
        "milestones_completed": "{done} از {total} انجام شده",
        "no_milestones": "هنوز مایلستونی اضافه نشده",

        "goals_in_progress": "در حال انجام",
        "average_progress": "میانگین پیشرفت",
        "across_all_goals": "بین تمام اهداف",
        "completed_this_year": "امسال",
        "progress_rate": "نرخ پیشرفت",
        "vs_last_month": "نسبت به ماه قبل",

        # =========================================================
        # Time Tracking / Timer
        # =========================================================
        "start_timer": "شروع تایمر",
        "stop_timer": "توقف تایمر",
        "start_focus_session": "شروع جلسه تمرکز",

        "edit_session": "ویرایش جلسه",
        "delete_session": "حذف جلسه",
        "delete_session_confirm":
            "آیا «{name}» حذف شود؟",

        "session_name": "نام جلسه",
        "session_name_placeholder": "مثلاً تمرین صبحگاهی",
        "duration": "مدت زمان",
        "duration_minutes": "مدت زمان",
        "custom_duration": "دلخواه",
        "reset": "بازنشانی",

        "total_time_today": "مجموع زمان امروز",
        "recent_sessions": "جلسات اخیر",

        "hours": "ساعت",
        "minutes": "دقیقه",
        "seconds": "ثانیه",

        "study": "مطالعه",
        "work": "کار",
        "fitness": "ورزش",
        "personal": "شخصی",
        "other": "سایر",

        "session_complete": "جلسه کامل شد!",
        "session_finished": "به پایان رسید!",

        # =========================================================
        # Dashboard
        # =========================================================
        "welcome_first_time":
            "خوش اومدی! عادت‌هات آماده‌ان — اولین‌هاشون رو تیک بزن "
            "تا پیشرفتت اینجا دیده بشه.",

        "getting_started": "شروع کار",

        "todays_overview": "نمای کلی امروز",
        "daily_overview": "نمای کلی امروز",
        "daily_score": "امتیاز روزانه",
        "weekly_avg": "میانگین هفتگی",

        "todays_habits": "عادت‌های امروز",
        "todays_tasks": "تسک‌های امروز",

        "habit_streaks": "تداوم عادت‌ها",

        "daily_progress": "پیشرفت روزانه",
        "habit_completion_today": "تکمیل عادت‌های امروز",
        "habits_completed": "عادت‌های انجام‌شده",
        "keep_it_up": "ادامه بده!",

        "active_goals": "اهداف فعال",
        "in_progress": "در حال انجام",

        "focus_time": "زمان تمرکز",
        "focus_time_today": "زمان تمرکز امروز",
        "focus_hours": "ساعت تمرکز",
        "tracked_sessions": "جلسات ثبت‌شده",

        "completed_today": "امروز انجام شده",
        "not_completed_yet": "هنوز انجام نشده",

        "no_tasks_due_today": "امروز تسکی برای انجام نیست",

        "view_all": "مشاهده همه ←",
        "show_less": "نمایش کمتر",

        "habits_ready": "عادت آماده",
        "tap_habit_to_mark_done":
            "روی یک عادت بزن تا انجام‌شده علامت بخورد",

        "lets_begin": "شروع کنیم",

        "day_streak": "روز تداوم",
        "level": "سطح",
        "achiever": "موفق",
        "level_achiever": "سطح موفقیت",

        "good_morning": "صبح بخیر",
        "good_afternoon": "بعدازظهر بخیر",
        "good_evening": "عصر بخیر",

        "amazing_keep_going":
            "عالی پیش می‌روی! به مسیر رشدت ادامه بده.",

        "every_small_step":
            "هر قدم کوچک مهم است. امروز یک عادت را انجام بده "
            "تا زنجیره‌ات شروع شود.",

        "go_to_habits_check_off":
            "به بخش عادت‌ها برو و کارهایی که امروز انجام دادی را علامت بزن",

        "add_task_or_timer":
            "یک تسک اضافه کن یا تایمر تمرکز را شروع کن",

        "stats_fill_automatically":
            "دوباره به اینجا برگرد — آمار پیشرفتت خودکار تکمیل می‌شود",

        # =========================================================
        # Days
        # =========================================================
        "sat": "شنبه",
        "sun": "یکشنبه",
        "mon": "دوشنبه",
        "tue": "سه‌شنبه",
        "wed": "چهارشنبه",
        "thu": "پنجشنبه",
        "fri": "جمعه",

        # =========================================================
        # Analytics
        # =========================================================
        "weekly_activity": "فعالیت هفتگی",
        "time_distribution": "توزیع زمان",

        "habit_score": "امتیاز عادت‌ها",
        "todays_completion": "تکمیل امروز",

        "goal_progress": "پیشرفت اهداف",

        "task_completion": "تکمیل تسک‌ها",
        "all_time": "از ابتدا",

        "longest_streak": "بیشترین تداوم",
        "days_active": "روزهای فعال",
        "best": "بهترین",

        "focused_today": "تمرکز امروز",
        "vs_yesterday": "+۳۰ دقیقه نسبت به دیروز",
        "this_week": "این هفته",
        "last_week": "هفته قبل",

        "across_all_categories": "در تمام دسته‌بندی‌ها",
        "top_category": "دسته‌بندی برتر",
        "most_time_spent": "بیشترین زمان صرف‌شده",
        "daily_average": "میانگین روزانه",

        "empty_analytics_title": "پیشرفتت در انتظارت است",
        "empty_analytics_desc":
            "شروع به ثبت فعالیت‌ها کن تا الگوهای رشد و بینش‌های عملکردت را ببینی.",

        "no_data_available": "داده‌ای برای نمایش وجود ندارد",
        "no_data_yet": "هنوز داده‌ای وجود ندارد",

        # Trends
        "habit_score_trend": "روند امتیاز عادت‌ها",
        "weekly_focus_time": "زمان تمرکز هفتگی",
        "weekly_focus": "تمرکز هفتگی",

        # Radar / Comparison
        "performance_radar": "رادار عملکرد",
        "focus_weekly_vs_last":
            "مقایسه تمرکز این هفته با هفته قبل",

        # Performance Banner
        "outstanding_performance": "عملکرد فوق‌العاده!",
        "outstanding_performance_desc":
            "امروز تمام عادت‌هایت را انجام داده‌ای. همین‌طور ادامه بده!",

        "great_work_today": "امروز عالی بود!",
        "great_work_today_desc":
            "امروز {pct}% از عادت‌هایت را انجام داده‌ای.",

        "good_progress_msg": "پیشرفت خوبی داری!",
        "good_progress_desc":
            "همین روند را ادامه بده و قدم‌به‌قدم پیش برو.",

        "lets_get_moving": "بیا شروع کنیم!",
        "lets_get_moving_desc":
            "امروز هنوز فرصت داری چند عادت را انجام بدهی.",

        "welcome_analytics": "به بخش تحلیل خوش آمدی!",
        "welcome_analytics_desc":
            "با شروع ثبت فعالیت‌ها، آمار و تحلیل عملکردت اینجا نمایش داده می‌شود.",

        # =========================================================
        # Insights
        # =========================================================
        "key_insight": "بینش کلیدی",
        "key_insights": "نکات مهم",

        "insight_streak":
            "رکورد پیوستگی «{habit}» به {streak} روز رسیده. همین‌طور ادامه بده!",

        "insight_goal_almost_done":
            "هدف «{goal}» رو {progress}% پیش بردی. تقریباً رسیدی!",

        "no_insight_yet":
            "به استفاده از Smart Life ادامه بده تا اینجا یک نکته جالب "
            "درباره پیشرفتت نشون بدیم.",

        "day_streak_insight": "{streak} روز تداوم",

        "streak_insight_desc":
            "عادت «{name}» را {streak} روز متوالی انجام داده‌ای.",

        "goal_almost_done": "هدف نزدیک به پایان",

        "goal_almost_done_desc":
            "هدف «{name}» {pct}% پیشرفت داشته است.",

        "perfect_day": "روز عالی",

        "perfect_day_desc":
            "امروز تمام عادت‌هایت را انجام داده‌ای. فوق‌العاده است!",

        "deep_focus_session": "تمرکز عمیق",

        "deep_focus_desc":
            "امروز {hours} ساعت تمرکز داشته‌ای.",

        # =========================================================
        # Categories
        # =========================================================
        "all": "همه",
        "fitness": "ورزش",
        "health": "سلامت",
        "mindfulness": "ذهن‌آگاهی",
        "personal_growth": "رشد فردی",
        "learning": "یادگیری",
        "finance": "مالی",
        "study": "مطالعه",
        "work": "کار",
        "personal": "شخصی",
        "wellness": "رفاه",
        "skills": "مهارت‌ها",
        "digital_wellness": "سلامت دیجیتال",
        "career": "شغل",
        "other": "سایر",

        "cat_mindfulness": "ذهن‌آگاهی",
        "cat_fitness": "تناسب اندام",
        "cat_health": "سلامتی",
        "cat_personal_growth": "رشد شخصی",
        "cat_skills": "مهارت‌ها",
        "cat_digital_wellness": "سلامت دیجیتال",
        "cat_career": "شغل",
        "cat_work": "کار",
        "cat_personal": "شخصی",
        "cat_learning": "یادگیری",
        "cat_wellness": "رفاه",
        "cat_finance": "مالی",
        "cat_study": "مطالعه",
        "cat_other": "سایر",

        # =========================================================
        # Priorities
        # =========================================================
        "prio_high": "بالا",
        "prio_medium": "متوسط",
        "prio_low": "پایین",

        # =========================================================
        # Deadline / Progress
        # =========================================================
        "days_overdue": "روز تأخیر",
        "due_today": "سررسید امروز",
        "days_left": "روز باقی‌مانده",
        "progress": "پیشرفت",

        # =========================================================
        # Empty States
        # =========================================================
        "no_habits_yet":
            "هنوز عادتی ندارید — در صفحه عادت‌ها اضافه کنید",

        "no_habits_add":
            "هنوز عادتی ندارید — در صفحه عادت‌ها اضافه کنید!",

        "no_tasks_today":
            "امروز تسکی برای انجام نیست",

        "no_tasks_add":
            "هنوز تسکی ندارید — اولین تسک خود را اضافه کنید!",

        "no_goals_yet":
            "هنوز هدفی ندارید",

        "no_goals_add":
            "هنوز هدفی ندارید — اولین هدف خود را اضافه کنید!",

        "no_sessions_today":
            "امروز جلسه‌ای ثبت نشده",

        "empty_habits_title":
            "سفر خود را شروع کنید",

        "empty_habits_desc":
            "با عادت‌های روزانه ثبات بسازید. قدم‌های کوچک منجر به تغییرات بزرگ می‌شوند!",

        "empty_goals_title":
            "اهداف خود را تعیین کنید",

        "empty_goals_desc":
            "آنچه می‌خواهید به آن برسید را تعریف کنید. "
            "رویاهای بزرگ را به مایلستون‌ها تقسیم کنید.",

        "empty_tasks_title":
            "منظم بمانید",

        "empty_tasks_desc":
            "کارها و اولویت‌های خود را پیگیری کنید. روی چیزهای مهم تمرکز کنید.",

        "empty_timer_title":
            "تمرکز خود را پیگیری کنید",

        "empty_timer_desc":
            "زمان مولد خود را اندازه بگیرید. هر دقیقه به سمت اهداف شما می‌شمارد.",

        # =========================================================
        # Placeholders
        # =========================================================
        "ph_habit_name": "مثال: مدیتیشن صبحگاهی",
        "ph_task_name": "مثال: تکمیل پروپوزال پروژه",
        "ph_task_desc": "توضیح کوتاه...",
        "ph_goal_name": "مثال: یادگیری توسعه وب کامل",
        "ph_goal_desc": "توضیح کوتاه...",
        "ph_milestone": "مثال: تکمیل مبانی React",

        # =========================================================
        # Onboarding
        # =========================================================
        "choose_language": "زبان برنامه را انتخاب کنید",
        "choose_language_sub":
            "بعداً می‌توانید از تنظیمات آن را تغییر دهید.",

        "welcome":
            "به داشبورد\nزندگی هوشمند خوش آمدید",

        "onboarding_desc":
            "یه داشبورد شخصی برای مدیریت عادت‌ها، اهداف و وقتت.\n"
            "بذار با هم شروع کنیم — فقط ۳ مرحله‌ست!",

        "your_name": "اسمت چیه؟",
        "name_placeholder": "مثلاً: سارا",

        "select_habits": "چه عادت‌هایی می‌خوای شروع کنی؟",
        "select_habits_sub":
            "حداقل یکی انتخاب کن — بعداً می‌تونی تغییرشون بدی",

        "select_goals": "یه هدف بزرگ داری؟",
        "select_goals_sub":
            "می‌تونی بیشتر از یکی انتخاب کنی یا رد کنی",

        "ready": "آماده‌ای، {name}!",
        "ready_title": "آماده‌ای، {name}!",

        "ready_sub":
            "عادت‌ها و اهدافت ذخیره شدن.\n"
            "هر روز یه قدم کوچیک — نتایج بزرگ می‌سازه!",

        "ready_desc":
            "عادت‌ها و اهدافت ذخیره شدن.\n"
            "هر روز یه قدم کوچیک، نتایج بزرگ می‌سازه!",

        "back": "← برگشت",
        "next": "بعدی →",
        "lets_start": "شروع کنیم →",
        "lets_go": "بزن بریم! 🚀",
        "continue": "ادامه →",

        "select_habit_error": "یک عادت انتخاب کن",
        "select_habit_error_desc":
            "حداقل یک عادت انتخاب کن تا شروع کنی.",

        # =========================================================
        # Demo Data
        # =========================================================
        "demo_data_title": "داده نمونه رو امتحان کنی؟",

        "demo_data_desc":
            "نمونه عادت‌ها، اهداف و تسک‌ها رو بار کن تا ببینی "
            "برنامه چطور کار می‌کنه. هر وقت از تنظیمات می‌تونی پاکشون کنی.",

        "load_demo": "بارگذاری داده نمونه",
        "skip_demo": "شروع تازه",

        "demo_data_prompt_desc":
            "داده‌های نمونه شامل عادت‌ها، اهداف، تسک‌ها و جلسات زمانی را بارگذاری کن تا با برنامه آشنا شوی.",

        "demo_data_yes_btn": "بله، داده نمونه را بارگذاری کن",
        "demo_data_no_btn": "نه، از صفر شروع کن",

        "demo_data_error_title": "خطا در داده نمونه",
        "demo_data_error_desc":
            "هنگام بارگذاری داده‌های نمونه مشکلی پیش آمد.",

        "demo_goal_description":
            "برای رسیدن به «{name}» تلاش کن.",

        # =========================================================
        # Suggested Goals
        # =========================================================
        "goal_learn_something": "یادگیری یک مهارت جدید",
        "goal_get_fit": "تناسب اندام",
        "goal_save_money": "پس‌انداز پول",
        "goal_read_books": "خواندن ۱۲ کتاب",
        "goal_side_project": "ساخت یک پروژه شخصی",
        "goal_new_language": "یادگیری زبان جدید",

        # =========================================================
        # Suggested Milestones
        # =========================================================
        "ms_choose_topic": "انتخاب موضوع",
        "ms_beginner_lessons": "تکمیل درس‌های مقدماتی",
        "ms_practice_consistently": "تمرین منظم",
        "ms_build_small_project": "ساخت یک پروژه کوچک",
        "ms_master_basics": "تسلط بر مبانی",

        "ms_create_workout_plan": "ساخت برنامه تمرینی",
        "ms_complete_first_month": "تکمیل ماه اول",
        "ms_improve_endurance": "بهبود استقامت",
        "ms_reach_first_fitness_goal":
            "رسیدن به اولین هدف تناسب اندام",
        "ms_keep_consistency": "حفظ استمرار",

        "ms_set_saving_target": "تعیین هدف پس‌انداز",
        "ms_save_first_amount": "اولین مبلغ را پس‌انداز کن",
        "ms_save_25_percent": "پس‌انداز ۲۵٪ از هدف",
        "ms_save_50_percent": "پس‌انداز ۵۰٪ از هدف",
        "ms_reach_saving_goal": "رسیدن به هدف پس‌انداز",

        "ms_finish_first_book": "خواندن اولین کتاب",
        "ms_finish_three_books": "خواندن ۳ کتاب",
        "ms_finish_six_books": "خواندن ۶ کتاب",
        "ms_finish_nine_books": "خواندن ۹ کتاب",
        "ms_finish_twelve_books": "خواندن ۱۲ کتاب",

        "ms_choose_project_idea": "انتخاب ایده پروژه",
        "ms_plan_project": "برنامه‌ریزی پروژه",
        "ms_build_mvp": "ساخت MVP",
        "ms_launch_first_version": "انتشار نسخه اول",
        "ms_improve_from_feedback":
            "بهبود بر اساس بازخورد",

        "ms_learn_alphabet": "یادگیری الفبا",
        "ms_learn_500_words": "یادگیری ۵۰۰ کلمه",
        "ms_first_conversation": "اولین مکالمه",
        "ms_reach_a2": "رسیدن به سطح A2",
        "ms_reach_b1": "رسیدن به سطح B1",

        # =========================================================
        # Settings
        # =========================================================
        "settings_title": "تنظیمات",
        "language": "زبان",
        "english": "English",
        "persian": "فارسی",

        "theme": "تم",
        "dark": "تاریک",
        "light": "روشن",

        "data": "داده‌ها",
        "clear_demo": "پاک کردن داده نمونه",
        "clear_demo_desc":
            "حذف تمام داده‌های نمونه اضافه شده در شروع",

        # =========================================================
        # Demo Tasks
        # =========================================================
        "task_finish_python_exercise": "تکمیل تمرین پایتون",
        "task_python_exercise_desc": "تمرین‌های فصل سوم",

        "task_go_for_run": "رفتن برای دویدن",
        "task_go_for_run_desc": "۳۰ دقیقه دویدن",

        "task_reply_emails": "پاسخ به ایمیل‌ها",
        "task_reply_emails_desc": "پاک‌سازی صندوق ایمیل",

        "task_book_dentist": "گرفتن وقت دندانپزشکی",
        "task_book_dentist_desc":
            "عقب‌افتاده — با کلینیک تماس بگیر",

        "task_read_chapter": "خواندن فصل پنجم",
        "task_read_chapter_desc":
            "ادامه مطالعه کتاب فعلی",

        "task_grocery_shopping": "خرید هفتگی",
        "task_grocery_shopping_desc":
            "شیر، تخم‌مرغ و سبزیجات",

        # =========================================================
        # Demo Time Sessions
        # =========================================================
        "session_python_study": "مطالعه پایتون",
        "session_deep_work": "بلوک کار عمیق",
        "session_evening_run": "دویدن عصرگاهی",
        "session_journaling": "نوشتن روزانه",
        "session_book_reading": "مطالعه کتاب",

        # =========================================================
        # Habit Statistics
        # =========================================================
        "days_count": "{count} روز",
        "weeks_count": "{count} هفته",
        "longest": "طولانی‌ترین",
        "across_all_habits": "در تمام عادت‌ها",
        "building_consistency": "در حال ساختن استمرار",
        "at_risk": "در معرض خطر",
        "broken": "قطع شده",
        "weeks": "هفته",
        "of": "از",
    },
}


def t(key: str, lang: str = "en") -> str:
    """
    Get translation for a key in the specified language.

    Falls back to the key itself if the translation does not exist.
    """
    return TRANSLATIONS.get(lang, {}).get(key, key)