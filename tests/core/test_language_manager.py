import unittest

from core.language_manager import LanguageManager, reset_language_manager


class LanguageManagerTests(unittest.TestCase):
    def setUp(self):
        reset_language_manager()

    def test_loads_default_language_when_storage_is_unavailable(self):
        def getter(key, default="en"):
            raise RuntimeError("DB is not ready")

        manager = LanguageManager(language_getter=getter, language_setter=lambda *args, **kwargs: None)
        self.assertEqual(manager.get_current_language(), "en")

    def test_set_language_uses_injected_storage(self):
        calls = []

        def getter(key, default="en"):
            return "fa" if key == "language" else default

        def setter(key, value):
            calls.append((key, value))

        manager = LanguageManager(language_getter=getter, language_setter=setter)
        self.assertTrue(manager.set_language("en"))
        self.assertEqual(manager.get_current_language(), "en")
        self.assertEqual(calls, [("language", "en")])

    def test_translate_uses_current_language(self):
        manager = LanguageManager(
            language_getter=lambda key, default="en": "en",
            language_setter=lambda *args, **kwargs: None,
        )

        self.assertTrue(manager.set_language("fa"))
        self.assertEqual(manager.translate("less"), "کمتر")


if __name__ == "__main__":
    unittest.main()
