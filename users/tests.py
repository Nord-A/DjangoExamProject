from django.test import TestCase
from .forms import UserRegisterForm
from django.test import Client


# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# class SetupClass(TestCase):
#
#     def setUp(self):
#         self.user = UserRegisterForm.objects.create(username = "Nilas", email = "nil@as.dk", password1 = "asdqwe33",
#                                                     password2 = "asdqwe33")


#test_forms
class UserRegister_Form_Test(TestCase):
    def test_userregisterform_valid(self):
        form = UserRegisterForm(data={'username':"Nilas", 'email':"nil@as.dk", 'password1':"asdqwe33",'password2':"asdqwe33"})
        self.assertTrue(form.is_valid())

    def test_userregisterform_invalid(self):
        form = UserRegisterForm(data={'username':"asdfg", 'email':"nilas.com", 'password1':"asdqwe33",'password2':"asdqwe33"})
        self.assertFalse(form.is_valid())


#test_views
class Test_Reponse_Codes(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_response_code(self):
        response = self.client.get('/login/') #reverse('blog_index')
        self.assertEquals(response.status_code, 200)

    def test_register_response_code(self):
        response = self.client.get('/register/')
        self.assertEquals(response.status_code, 200)