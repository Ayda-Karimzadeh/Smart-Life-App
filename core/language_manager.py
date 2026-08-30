"""
language_manager.py
─────────────────────────────────────────────────────────────
Manages language selection and persistence
"""
from __future__ import annotations

from typing import Callable, Optional

try:
    from PyQt6.QtCore import QObject, pyqtSignal
except ImportError:
    class QObject:
        pass

    class _FallbackSignal:
        def connect(self, callback):
            pass

        def emit(self, value):
            pass

    def pyqtSignal(*args):
        return _FallbackSignal()

from core.translations import t


class LanguageManager(QObject):
    """Manages application language settings."""

    language_changed = pyqtSignal(str)

    SUPPORTED_LANGUAGES = {
        "en": "English",
        "fa": "فارسی",
    }

    def __init__(
        self,
        language_getter: Optional[Callable[[str, str], str]] = None,
        language_setter: Optional[Callable[[str, str], None]] = None,
    ):
        super().__init__()
        self._language_getter = language_getter or self._default_getter
        self._language_setter = language_setter or self._default_setter
        self._current_language = "en"
        self._load_language()

    @staticmethod
    def _default_getter(key: str, default: str = "en") -> str:
        try:
            from database.db_manager import get_setting

            return get_setting(key, default)
        except Exception:
            return default

    @staticmethod
    def _default_setter(key: str, value: str) -> None:
        try:
            from database.db_manager import set_setting

            set_setting(key, value)
        except Exception:
            pass

    def _load_language(self):
        """Load language from persistent settings with safe fallback."""
        try:
            saved_lang = self._language_getter("language", "en")
        except Exception:
            saved_lang = "en"

        if saved_lang in self.SUPPORTED_LANGUAGES:
            self._current_language = saved_lang
        else:
            self._current_language = "en"

    def get_current_language(self) -> str:
        """Get current language code."""
        return self._current_language

    def set_language(self, lang_code: str) -> bool:
        """Set language and save to storage if available."""
        if lang_code not in self.SUPPORTED_LANGUAGES:
            return False

        self._current_language = lang_code
        try:
            self._language_setter("language", lang_code)
        except Exception:
            pass

        self.language_changed.emit(lang_code)
        return True

    def translate(self, key: str) -> str:
        """Get translation for a key in the current language."""
        return t(key, self._current_language)

    def get_supported_languages(self) -> dict:
        """Get dictionary of supported languages."""
        return self.SUPPORTED_LANGUAGES.copy()


# Global instance
_language_manager: Optional[LanguageManager] = None


def get_language_manager() -> LanguageManager:
    """Get the global language manager instance."""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager


def reset_language_manager() -> None:
    """Reset singleton for tests and controlled reinitialization."""
    global _language_manager
    _language_manager = None


def tr(key: str) -> str:
    """Convenience function to translate using the global manager."""
    return get_language_manager().translate(key)
