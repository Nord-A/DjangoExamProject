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
# class Setup_Class(TestCase):
#
#     def setUp(self):
#         self.forum_thread = ThreadForm.objects.create(topic="Djangooooooooo", title="ThreadTest",
#                                                       question="How to make tests in Django?")


class Thread_Form_Test(TestCase):

    def setUp(self):
        self.forum_thread = ForumThread.objects.create(topic="Djangooooooooo", title="ThreadTest",
                                                              question="How to make tests in Django?")
        # topic = Topic.objects.create(name="Django")
        # self.initialform = ThreadForm(data={'topic': topic.id, 'title': "ThreadTest", 'question': "How to make tests in Django?"})

    def test_ThreadForm_valid(self):
        topic = Topic.objects.create(name="Django")
        form = ThreadForm(data={'topic': topic.id, 'title': "ThreadTest", 'question': "How to make tests in Django?"})

        self.assertTrue(form.is_valid() )  # Expects form.is_valid() to be True


# class TestBasic2(unittest.TestCase):
#     "Show setup and teardown"
#
#     def setUp(self):
#         self.a = 1
#
#     def tearDown(self):
#         del self.a
#
#     def test_basic1(self):
#         "Basic with setup"
#
#         self.assertNotEqual(self.a, 2)
#
#     def test_basic2(self):
#         "Basic2 with setup"
#         assert self.a != 2
#
#     def test_fail(self):
#         "This test should fail"
#         assert self.a == 2