from django.core.management.base import BaseCommand, CommandError
from server.models import ExcludeFromCache
import server.conversation as conversation
import tensorflow_hub as hub

GENERIC_QUESTIONS = [
    "Can you explain that further?",
    "Could you elaborate on this point?",
    "Please provide more details on [topic/issue].",
    "I'm not sure I understand, could you clarify?",
    "What do you mean by [term/phrase]?",
    "How does this concept relate to [related topic]?",
    "Can you give an example to illustrate this?",
    "In what context does this statement apply?",
    "What are the implications of [action/decision]?",
    "How does this impact [relevant subject]?",
    "What is the rationale behind this approach?",
    "Could you provide some background information?",
    "What are the key factors influencing this situation?",
    "How does this align with [goal/objective]?",
    "What are the potential advantages and disadvantages?",
    "How does this compare to [alternative option]?",
    "Are there any specific limitations to consider?",
    "Can you walk me through the process of [task/activity]?",
    "How does this fit into the broader picture of [topic]?",
    "What are the potential outcomes of [action/strategy]?",
]


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def handle(self, *args, **options):
        for question in GENERIC_QUESTIONS:
            embedding = conversation.generate_embedding(self.embedding_model, question)
            ExcludeFromCache.objects.create(text=question, embedding=embedding)
        self.stdout.write(
            self.style.SUCCESS("Successfully populated db with generic questions")
        )
