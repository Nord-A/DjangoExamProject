from django.test import TestCase
from .forms import UserRegisterForm


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

class UserRegister_Form_Test(TestCase):
    def test_userregisterform_valid(self):
        form = UserRegisterForm(data={'username':"Nilas", 'email':"nil@as.dk", 'password1':"asdqwe33",'password2':"asdqwe33"})
        self.assertTrue(form.is_valid())


    def test_userregisterform_invalid(self):
        form = UserRegisterForm(data={'username':"asdfg", 'email':"nilas.com", 'password1':"asdqwe33",'password2':"asdqwe33"})
        self.assertFalse(form.is_valid())
