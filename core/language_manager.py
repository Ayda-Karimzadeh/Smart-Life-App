"""
language_manager.py
─────────────────────────────────────────────────────────────
Manages language selection and persistence
"""
from PyQt6.QtCore import QObject, pyqtSignal
from database.db_manager import get_setting, set_setting
from core.translations import t, TRANSLATIONS


class LanguageManager(QObject):
    """Manages application language settings"""

    language_changed = pyqtSignal(str)
    
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "fa": "فارسی"
    }
    
    def __init__(self):
        super().__init__()
        self._current_language = None
        self._load_language()
        
    
    def _load_language(self):
        """Load language from database settings"""
        saved_lang = get_setting("language", "en")
        if saved_lang in self.SUPPORTED_LANGUAGES:
            self._current_language = saved_lang
        else:
            self._current_language = "en"
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self._current_language
    
    def set_language(self, lang_code: str) -> bool:
        """Set language and save to database"""
        if lang_code not in self.SUPPORTED_LANGUAGES:
            return False
        
        self._current_language = lang_code
        set_setting("language", lang_code)

        self.language_changed.emit(lang_code)
        
        return True
    
    def translate(self, key: str) -> str:
        """Get translation for a key in current language"""
        return t(key, self._current_language)
    
    def get_supported_languages(self) -> dict:
        """Get dictionary of supported languages"""
        return self.SUPPORTED_LANGUAGES.copy()


# Global instance
_language_manager = None


def get_language_manager() -> LanguageManager:
    """Get the global language manager instance"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager


def tr(key: str) -> str:
    """Convenience function to translate using global manager"""
    return get_language_manager().translate(key)
