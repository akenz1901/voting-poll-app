import datetime
from django.test import TestCase
from django.urls import reverse
from .models import Question
from django.utils import timezone


class QuestionModeTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Question(published_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(published_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_time = Question(published_date=time)
        self.assertIs(recent_time.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, published_date=time)


class QuestionIndexViewTests(TestCase):
    """
    We created a question function that  helps take the repetition out of the process of creating
    test_no_questions doesn’t create any questions, but checks the message: “No polls are available.” and verifies
    the latest_question_list is empty.

    We created question for past question and future question using the create_question function
    The database is reset for each test method, so the first question is no longer there, and so again the index shouldn’t have any questions in it.

    The database is reset for each test method, so the first question is no longer there, and so again the index shouldn’t have any questions in it.
    """
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):

        question = create_question(question_text="Past Question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question],)

    def test_future_question(self):
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):

        question = create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question], )

    def test_two_past_question(self):
        question1 = create_question(question_text="Past question 1", days=-30)
        question2 = create_question(question_text="Past question 2", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1],)

    class QuestionDetailViewTests(TestCase):
        def test_future_question(self):
            future_question = create_question(question_text="Future question", days=5)
            url = reverse("polls:details", args=(future_question.id,))
            response = self.client.get(url)
            self.asserEqual(response.status_code, 404)

        def test_past_question(self):
            past_question = create_question(question_text="Past Question", days=-30)
            url = reverse('polls:details', args=(past_question.id, ))
            response = self.client.get(url)
            self.assertContains(response, past_question.question_text)
