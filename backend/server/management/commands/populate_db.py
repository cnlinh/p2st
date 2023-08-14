from django.core.management.base import BaseCommand, CommandError
from server.models import ExcludeFromCache, Module, Topic
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
    "What do you think about this?",
    "How does this make you feel?",
    "Why do you say that?",
    "What are your thoughts on the matter?",
    "Can you provide more information?",
    "What are the main points to consider?",
    "What are the key factors involved?",
    "How does this impact others?",
    "What are the potential consequences?",
    "Why is this important?",
    "What would be an ideal solution?",
    "How does this relate to your experience?",
    "What are the possible outcomes?",
    "What are the implications of this?",
    "Can you give a brief summary?",
    "What are the pros and cons?",
    "Why is this a challenging issue?",
    "What are the different perspectives?",
    "How does this align with your values?",
    "What other information is needed?",
    "What is the overall objective?",
    "What are the underlying assumptions?",
    "How would you approach this problem?",
    "What are the key takeaways?",
    "Can you provide an example?",
]

MODULES = [
    {
        "code": "CS3243",
        "name": "Introduction to Artificial Intelligence",
        "topics": [
            "Intro to AI/Agents",
            "Problem-solving via Search",
            "Adversarial Search",
            "Constraint Satisfaction Problems",
            "Logical Agents",
            "Uncertainty and Bayesian Belief Networks",
        ],
    }
]


class Command(BaseCommand):
    help = "Populates the database"
    embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def handle(self, *args, **options):
        self.insert_generic_questions()
        self.insert_modules_and_topics()

    def insert_generic_questions(self):
        for question in GENERIC_QUESTIONS:
            embedding = conversation.generate_embedding(self.embedding_model, question)
            ExcludeFromCache.objects.create(text=question, embedding=embedding)
        self.stdout.write(
            self.style.SUCCESS("Successfully populated db with generic questions")
        )

    def insert_modules_and_topics(self):
        for m in MODULES:
            module = Module.objects.create(code=m["code"], name=m["name"])
            for topic in m["topics"]:
                Topic.objects.create(name=topic, module=module)
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully populated db with module {}".format(m["code"])
                )
            )
