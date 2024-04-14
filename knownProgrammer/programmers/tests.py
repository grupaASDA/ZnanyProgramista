from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from programmers.models import ProgrammerProfile, Rating

User = get_user_model()


class ProgrammerProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.programmer_list_url = reverse('programmers_list')
        cls.programmer_create_url = reverse('programmer_create_form')
        cls.user_create_url = reverse('register')

    def setUp(self):
        # USERS
        self.user1 = User.objects.create(
            id=1,
            email="admin333@admin.com",
            first_name="John",
            last_name="Doe",
            is_dev=True,
        )
        self.user2 = User.objects.create(
            id=2,
            email="admin666@admin.com",
            first_name="Jane",
            last_name="Smith",
            is_dev=True,
        )
        self.user3 = User.objects.create(
            id=3,
            email="admin999@admin.com",
            first_name="Mike",
            last_name="Black",
            is_dev=True,
        )
        self.user4 = User.objects.create(
            id=4,
            email="admin123@admin.com",
            first_name="Tim",
            last_name="White",
            is_dev=True,
        )
        self.user5 = User.objects.create(
            id=5,
            email="admin000@admin.com",
            first_name="Test",
            last_name="User",
        )

        self.user_data = dict(
            email="test@email.com",
            first_name="Test",
            last_name="User",
            password1="admin123123",
            password2="admin123123",
        )

        # PROGRAMMERS
        self.programmer1 = ProgrammerProfile.objects.create(
            id=1,
            wage=70,
            description="Lorem asperiores cumque deleniti dolorem excepturi, quos repellendus sint, suscipit tempora temporibus vero! Iure, laboriosam.",
            experience="Mid",
            portfolio="http://example.com",
            programming_languages="Python,SQL,R",
            tech_stack="Django,FastAPI,Databases,Docker,Git | GitHub",
            phone=587412123,
            user_id_id=1,
        )
        self.programmer2 = ProgrammerProfile.objects.create(
            id=2,
            wage=100,
            description="Lorem asperiores cumque deleniti dolorem excepturi vero! Iure, laboriosam.",
            experience="Senior",
            portfolio="http://example.com",
            programming_languages="JavaScript,Python,R,SQL",
            tech_stack="Django,Flask,FastAPI,Databases,Docker,Git | GitHub",
            phone=505055505,
            user_id_id=2,
        )
        self.programmer3 = ProgrammerProfile.objects.create(
            id=3,
            wage=40,
            description="Iure, laboriosam.",
            experience="Junior",
            portfolio="http://example.com",
            programming_languages="Python,SQL",
            tech_stack="Django,Databases,Git | GitHub",
            phone=666999666,
            user_id_id=3,
        )
        self.programmer4 = ProgrammerProfile.objects.create(
            id=4,
            wage=60,
            description="Iure,asperiores cumque deleniti dolorem laboriosam.",
            experience="Mid",
            portfolio="http://example.com",
            programming_languages="Python,SQL,R",
            tech_stack="Django,FastAPI,Databases,Git | GitHub",
            phone=99658412,
            user_id_id=4,
        )
        self.programmer_data = dict(
            wage=10,
            description="Iure,asperiores cumque deleniti dolorem laboriosam.",
            experience="Junior",
            portfolio="http://example.com",
            programming_languages="Python",
            tech_stack="Git | GitHub",
            phone=666666666,
            user_id_id=5,
        )

        # RATINGS
        self.rating1 = Rating.objects.create(
            rating=3,
            programmer_id=2,
            user_id=1,
        )
        self.rating2 = Rating.objects.create(
            rating=5,
            programmer_id=3,
            user_id=1,
        )
        self.rating3 = Rating.objects.create(
            rating=3,
            programmer_id=1,
            user_id=2,
        )
        self.rating4 = Rating.objects.create(
            rating=3,
            programmer_id=3,
            user_id=2,
        )
        self.rating5 = Rating.objects.create(
            rating=4,
            programmer_id=4,
            user_id=2,
        )
        self.rating6 = Rating.objects.create(
            rating=2,
            programmer_id=1,
            user_id=3,
        )
        self.rating7 = Rating.objects.create(
            rating=4,
            programmer_id=2,
            user_id=3,
        )
        self.rating8 = Rating.objects.create(
            rating=5,
            programmer_id=3,
            user_id=4,
        )
        self.rating9 = Rating.objects.create(
            rating=5,
            programmer_id=1,
            user_id=4,
        )
        self.rating_data = dict(
            rating=5,
            programmer_id=1,
            user_id=5,
        )

    def test_set_up(self):
        users_count = User.objects.count()
        programmers_count = ProgrammerProfile.objects.count()
        ratings_count = Rating.objects.count()

        self.assertEqual(users_count, 5)
        self.assertEqual(programmers_count, 4)
        self.assertEqual(ratings_count, 9)

    def test_create_user_when_valid_data_given(self):
        expected_users_count = 6
        expected_status_code = 302
        response = self.client.post(self.user_create_url, data=self.user_data)
        users_count = User.objects.count()
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(expected_users_count, users_count)

    def test_create_user_when_invalid_data_given(self):
        expected_users_count = 5
        expected_status_code = 200
        self.user_data["password2"] = "111"
        response = self.client.post(self.user_create_url, data=self.user_data)
        users_count = User.objects.count()
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(expected_users_count, users_count)

    def test_create_programmer_when_valid_data_given(self):
        self.client.force_login(user=self.user5)
        expected_programmers_count = 5
        expected_status_code = 302
        response = self.client.post(self.programmer_create_url, data=self.programmer_data)
        programmers_count = ProgrammerProfile.objects.count()
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(expected_programmers_count, programmers_count)

    def test_create_programmer_when_invalid_data_given(self):
        self.client.force_login(user=self.user5)
        expected_programmers_count = 4
        expected_status_code = 200
        self.programmer_data["experience"] = "Super Senior"
        response = self.client.post(self.programmer_create_url, data=self.programmer_data)
        programmers_count = ProgrammerProfile.objects.count()
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(expected_programmers_count, programmers_count)

    def test_create_programmer_when_exists(self):
        self.client.force_login(user=self.user4)
        expected_programmers_count = 4
        expected_status_code = 403
        response = self.client.post(self.programmer_create_url, data=self.programmer_data)
        programmers_count = ProgrammerProfile.objects.count()
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(expected_programmers_count, programmers_count)

    def test_list_view_displays_proper_amount_of_programmers(self):
        logged_in_user = self.user4
        self.client.force_login(user=logged_in_user)
        response = self.client.get(self.programmer_list_url)
        response_programmers = response.context["programmers"]
        expected_programmers = ProgrammerProfile.objects.exclude(user_id=logged_in_user.id)
        self.assertQuerysetEqual(expected_programmers, response_programmers, ordered=False)
        self.assertEqual(response.status_code, 200)

    def test_display_programmer_when_logged_in(self):
        self.client.force_login(user=self.user5)

        id_to_get = self.user4.id
        programmer_profile_url = reverse('programmer_detail', kwargs={'id': id_to_get})
        response = self.client.get(programmer_profile_url)

        expected_programmer = ProgrammerProfile.objects.get(user_id=id_to_get)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "programmers/programmer_detail.html")
        self.assertEqual(expected_programmer.user_id_id, response.context['programmer'].user_id_id)
        self.assertEqual(expected_programmer.user_id.first_name, response.context['programmer'].user_id.first_name)
        self.assertEqual(expected_programmer.user_id.last_name, response.context['programmer'].user_id.last_name)
        self.assertEqual(expected_programmer.user_id.email, response.context['programmer'].user_id.email)
        self.assertEqual(expected_programmer.description, response.context['programmer'].description)
        self.assertEqual(expected_programmer.wage, response.context['programmer'].wage)
        self.assertEqual(expected_programmer.experience, response.context['programmer'].experience)
        self.assertEqual(expected_programmer.portfolio, response.context['programmer'].portfolio)
        self.assertEqual(expected_programmer.programming_languages,
                         response.context['programmer'].programming_languages)
        self.assertEqual(expected_programmer.tech_stack, response.context['programmer'].tech_stack)
        self.assertEqual(expected_programmer.phone, response.context['programmer'].phone)

    def test_display_programmer_when_logged_out(self):
        self.client.logout()
        id_to_get = self.user4.id
        programmer_profile_url = reverse('programmer_detail', kwargs={'id': id_to_get})
        response = self.client.get(programmer_profile_url, follow=True)

        self.assertRedirects(response, "/accounts/login/?next=/programmers/detail/4")
        self.assertEqual(response.status_code, 200)

    def test_edit_programmer_when_valid_data_given(self):
        edited_user = self.user4
        self.client.force_login(user=edited_user)

        id_programmer_to_edit = ProgrammerProfile.get_profile_by_user_id(edited_user.id).id
        edit_programmer_profile_url = reverse('programmer_update_model_form',
                                              kwargs={'id': id_programmer_to_edit}
                                              )
        response = self.client.get(edit_programmer_profile_url, data=self.programmer_data)

        expected_programmer = ProgrammerProfile.objects.get(user_id=id_programmer_to_edit)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "programmers/programmer_update_model_form.html")
        self.assertEqual(expected_programmer.user_id_id, response.context['programmer'].user_id_id)
        self.assertEqual(expected_programmer.user_id.first_name, response.context['programmer'].user_id.first_name)
        self.assertEqual(expected_programmer.user_id.last_name, response.context['programmer'].user_id.last_name)
        self.assertEqual(expected_programmer.user_id.email, response.context['programmer'].user_id.email)
        self.assertEqual(expected_programmer.description, response.context['programmer'].description)
        self.assertEqual(expected_programmer.wage, response.context['programmer'].wage)
        self.assertEqual(expected_programmer.experience, response.context['programmer'].experience)
        self.assertEqual(expected_programmer.portfolio, response.context['programmer'].portfolio)
        self.assertEqual(expected_programmer.programming_languages,
                         response.context['programmer'].programming_languages)
        self.assertEqual(expected_programmer.tech_stack, response.context['programmer'].tech_stack)
        self.assertEqual(expected_programmer.phone, response.context['programmer'].phone)

    def test_edit_programmer_when_valid_data_given_but_without_permission_given(self):
        self.client.force_login(user=self.user1)
        edited_user = self.user4

        id_programmer_to_edit = ProgrammerProfile.get_profile_by_user_id(edited_user.id).id
        edit_programmer_profile_url = reverse('programmer_update_model_form',
                                              kwargs={'id': id_programmer_to_edit}
                                              )
        response = self.client.get(edit_programmer_profile_url, data=self.programmer_data)

        self.assertEqual(response.status_code, 403)

    def test_edit_programmer_when_invalid_data_given(self):
        edited_user = self.user4
        self.client.force_login(user=edited_user)

        id_programmer_to_edit = ProgrammerProfile.get_profile_by_user_id(edited_user.id).id
        edit_programmer_profile_url = reverse('programmer_update_model_form',
                                              kwargs={'id': id_programmer_to_edit}
                                              )
        invalid_data = self.programmer_data
        invalid_data['experience'] = "Super Senior"

        response = self.client.get(edit_programmer_profile_url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['programmer'].experience, "Super Senior")

    def test_delete_programmer_profile_with_permission_given(self):
        deleted_programmer = self.user4
        self.client.force_login(user=deleted_programmer)
        no_of_programmers_before_delete = ProgrammerProfile.objects.count()

        id_programmer_to_delete = ProgrammerProfile.get_profile_by_user_id(deleted_programmer.id).id

        delete_programmer_profile_url = reverse('programmer_delete_confirm',
                                                kwargs={'id': id_programmer_to_delete}
                                                )
        response = self.client.post(delete_programmer_profile_url)

        no_of_programmers_after_delete = ProgrammerProfile.objects.count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(no_of_programmers_before_delete, no_of_programmers_after_delete + 1)

    def test_delete_programmer_profile_without_permission_given(self):
        self.client.force_login(user=self.user1)
        deleted_programmer = self.user4
        no_of_programmers_before_delete = ProgrammerProfile.objects.count()

        id_programmer_to_delete = ProgrammerProfile.get_profile_by_user_id(deleted_programmer.id).id

        delete_programmer_profile_url = reverse('programmer_delete_confirm',
                                                kwargs={'id': id_programmer_to_delete}
                                                )
        response = self.client.post(delete_programmer_profile_url)

        no_of_programmers_after_delete = ProgrammerProfile.objects.count()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(no_of_programmers_before_delete, no_of_programmers_after_delete)
