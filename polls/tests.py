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
    