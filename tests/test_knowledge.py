from zerocoder_bot.knowledge import COURSES_INFO, FAQ_INFO, ZEROCODER_INFO


class TestKnowledgeBase:
    def test_zero_coder_info_contains_contacts(self):
        assert "+7 (939) 328-38-12" in ZEROCODER_INFO
        assert "care@zerocoder.ru" in ZEROCODER_INFO
        assert "https://zerocoder.ru/" in ZEROCODER_INFO

    def test_courses_info_contains_programs(self):
        for program in ("ПРОМПТ-ИНЖИНИРИНГ", "ВАЙБ-КОДЕР", "ИИ-КОНСАЛТИНГ"):
            assert program in COURSES_INFO

    def test_courses_info_contains_links(self):
        assert "zerocoder.ru" in COURSES_INFO

    def test_faq_contains_questions(self):
        lowered = FAQ_INFO.lower()
        for question in ("зерокодинг", "стоят курсы", "рассрочка"):
            assert question in lowered
