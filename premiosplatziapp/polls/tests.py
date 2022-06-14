from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def setUp(self):
        self.question = Question(question_text="¿Quien es el mejor Course Director de Platzi")

    def test_was_published_recently_with_past_questions(self):
        """
        was_published_recently returns False for questions whose pub_date is in the past
        """

        time = timezone.now() - timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        """
        was_published_recently returns True for questions whose pub_date is within the first 24 hours of publication
        """

        time = timezone.now()
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently returns False for questions whose pub_date is in the future
        """

        time = timezone.now() + timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)