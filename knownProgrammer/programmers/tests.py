import os

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseNotFound
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser, DEFAULT_AVATAR
from programmers.forms import ProgrammerCreationModelForm, RatingForm, AvatarUploadForm
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
            avatar='Test_avatar.jpg'
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
            user_id=5,
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
        self.new_rating_data = dict(
            rating=5,
            programmer_id=4,
            user_id=1,
        )
        self.changed_rating_data = dict(
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

    def test_GET_create_user_when_valid_data_given(self):
        expected_users_count = 5
        expected_get_status_code = 200

        response_get = self.client.get(self.user_create_url)
        users_count = User.objects.count()
        self.assertEqual(response_get.status_code, expected_get_status_code)
        self.assertEqual(expected_users_count, users_count)

    def test_POST_create_user_when_valid_data_given(self):
        expected_users_count = 6
        expected_post_status_code = 302
        response_post = self.client.post(self.user_create_url, data=self.user_data)
        users_count = User.objects.count()
        self.assertEqual(response_post.status_code, expected_post_status_code)
        self.assertEqual(expected_users_count, users_count)

    def test_GET_create_user_when_invalid_data_given(self):
        expected_users_count = 5
        expected_status_code = 200
        self.user_data["password2"] = "111"
        response_get = self.client.get(self.user_create_url)

        users_count = User.objects.count()
        self.assertEqual(response_get.status_code, expected_status_code)
        self.assertEqual(expected_users_count, users_count)

    def test_POST_create_user_when_invalid_data_given(self):
        expected_users_count = 5
        expected_status_code = 200
        self.user_data["password2"] = "111"
        response_post = self.client.post(self.user_create_url, data=self.user_data)
        users_count = User.objects.count()

        self.assertEqual(response_post.status_code, expected_status_code)
        self.assertEqual(expected_users_count, users_count)

    def test_GET_create_programmer_when_valid_data_given(self):
        self.client.force_login(user=self.user5)
        expected_programmers_count = 4
        expected_get_status_code = 200
        response_get = self.client.get(self.programmer_create_url)
        form = response_get.context['form']
        programmers_count = ProgrammerProfile.objects.count()
        self.assertEqual(response_get.status_code, expected_get_status_code)
        self.assertTemplateUsed(response_get, "programmers/programmer_create_model_form.html")
        self.assertIsInstance(form, ProgrammerCreationModelForm)
        self.assertEqual(expected_programmers_count, programmers_count)

    def test_POST_create_programmer_when_valid_data_given(self):
        self.client.force_login(user=self.user5)
        expected_programmers_count = 5
        expected_post_status_code = 302
        response_post = self.client.post(self.programmer_create_url, data=self.programmer_data)
        programmers_count = ProgrammerProfile.objects.count()

        self.assertEqual(response_post.status_code, expected_post_status_code)
        self.assertEqual(expected_programmers_count, programmers_count)

    def test_GET_create_programmer_when_invalid_data_given(self):
        self.client.force_login(user=self.user5)
        expected_programmers_count = 4
        self.programmer_data["experience"] = "Super Senior"
        expected_status_code = 200
        response_get = self.client.get(self.programmer_create_url)
        form = response_get.context['form']
        programmers_count = ProgrammerProfile.objects.count()

        self.assertEqual(response_get.status_code, expected_status_code)
        self.assertTemplateUsed(response_get, "programmers/programmer_create_model_form.html")
        self.assertIsInstance(form, ProgrammerCreationModelForm)
        self.assertEqual(expected_programmers_count, programmers_count)

    def test_POST_create_programmer_when_invalid_data_given(self):
        self.client.force_login(user=self.user5)
        expected_programmers_count = 4
        self.programmer_data["experience"] = "Super Senior"
        expected_status_code = 200
        response_post = self.client.post(self.programmer_create_url, data=self.programmer_data)
        programmers_count = ProgrammerProfile.objects.count()

        self.assertEqual(response_post.status_code, expected_status_code)
        self.assertEqual(expected_programmers_count, programmers_count)

    def test_POST_create_programmer_when_exists(self):
        self.client.force_login(user=self.user4)
        expected_programmers_count = 4
        expected_status_code = 403
        response = self.client.post(self.programmer_create_url, data=self.programmer_data)
        programmers_count = ProgrammerProfile.objects.count()
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(expected_programmers_count, programmers_count)

    def test_GET_list_view_displays_proper_amount_of_programmers(self):
        logged_in_user = self.user4
        self.client.force_login(user=logged_in_user)
        response_get = self.client.get(self.programmer_list_url)
        response_programmers = response_get.context["programmers"]
        expected_programmers = ProgrammerProfile.objects.exclude(user_id=logged_in_user.id)
        self.assertQuerysetEqual(expected_programmers, response_programmers, ordered=False)
        self.assertTemplateUsed(response_get, "programmers/programmers_list.html")
        self.assertEqual(response_get.status_code, 200)

    def test_GET_display_programmer_when_logged_in(self):
        self.client.force_login(user=self.user5)

        id_to_get = self.programmer4.id
        programmer_profile_url = reverse('programmer_detail', kwargs={'id': id_to_get})
        response = self.client.get(programmer_profile_url)

        expected_programmer = ProgrammerProfile.objects.get(user_id=id_to_get)
        expected_avg_rating = expected_programmer.average_rating()
        response_avg_rating = response.context['programmer'].average_rating

        expected_rating_count = expected_programmer.ratings_count()
        response_rating_count = response.context['programmer'].ratings_count()

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
        self.assertEqual(expected_avg_rating, response_avg_rating)
        self.assertEqual(expected_rating_count, response_rating_count)

    def test_display_programmer_when_logged_out(self):
        self.client.logout()
        id_to_get = self.programmer4.id
        programmer_profile_url = reverse('programmer_detail', kwargs={'id': id_to_get})
        response = self.client.get(programmer_profile_url, follow=True)

        self.assertRedirects(response, "/accounts/login/?next=/programmers/detail/4")
        self.assertEqual(response.status_code, 200)

    def test_display_programmer_when_doesnt_exist(self):
        self.client.force_login(user=self.user5)
        invalid_id = 999

        programmer_profile_url = reverse('programmer_detail', kwargs={'id': invalid_id})
        response = self.client.get(programmer_profile_url)

        self.assertEqual(response.status_code, 404)
        self.assertIn("Not Found", response.content.decode('utf-8'))
        self.assertIsInstance(response, HttpResponseNotFound)

    def test_if_user_is_owner_true(self):
        self.client.force_login(user=self.user1)
        id_to_get = self.programmer1.id
        programmer_profile_url = reverse('programmer_detail', kwargs={'id': id_to_get})
        response = self.client.get(programmer_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "programmers/programmer_detail.html")
        self.assertEqual(response.context['programmer'].user_id_id, id_to_get)
        self.assertEqual(response.context['owner'], True)

    def test_if_user_is_owner_false(self):
        self.client.force_login(user=self.user1)
        id_to_get = self.programmer4.id
        programmer_profile_url = reverse('programmer_detail', kwargs={'id': id_to_get})
        response = self.client.get(programmer_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "programmers/programmer_detail.html")
        self.assertEqual(response.context['programmer'].user_id_id, id_to_get)
        self.assertEqual(response.context['owner'], False)

    def test_if_user_rated_programmer_true(self):
        self.client.force_login(user=self.user1)
        id_to_get = self.programmer2.id
        programmer_profile_url = reverse('programmer_detail', kwargs={'id': id_to_get})
        response = self.client.get(programmer_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "programmers/programmer_detail.html")
        self.assertEqual(response.context['rated'], True)

    def test_if_user_rated_programmer_false(self):
        self.client.force_login(user=self.user1)
        id_to_get = self.programmer4.id
        programmer_profile_url = reverse('programmer_detail', kwargs={'id': id_to_get})
        response = self.client.get(programmer_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "programmers/programmer_detail.html")
        self.assertEqual(response.context['rated'], False)

    def test_GET_edit_programmer_when_valid_data_given(self):
        edited_user = self.user4
        self.client.force_login(user=edited_user)

        id_programmer_to_edit = ProgrammerProfile.get_profile_by_user_id(edited_user.id).id
        edit_programmer_profile_url = reverse('programmer_update_model_form',
                                              kwargs={'id': id_programmer_to_edit}
                                              )
        response_get = self.client.get(edit_programmer_profile_url)

        expected_status_code = 200
        form = response_get.context['form']

        self.assertEqual(response_get.status_code, expected_status_code)
        self.assertTemplateUsed(response_get, "programmers/programmer_update_model_form.html")
        self.assertIsInstance(form, ProgrammerCreationModelForm)

    def test_POST_edit_programmer_when_valid_data_given(self):
        edited_user = self.user4
        self.client.force_login(user=edited_user)

        programmer_to_edit = ProgrammerProfile.get_profile_by_user_id(edited_user.id)
        edit_programmer_profile_url = reverse('programmer_update_model_form',
                                              kwargs={'id': programmer_to_edit.id}
                                              )

        response_post = self.client.post(edit_programmer_profile_url, data=self.programmer_data, follow=True)

        expected_status_code = 200

        expected_programmer = ProgrammerProfile.objects.get(user_id=programmer_to_edit.id)

        self.assertEqual(response_post.status_code, expected_status_code)
        self.assertEqual(expected_programmer.user_id_id, response_post.context['programmer'].user_id_id)
        self.assertEqual(expected_programmer.user_id.first_name, response_post.context['programmer'].user_id.first_name)
        self.assertEqual(expected_programmer.user_id.last_name, response_post.context['programmer'].user_id.last_name)
        self.assertEqual(expected_programmer.user_id.email, response_post.context['programmer'].user_id.email)
        self.assertEqual(expected_programmer.description, response_post.context['programmer'].description)
        self.assertEqual(expected_programmer.wage, response_post.context['programmer'].wage)
        self.assertEqual(expected_programmer.experience, response_post.context['programmer'].experience)
        self.assertEqual(expected_programmer.portfolio, response_post.context['programmer'].portfolio)
        self.assertEqual(expected_programmer.programming_languages,
                         response_post.context['programmer'].programming_languages)
        self.assertEqual(expected_programmer.tech_stack, response_post.context['programmer'].tech_stack)
        self.assertEqual(expected_programmer.phone, response_post.context['programmer'].phone)
        self.assertContains(response_post,
                            f"Programmer {programmer_to_edit.user_id.first_name} {programmer_to_edit.user_id.last_name} has been successfully edited")

    def test_POST_edit_programmer_when_valid_data_given_but_without_permission_given(self):
        self.client.force_login(user=self.user1)
        edited_user = self.user4

        id_programmer_to_edit = ProgrammerProfile.get_profile_by_user_id(edited_user.id).id
        edit_programmer_profile_url = reverse('programmer_update_model_form',
                                              kwargs={'id': id_programmer_to_edit}
                                              )
        response = self.client.post(edit_programmer_profile_url, data=self.programmer_data)

        self.assertEqual(response.status_code, 403)

    def test_POST_edit_programmer_when_invalid_data_given(self):
        edited_user = self.user4
        self.client.force_login(user=edited_user)

        id_programmer_to_edit = ProgrammerProfile.get_profile_by_user_id(edited_user.id).id
        edit_programmer_profile_url = reverse('programmer_update_model_form',
                                              kwargs={'id': id_programmer_to_edit}
                                              )
        invalid_data = self.programmer_data
        invalid_data['experience'] = "Super Senior"

        response = self.client.post(edit_programmer_profile_url, data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['programmer'].experience, "Super Senior")

    def test_GET_delete_programmer_profile_with_permission_given(self):
        deleted_programmer = self.user4
        self.client.force_login(user=deleted_programmer)

        id_programmer_to_delete = ProgrammerProfile.get_profile_by_user_id(deleted_programmer.id).id

        delete_programmer_profile_url = reverse('programmer_delete_confirm',
                                                kwargs={'id': id_programmer_to_delete}
                                                )
        response_get = self.client.get(delete_programmer_profile_url)

        expected_get_status_code = 200

        self.assertEqual(response_get.status_code, expected_get_status_code)
        self.assertTemplateUsed(response_get, "programmers/programmer_delete_confirm.html")

    def test_POST_delete_programmer_profile_with_permission_given(self):
        deleted_programmer = self.user4
        self.client.force_login(user=deleted_programmer)
        no_of_programmers_before_delete = ProgrammerProfile.objects.count()

        programmer_to_delete = ProgrammerProfile.get_profile_by_user_id(deleted_programmer.id)

        delete_programmer_profile_url = reverse('programmer_delete_confirm',
                                                kwargs={'id': programmer_to_delete.id}
                                                )

        response_post = self.client.post(delete_programmer_profile_url, follow=True)

        expected_post_status_code = 200

        no_of_programmers_after_delete = ProgrammerProfile.objects.count()

        self.assertEqual(response_post.status_code, expected_post_status_code)
        self.assertNotEqual(no_of_programmers_before_delete, no_of_programmers_after_delete)
        self.assertContains(response_post,
                            f"Programmer {programmer_to_delete.user_id.first_name} {programmer_to_delete.user_id.last_name} has been successfully deleted")

    def test_POST_delete_programmer_profile_without_permission_given(self):
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

    def test_GET_rate_programmer_profile_with_permission_given(self):
        rated_programmer = self.programmer4
        self.client.force_login(user=self.user1)

        id_programmer_to_rate = ProgrammerProfile.get_profile_by_user_id(rated_programmer.id).id

        rate_programmer_profile_url = reverse('rate_programmer',
                                              kwargs={'id': id_programmer_to_rate}
                                              )
        response_get = self.client.get(rate_programmer_profile_url)
        form = response_get.context['form']
        programmer = response_get.context['programmer']

        expected_get_status_code = 200

        self.assertEqual(response_get.status_code, expected_get_status_code)
        self.assertTemplateUsed(response_get, "programmers/rate_programmer.html")
        self.assertEqual(programmer, rated_programmer)
        self.assertIsInstance(form, RatingForm)

    def test_GET_update_rate_programmer_profile_with_permission_given(self):
        rated_programmer = self.programmer1
        self.client.force_login(user=self.user5)

        id_programmer_to_rate = ProgrammerProfile.get_profile_by_user_id(rated_programmer.id).id

        rate_programmer_profile_url = reverse('rate_programmer',
                                              kwargs={'id': id_programmer_to_rate}
                                              )
        response_get = self.client.get(rate_programmer_profile_url)
        form = response_get.context['form']
        programmer = response_get.context['programmer']

        expected_get_status_code = 200

        self.assertEqual(response_get.status_code, expected_get_status_code)
        self.assertTemplateUsed(response_get, "programmers/rate_programmer.html")
        self.assertEqual(programmer, rated_programmer)
        self.assertIsInstance(form, RatingForm)

    def test_GET_rate_yourself_exception(self):
        user = self.user1
        rated_programmer = user
        self.client.force_login(user=user)

        id_programmer_to_rate = ProgrammerProfile.get_profile_by_user_id(rated_programmer.id).id

        rate_programmer_profile_url = reverse('rate_programmer',
                                              kwargs={'id': id_programmer_to_rate}
                                              )
        response_get = self.client.get(rate_programmer_profile_url)

        expected_get_status_code = 403

        self.assertEqual(response_get.status_code, expected_get_status_code)

    def test_POST_rate_programmer_profile_for_the_first_time_with_permission_given(self):
        rated_programmer = self.programmer4
        user = self.user1
        avg_rating_before = rated_programmer.average_rating()
        is_rated_before = rated_programmer.is_rated(user)

        self.client.force_login(user=user)

        id_programmer_to_rate = ProgrammerProfile.get_profile_by_user_id(rated_programmer.id).id

        rate_programmer_profile_url = reverse('rate_programmer',
                                              kwargs={'id': id_programmer_to_rate}
                                              )
        response_post = self.client.post(rate_programmer_profile_url, data=self.new_rating_data)
        is_rated_after = rated_programmer.is_rated(user)

        avg_rating_after = rated_programmer.average_rating()

        expected_post_status_code = 200

        self.assertEqual(response_post.status_code, expected_post_status_code)
        self.assertNotEqual(avg_rating_before, avg_rating_after)
        self.assertFalse(is_rated_before)
        self.assertTrue(is_rated_after)
        self.assertContains(response_post, "Your rating has been submitted.")

    def test_POST_change_rating_for_programmer_profile(self):
        user = self.user5
        self.client.force_login(user=user)
        rated_programmer = self.programmer1
        avg_rating_before = rated_programmer.average_rating()
        is_rated_before = rated_programmer.is_rated(user)

        id_programmer_to_rate = ProgrammerProfile.get_profile_by_user_id(rated_programmer.id).id

        rate_programmer_profile_url = reverse('rate_programmer',
                                              kwargs={'id': id_programmer_to_rate}
                                              )
        response_post = self.client.post(rate_programmer_profile_url, data=self.changed_rating_data)

        avg_rating_after = rated_programmer.average_rating()

        expected_post_status_code = 200

        self.assertEqual(response_post.status_code, expected_post_status_code)
        self.assertNotEqual(avg_rating_before, avg_rating_after)
        self.assertTrue(is_rated_before)
        self.assertContains(response_post, "Your rating has been updated.")

    def test_POST_rate_programmer_with_invalid_form(self):
        self.client.force_login(user=self.user5)
        invalid_programmer_id = 999

        rate_programmer_profile_url = reverse('rate_programmer',
                                              kwargs={'id': invalid_programmer_id}
                                              )
        response_post = self.client.post(rate_programmer_profile_url, data=self.new_rating_data)

        expected_post_status_code = 404

        self.assertEqual(response_post.status_code, expected_post_status_code)
        self.assertIn("Not Found", response_post.content.decode('utf-8'))
        self.assertIsInstance(response_post, HttpResponseNotFound)

    def test_POST_rate_programmer_profile_when_doesnt_exist(self):
        self.client.force_login(user=self.user5)
        rated_programmer = self.programmer1

        rating_data = self.changed_rating_data
        invalid_rating_data = rating_data.copy()
        invalid_rating_data['rating'] = -4
        id_programmer_to_rate = ProgrammerProfile.get_profile_by_user_id(rated_programmer.id).id

        rate_programmer_profile_url = reverse('rate_programmer',
                                              kwargs={'id': id_programmer_to_rate}
                                              )
        response_post = self.client.post(rate_programmer_profile_url, data=invalid_rating_data)

        expected_post_status_code = 302

        self.assertEqual(response_post.status_code, expected_post_status_code)

    def test_GET_upload_avatar(self):
        edited_user = self.user4
        self.client.force_login(user=edited_user)

        upload_avatar_url = reverse('upload_avatar',
                                    kwargs={'id': edited_user.id}
                                    )
        response_get = self.client.get(upload_avatar_url)

        expected_status_code = 200
        form = response_get.context['form']

        self.assertEqual(response_get.status_code, expected_status_code)
        self.assertTemplateUsed(response_get, "programmers/programmer_avatar_update.html")
        self.assertIsInstance(form, AvatarUploadForm)

    def test_GET_upload_avatar_permission_denied(self):
        edited_user = self.user4
        self.client.force_login(user=self.user2)

        upload_avatar_url = reverse('upload_avatar', kwargs={'id': edited_user.id})

        response_get = self.client.get(upload_avatar_url)

        expected_status_code = 403

        self.assertEqual(response_get.status_code, expected_status_code)
        self.assertRaises(PermissionDenied)

    def test_POST_upload_avatar_success(self):
        edited_user = self.user4
        self.client.force_login(user=edited_user)

        user_to_upload_avatar = CustomUser.objects.get(id=edited_user.id)
        initial_avatar = user_to_upload_avatar.avatar

        upload_avatar_url = reverse('upload_avatar',
                                    kwargs={'id': edited_user.id}
                                    )

        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        grandparent_directory = os.path.dirname(parent_directory)
        image_path = os.path.join(grandparent_directory, "README_images/Python.png")

        with open(image_path, "rb") as file:
            uploaded_file = SimpleUploadedFile("Python.png", file.read(), content_type="image/png")

        response_post = self.client.post(upload_avatar_url, {"avatar": uploaded_file})

        expected_user = CustomUser.objects.get(id=edited_user.id)

        expected_status_code = 302

        response_get = self.client.get(response_post.url)

        self.assertEqual(response_post.status_code, expected_status_code)
        self.assertNotEqual(initial_avatar, expected_user.avatar)
        self.assertContains(response_get, "Your avatar has been successfully uploaded.")

    def test_POST_upload_avatar_failed(self):
        edited_user = self.user4
        self.client.force_login(user=edited_user)

        upload_avatar_url = reverse('upload_avatar',
                                    kwargs={'id': edited_user.id}
                                    )

        invalid_uploaded_file = "Invalid.png"

        response_post = self.client.post(upload_avatar_url, {"avatar": invalid_uploaded_file})

        expected_status_code = 200

        self.assertEqual(response_post.status_code, expected_status_code)
        self.assertContains(response_post, "Invalid form submission.")

    def test_GET_restore_default_avatar(self):
        user_to_restore_avatar = self.user4
        self.client.force_login(user=user_to_restore_avatar)

        restore_avatar_url = reverse('restore_avatar', kwargs={'id': user_to_restore_avatar.id})

        response_get = self.client.get(restore_avatar_url)
        form = response_get.context["form"]
        expected_status_code = 200

        self.assertEqual(response_get.status_code, expected_status_code)
        self.assertIsInstance(form, AvatarUploadForm)

    def test_POST_restore_default_avatar(self):
        user_to_restore_avatar = self.user4
        self.client.force_login(user=user_to_restore_avatar)
        initial_avatar = user_to_restore_avatar.avatar

        restore_avatar_url = reverse('restore_avatar', kwargs={'id': user_to_restore_avatar.id})

        response_post = self.client.post(restore_avatar_url, follow=True)

        expected_user = CustomUser.objects.get(id=user_to_restore_avatar.id)
        expected_status_code = 200

        self.assertEqual(response_post.status_code, expected_status_code)
        self.assertNotEqual(initial_avatar, expected_user.avatar)
        self.assertEqual(expected_user.avatar, DEFAULT_AVATAR)
        self.assertContains(response_post, "Your avatar has been successfully restored to default.")

    def test_POST_restore_default_avatar_permission_denied(self):
        user_to_restore_avatar = self.user4
        self.client.force_login(user=self.user2)
        initial_avatar = user_to_restore_avatar.avatar

        restore_avatar_url = reverse('restore_avatar', kwargs={'id': user_to_restore_avatar.id})

        response_post = self.client.post(restore_avatar_url, follow=True)

        expected_user = CustomUser.objects.get(id=user_to_restore_avatar.id)
        expected_status_code = 403

        self.assertEqual(response_post.status_code, expected_status_code)
        self.assertEqual(initial_avatar, expected_user.avatar)
        self.assertRaises(PermissionDenied)

    def test_GET_my_profile_view(self):
        user_to_view = self.user2
        self.client.force_login(user=user_to_view)
        my_profile_url = reverse('my_profile', kwargs={'id': user_to_view.id})

        response_get = self.client.get(my_profile_url)
        expected_status_code = 200

        self.assertEqual(response_get.status_code, expected_status_code)
        self.assertTemplateUsed(response_get, "programmers/my_profile.html")

    def test_GET_my_profile_view_permission_denied(self):
        user_to_view = self.user4
        self.client.force_login(user=self.user2)
        my_profile_url = reverse('my_profile', kwargs={'id': user_to_view.id})

        response_post = self.client.get(my_profile_url)

        expected_status_code = 403

        self.assertEqual(response_post.status_code, expected_status_code)
        self.assertRaises(PermissionDenied)
