from django.test import TestCase
from .models import ForumThread, Topic
from django.contrib.auth.models import User
from .forms import ThreadForm
from django.http import request
from django.test import Client
# from django.core.urlresolvers import reverse

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


# class CreateThreadTest(TestCase):
    # def setUp(self):
    #     self.http_request = request.HttpRequest.POST
    #     self.http_request.method = 'POST'
    #     self.http_request.path = '/createthread'
    #     # self.http_request.content_params = {'topic':}  # Init as dictionary?
    #     self.http_request.content_type = ThreadForm
    #     self.http_request.
    #     #How to set request.user?
    #
    # def test_create_thread(self):
    #     pass


class Test_Reponse_Codes(TestCase):
    def setUp(self):
        self.client = Client()
        topic = Topic.objects.create(name="Django")
        owner = User.objects.create(username="TestUser", email="test@test.com", password="test123_ok")
        new_thread = ForumThread.objects.create(topic=topic, title="ThreadTest",
                                                owner=owner, question="How to make tests in Django?")
        # topic.save()
        # owner.save()
        new_thread.save()  # Save ForumThread to DB
        new_thread2 = ForumThread.objects.get(title="ThreadTest") #Get ForumThread from DB
        self.thread_id = new_thread2.id  # Save id in variable to use in tests

    def test_index_response_code(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)  # 200 success

    # User is not logged in and therefore redirected
    def test_create_thread_response_code(self):
        response = self.client.get('/createthread/') #reverse('blog_index')
        self.assertEquals(response.status_code, 302)  # 302 used in redirect

    # User is not logged in and therefore redirected
    def test_edit_thread_response_code(self):
        response = self.client.get('/editthread/' + str(self.thread_id))
        self.assertEquals(response.status_code, 302)  # 302 used in redirect

    def test_view_thread_response_code(self):
        response = self.client.get('/thread/' + str(self.thread_id))
        self.assertEquals(response.status_code, 200)  # 200 success

    def test_view_all_threads_response_code(self):
        response = self.client.get('/allthreads/')
        self.assertEquals(response.status_code, 200)  # 200 success

    # User is not logged in and therefore redirected
    def test_view_own_threads_response_code(self):
        response = self.client.get('/viewownthreads/')
        self.assertEquals(response.status_code, 302)  # 302 used in redirect

#test_forms
# class Setup_Class(TestCase):
#
#     def setUp(self):
#         self.forum_thread = ThreadForm.objects.create(topic="Djangooooooooo", title="ThreadTest",
#                                                       question="How to make tests in Django?")


# class Thread_Form_Test(TestCase):
#
#     def setUp(self):
#         self.userid = 1
#         self.forum_thread = ForumThread.objects.create(topic=topic, owner_id=self.userid, title="ThreadTest",
#                                                        question="How to make tests in Django?")
#         # topic = Topic.objects.create(name="Django")
#         # self.initialform = ThreadForm(data={'topic': topic.id, 'title': "ThreadTest", 'question': "How to make tests in Django?"})
#
#
#     def test_ThreadForm_valid(self):
#         topic = Topic.objects.create(name="Django")
#         form = ThreadForm(data={'topic': topic.id, 'title': "ThreadTest", 'question': "How to make tests in Django?"})
#         new_thread = form.save(commit=False)
#         new_thread.owner_id = self.userid
#         self.assertTrue(form == self.forum_thread)  # Expects form.is_valid() to be True


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