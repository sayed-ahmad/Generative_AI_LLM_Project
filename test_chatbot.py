import unittest

from chatbot import InterviewPrepChatbot


class InterviewPrepChatbotTests(unittest.TestCase):
    def setUp(self):
        self.bot = InterviewPrepChatbot()

    def test_question_command_supports_difficulty_without_topic(self):
        response = self.bot.respond("question advanced")
        self.assertTrue(response.startswith("["))
        self.assertIn("• Advanced]", response)

    def test_invalid_difficulty_returns_clear_error(self):
        response = self.bot.respond("question sql hard")
        self.assertIn("Please choose a valid difficulty", response)
        self.assertIn("hard", response)

    def test_question_command_with_topic_and_difficulty(self):
        response = self.bot.respond("question sql advanced")
        self.assertIn("[SQL • Advanced]", response)
        self.assertIn("?", response)


if __name__ == "__main__":
    unittest.main()
