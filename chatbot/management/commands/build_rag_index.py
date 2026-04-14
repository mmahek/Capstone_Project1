from django.core.management.base import BaseCommand
from chatbot.ml.rag import retriever

class Command(BaseCommand):
    help = 'Build RAG index from knowledge.json'

    def handle(self, *args, **options):
        print("Building RAG index...")
        retriever.build_index()
        self.stdout.write(
            self.style.SUCCESS('RAG index built successfully!')
        )
