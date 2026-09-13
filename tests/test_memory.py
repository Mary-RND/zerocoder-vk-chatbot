from zerocoder_bot.memory import SessionMemory


class TestSessionMemory:
    def test_append_and_get(self):
        memory = SessionMemory(max_messages=5)
        memory.append(1, "user", "привет")
        memory.append(1, "assistant", "здравствуйте")
        history = memory.get(1)
        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[1]["content"] == "здравствуйте"

    def test_max_messages_eviction(self):
        memory = SessionMemory(max_messages=3)
        for i in range(5):
            memory.append(1, "user", str(i))
        history = memory.get(1)
        assert len(history) == 3
        assert history[0]["content"] == "2"
        assert history[-1]["content"] == "4"

    def test_last_n(self):
        memory = SessionMemory(max_messages=10)
        for i in range(5):
            memory.append(1, "user", str(i))
        last_two = memory.get(1, last_n=2)
        assert [msg["content"] for msg in last_two] == ["3", "4"]

    def test_sessions_are_isolated(self):
        memory = SessionMemory(max_messages=10)
        memory.append(1, "user", "для первого")
        memory.append(2, "user", "для второго")
        assert memory.get(1)[0]["content"] == "для первого"
        assert memory.get(2)[0]["content"] == "для второго"

    def test_clear(self):
        memory = SessionMemory(max_messages=10)
        memory.append(1, "user", "что-то")
        memory.clear(1)
        assert memory.get(1) == []

    def test_len_total(self):
        memory = SessionMemory(max_messages=10)
        memory.append(1, "user", "a")
        memory.append(1, "assistant", "b")
        memory.append(2, "user", "c")
        assert len(memory) == 3