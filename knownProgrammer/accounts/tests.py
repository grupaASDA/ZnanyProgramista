from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model,authenticate, login

from django.contrib.messages import get_messages
from .models import CustomUser
from .forms import UserUpdateForm


User = get_user_model()
class HomepageViewTest(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'accounts/home_page.html')

# TESTING LOGIN
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_user_successfully(self):
        # USER
        user = User.objects.create_user(first_name='test',last_name='test name', email='test@example.com', password='testpassword')
        user.save()

        # LOGIN
        login_data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.login_url, login_data, follow=True)


        self.assertTrue(response.context['user'].is_authenticated)

        # MESSAGES
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertListEqual(["Logged in succesfully!"], messages)

        # REDIRECT TO HOME PAGE
        self.assertRedirects(response, reverse('homepage'))

    def test_login_user_invalid_credentials(self):
        # LOGIN
        login_data = {'email': 'invalid@example.com', 'password': 'invalidpassword'}
        response = self.client.post(self.login_url, login_data, follow=True)


        self.assertFalse(response.context['user'].is_authenticated)

        # MESSAGES
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Invalid Email or Password!", messages)

        # REDIRECT TO LOGIN PAGE
        self.assertRedirects(response, reverse('login'))

#TESTING LOGOUT

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')

    def test_logout_user(self):
        #USER
        user = User.objects.create_user(first_name='test',last_name='test name', email='test@example.com', password='testpassword')
        user.save()

        # LOGIN
        self.client.login(email='test@example.com', password='testpassword')

        # CHECK LOGIN
        self.assertTrue(self.client.session['_auth_user_id'])

        # LOGOUT
        response = self.client.get(self.logout_url)

        # REDIRECT HOMEPAGE
        self.assertRedirects(response, reverse('homepage'))

        # CHECK LOGOUT
        self.assertFalse(self.client.session.get('_auth_user_id', None))


# REGISTER TEST

class RegisterUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_get_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register_user.html')

    def test_register_user_successfully(self):

        post_data = {
            'first_name': 'test',
            'last_name': 'test name',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        # POST
        response = self.client.post(self.register_url, post_data, follow=True)

        # REDIRECT
        self.assertRedirects(response, reverse('homepage'))

        # CHECK CREATED
        self.assertTrue(User.objects.filter(first_name='test',last_name='test name', email='test@example.com', is_active=False).exists())

        # CHECK MESSAGES
        messages = [m.message for m in response.context['messages']]
        self.assertListEqual(['Dear test, please go to your email test@example.com inbox and click on received activation link to confirm and complete te registration. Check your spam folder.'], messages)


    def test_register_user_invalid_data(self):
        # INVALID DATA
        post_data = {
            'first_name': 'test',
            'last_name': '',
            'email': 'testexample.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        # POST INVALID DATA
        response = self.client.post(self.register_url, post_data, follow=True)

        # CHECK MESSAGES
        messages = [m.message for m in response.context['messages']]
        self.assertListEqual(['Registration failed'], messages)

        # CHECK REDIRECT TO REGISTER
        self.assertTemplateUsed(response, 'accounts/register_user.html')

#PASSWORD CHANGED VIEW TEST

class PasswordChangedViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password_changed_url = reverse('password_changed')

    def test_password_changed_page(self):
        response = self.client.get(self.password_changed_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/changed_password.html')


#UPDATE USER INFO TEST


class UserUpdateFormViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(first_name='testuser',last_name='test', email='test@example.com', password='testpassword')

        self.user_update_url = reverse('update_user', args=[self.user.id])

    def test_get_user_update_form(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(self.user_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_update_form.html')

    def test_get_user_update_form_permission_denied(self):
        self.client.login(email='test@example.com', password='testpassword')
        another_user = User.objects.create_user(first_name='oooo', last_name='test', email='another@example.com',
                                                password='testpassword')
        id_user_to_update = another_user.id
        update_user_profile_url = reverse('update_user', kwargs={'id': id_user_to_update})
        response = self.client.get(update_user_profile_url)
        self.assertEqual(response.status_code, 403)
    def test_post_user_update_form_witchout_email_update(self):

        self.client.login(email='test@example.com', password='testpassword')

        post_data = {
            'first_name': 'updatedusername',
            'last_name': 'updatedlastname',
            'email': 'test@example.com',

        }

        response = self.client.post(self.user_update_url, post_data, follow=True)

        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'updatedusername')
        self.assertEqual(updated_user.last_name, 'updatedlastname')
        self.assertEqual(updated_user.email, 'test@example.com')

        #MESSAGES
        messages = [m.message for m in response.context['messages']]
        self.assertIn("Data has been changed", messages)
        #REDIRECT TO HOMEPAGE
        self.assertRedirects(response, reverse('homepage'))

# DELATE ACCOUNT TEST
class AccountDeleteConfirmViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(first_name='tast',last_name='user', email='test@example.com', password='testpassword')
        self.account_delete_url = reverse('account_delete_confirm', args=[self.user.id])

    def test_get_account_delete_confirm(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(self.account_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/account_delete_confirm.html')

    def test_get_account_delete_confirm_permission_denied(self):
        self.client.login(email='test@example.com', password='testpassword')
        another_user = User.objects.create_user(first_name='oooo',last_name='test', email='another@example.com',
                                                password='testpassword')
        id_user_to_delete = another_user.id
        delete_user_profile_url = reverse('account_delete_confirm', kwargs={'id': id_user_to_delete})
        response = self.client.get(delete_user_profile_url)
        self.assertEqual(response.status_code, 403)
