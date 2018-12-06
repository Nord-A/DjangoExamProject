from django.test import TestCase
from .models import ForumThread, Topic
from django.contrib.auth.models import User
from .forms import ThreadForm

# Create your tests here.

#test_views
# class ForumThreadTestCase(TestCase):
#     def setUp(self):
#         topic = Topic.objects.create(name="Django")
#         owner = User.objects.create(username="TestUser", email="test@test.com", password="test123_ok")
#         ForumThread.objects.create(topic=topic, title="ThreadTest", owner=owner, question="How to make tests in Django?")
#
#     def test_create_thread(self):
#
#         new_thread = form.save(commit=False)


#test_forms
class Setup_Class(TestCase):

    def setUp(self):
        
        self.forum_thread = ThreadForm.objects.create(topic="Django", title="ThreadTest",
                                                      question="How to make tests in Django?")


class Thread_Form_Test(TestCase):

    def test_ThreadForm_valid(self):
        topic = Topic.objects.create(name="Django")
        form = ThreadForm(data={'topic': topic.id, 'title': "ThreadTest", 'question': "How to make tests in Django?"})
        self.assertTrue(form.is_valid())  # Expects form.is_valid() to be True