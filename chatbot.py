"""Simple Data Science interview preparation chatbot."""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class LearnerProfile:
    name: str = "Learner"
    target_role: str = "Data Scientist"
    focus_topics: list[str] = field(default_factory=lambda: ["statistics", "machine learning", "SQL"])


class InterviewPrepChatbot:
    """Rule-based interview preparation assistant with an LLM-ready interface."""

    QUESTION_BANK = {
        "statistics": {
            "beginner": ["What is the difference between mean and median?"],
            "intermediate": ["When would you use a t-test instead of a z-test?"],
            "advanced": ["Explain the bias-variance tradeoff and how regularization affects it."],
        },
        "machine learning": {
            "beginner": ["What is overfitting in machine learning?"],
            "intermediate": ["How does cross-validation help with model selection?"],
            "advanced": ["Compare gradient boosting and random forests in terms of bias and variance."],
        },
        "sql": {
            "beginner": ["What is the difference between WHERE and HAVING?"],
            "intermediate": ["How would you find duplicate rows in a table?"],
            "advanced": ["How would you optimize a slow query on a large fact table?"],
        },
    }

    CONCEPT_EXPLANATIONS = {
        "bias-variance tradeoff": (
            "Bias is error from overly simple assumptions; variance is error from sensitivity to training data. "
            "Good models balance both to improve generalization."
        ),
        "overfitting": "Overfitting happens when a model learns training noise and performs poorly on unseen data.",
        "cross-validation": (
            "Cross-validation splits data into folds to estimate model performance more reliably than a single split."
        ),
        "feature engineering": (
            "Feature engineering transforms raw data into informative inputs that improve model learning."
        ),
    }

    def __init__(self, profile: LearnerProfile | None = None) -> None:
        self.profile = profile or LearnerProfile()

    def set_focus_topics(self, topics: list[str]) -> None:
        cleaned = [topic.strip().lower() for topic in topics if topic.strip()]
        if cleaned:
            self.profile.focus_topics = cleaned

    def generate_question(self, topic: str | None = None, difficulty: str = "intermediate") -> str:
        selected_topic = (topic or random.choice(self.profile.focus_topics)).lower()
        topic_bank = self.QUESTION_BANK.get(selected_topic)
        if not topic_bank:
            return f"I don't have interview questions for '{selected_topic}' yet."

        question = random.choice(topic_bank.get(difficulty.lower(), topic_bank["intermediate"]))
        return f"[{selected_topic.title()} • {difficulty.title()}] {question}"

    def explain_concept(self, concept: str) -> str:
        explanation = self.CONCEPT_EXPLANATIONS.get(concept.strip().lower())
        if explanation:
            return explanation
        return (
            "I don't have a prepared explanation for that yet. "
            "Try asking about overfitting, cross-validation, bias-variance tradeoff, or feature engineering."
        )

    def respond(self, user_input: str) -> str:
        text = user_input.strip()
        lowered = text.lower()

        if lowered.startswith("focus:"):
            topics = text.split(":", 1)[1].split(",")
            self.set_focus_topics(topics)
            return f"Updated focus topics: {', '.join(self.profile.focus_topics)}"

        if lowered.startswith("question"):
            parts = text.split()
            topic = parts[1] if len(parts) > 1 else None
            difficulty = parts[2] if len(parts) > 2 else "intermediate"
            return self.generate_question(topic=topic, difficulty=difficulty)

        if lowered.startswith("explain "):
            concept = text.split(" ", 1)[1]
            return self.explain_concept(concept)

        return (
            f"Hi {self.profile.name}! I'm your {self.profile.target_role} interview coach. "
            "Try: 'question', 'question sql advanced', 'explain overfitting', or "
            "'focus: statistics, sql, machine learning'."
        )


def run_cli() -> None:
    bot = InterviewPrepChatbot()
    print("Data Science Interview Prep Chatbot")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bot: Good luck with your interview prep!")
            break
        print(f"Bot: {bot.respond(user_input)}")


if __name__ == "__main__":
    run_cli()
