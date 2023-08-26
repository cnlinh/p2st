from django.core.management.base import BaseCommand, CommandError
from server.models import ExcludeFromCache, Module, Topic, Question, Answer, Role
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
            "Introduction to AI; Problem Environments and Intelligence Agents",
            "Uninformed Search",
            "Informed Search",
            "Local Search",
            "Constraint Satisfaction Problems",
            "Adversarial Search",
            "Logical Agents",
            "Bayesian Networks",
            "Project 1.1",
            "Project 1.2",
            "Project 2.1",
            "Project 2.2",
            "Project 3",
        ],
    }
]

DEFAULT_ANSWERS = {
    "CS3243": {
        "Project 1.1": "1. How do you write a depth-first search maze solver in python?\n2. How do you write a uniform-cost search maze solver in python?\n3. How do you optimise a depth-first search maze solver in python?\n4. How do you optimise a uniform-cost search maze solver in python?",
        "Project 1.2": "1. How do you write a breadth-first search maze solver in python?\n2. How do you write an A* maze solver in python?\n3. What are some good heuristics for A* maze solver?\n4. How do you optimise a breadth-first search maze solver in python?\n5. How do you optimise an A* maze solver in python?",
        "Project 2.1": "This project is not released yet. Please check back in week 6!",
        "Project 2.2": "This project is not released yet. Please check back in week 6!",
        "Project 3": "This project is not released yet. Please check back later on in the course!",
    }
}

class Command(BaseCommand):
    help = "Populates the database"
    embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Run all population scripts",
        )

        parser.add_argument(
            "--generic_questions",
            action="store_true",
            help="Populate database with generic questions",
        )

        parser.add_argument(
            "--modules_and_topics",
            action="store_true",
            help="Populate database with modules and topics",
        )

        parser.add_argument(
            "--default_first_answers",
            action="store_true",
            help="Populate database with default first answers",
        )

    def handle(self, *args, **options):
        run_all = False
        if options["all"]:
            run_all = True

        if run_all or options["generic_questions"]:
            self.insert_generic_questions()
        if run_all or options["modules_and_topics"]:
            self.insert_modules_and_topics()
        if run_all or options["default_first_answers"]:
            self.insert_default_first_answers()

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

    def insert_default_first_answers(self):
        for module_code, topics in DEFAULT_ANSWERS.items():
            module = Module.objects.get(code=module_code)
            for topic_name, answer in topics.items():
                topic = Topic.objects.get(name=topic_name, module=module)
                question_text = f"What are good questions to ask when learning about {topic_name}?"
                embedding = conversation.generate_embedding(self.embedding_model, question_text)
                question = Question.objects.create(topic=topic, embedding=embedding, text=question_text, created_by=Role.SYSTEM, difficulty=0.5)
                Answer.objects.create(question=question, text=answer)
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully populated db with default first answers for module {}".format(
                        module_code
                    )
                )
            )
