from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question


def create_question(question_text, days=0):
    """
    Create a Question with the question_text and set the published date with the given days (positive or negative days)
    """
    time = timezone.now() + timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_past_questions(self):
        """
        was_published_recently returns False for questions whose pub_date is in the past
        """

        question = create_question("Past Question", days=-30)
        self.assertFalse(question.was_published_recently())

    def test_was_published_recently_with_present_questions(self):
        """
        was_published_recently returns True for questions whose pub_date is within the first 24 hours of publication
        """

        question = create_question("Present Question")
        self.assertTrue(question.was_published_recently())

    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently returns False for questions whose pub_date is in the future
        """

        question = create_question("Future Question", days=30)
        self.assertFalse(question.was_published_recently())


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no question exist, an appropiate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_questions_of_the_future_dont_show(self):
        """
        If a question for the future exist, it is not displayed
        """
        question = create_question("Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Question with a pub_date in the past is displayed on the index page
        """
        question = create_question("Past Question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed
        """
        past_question = create_question("Past Question", days=-30)
        future_question = create_question("Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        past_question1 = create_question("Past Question 1", days=-20)
        past_question2 = create_question("Past Question 2", days=-100)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question1, past_question2])

    def test_two_future_questions(self):
        """
        The questions index page does not display multiple questions in the future
        """
        future_question1 = create_question("Future Question 1", days=40)
        future_question2 = create_question("Future Question 2", days=100)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_two_future_and_two_past_questions(self):
        """
        The questions index page may display multiple past questions, but no questions in the future
        """
        future_question1 = create_question("Future Question 1", days=40)
        future_question2 = create_question("Future Question 2", days=100)
        past_question1 = create_question("Past Question 1", days=-20)
        past_question2 = create_question("Past Question 2", days=-100)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question1, past_question2])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 error not found
        """
        future_question = create_question("Future Question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past display the question's text
        """
        past_question = create_question("Past Question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)