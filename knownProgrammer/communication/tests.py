from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from programmers.models import ProgrammerProfile
from communication.models import Message
from datetime import datetime

User = get_user_model()

class MessagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.contacts_list_url = reverse('messages_person_list')
        cls.user_create_url = reverse('register')

    def setUp(self):
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
            is_dev=False,
        )
        self.user4 = User.objects.create(
            id=4,
            email="admin123@admin.com",
            first_name="Tim",
            last_name="White",
            is_dev=False,
        )

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

        self.message1 = Message.objects.create(
            id=1,
            sent_by = self.user3,
            sent_to = self.user1,
            title = "Title 1",
            content = "Content 1",
            created_at = datetime.now(),
        )
        self.message2 = Message.objects.create(
            id=2,
            sent_by=self.user4,
            sent_to=self.user2,
            title="Title 2",
            content="Content 2",
            created_at=datetime.now(),
        )
        self.message3 = Message.objects.create(
            id=3,
            sent_by=self.user3,
            sent_to=self.user2,
            title="Title 3",
            content="Content 3",
            created_at=datetime.now(),
        )
        self.message4 = Message.objects.create(
            id=4,
            sent_by=self.user4,
            sent_to=self.user1,
            title="Re: Title 4",
            content="Content 4",
            created_at=datetime.now(),
        )

        self.message5_replay = Message.objects.create(
        id = 5,
        sent_by = self.user1,
        sent_to = self.user3,
        title = "Re: Title 1",
        content = "Content 5",
        created_at = datetime.now(),
        )

        self.message6_replay = Message.objects.create(
            id=6,
            sent_by=self.user2,
            sent_to=self.user4,
            title="Re: Title 2",
            content="Content 6",
            created_at=datetime.now(),
        )

        self.message7_sent_again = Message.objects.create(
            id=7,
            sent_by=self.user4,
            sent_to=self.user2,
            title="Re: Title 2",
            content="Content 7",
            created_at=datetime.now(),
        )

        self.message8_sent_again = Message.objects.create(
            id=8,
            sent_by=self.user4,
            sent_to=self.user2,
            title="Re: Title 2",
            content="Content 8",
            created_at=datetime.now(),
        )
        self.message9 = Message.objects.create(
            id=9,
            sent_by=self.user2,
            sent_to=self.user4,
            title="Title 9",
            content="Content 9",
            created_at=datetime.now(),
        )

        self.message_data1 = dict(
            sent_by = self.user3,
            sent_to = self.user1,
            title = "Title 10",
            content = "Content 10",
        )

        self.message_respond_1 = dict(
            sent_by=self.user1,
            sent_to=self.user3,
            title="Re: Title 1",
            content="Content 5",
        )
        self.message_send_again_1 = dict(
            sent_by=self.user3,
            sent_to=self.user1,
            title="Re: Title 1",
            content="Content 5",
        )

    def test_set_up(self):
        users_count = User.objects.count()
        programmers_count = ProgrammerProfile.objects.count()
        messages_count = Message.objects.count()

        self.assertEqual(users_count, 4)
        self.assertEqual(programmers_count, 2)
        self.assertEqual(messages_count, 9)

    def test_send_message_when_valid_data_given(self):
        self.client.force_login(user=self.user3)
        message_to_send = self.message_data1
        expected_message_count = 10
        expected_status_code = 302
        send_message_url = reverse('send_message', kwargs={'id': message_to_send['sent_to'].id})
        response = self.client.post(send_message_url, data=message_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/send_message.html")
        self.assertEqual(expected_message_count, messages_count)

    def test_send_message_when_invalid_data_given_message_to_yourself(self):
        #SENDING MESSAGE TO YOURSELF
        self.client.force_login(user=self.user3)
        message_to_send = self.message_data1
        expected_message_count = 9
        expected_status_code = 403
        send_message_url = reverse('send_message', kwargs={'id': message_to_send['sent_by'].id})
        response = self.client.post(send_message_url, data=message_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/send_message.html")
        self.assertEqual(expected_message_count, messages_count)
    def test_send_message_when_invalid_data_given_without_logging(self):
        #WITHOUT LOGGING
        message_to_send = self.message_data1
        expected_message_count = 9
        expected_status_code = 302
        send_message_url = reverse('send_message', kwargs={'id': message_to_send['sent_to'].id})
        response = self.client.post(send_message_url, data=message_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/send_message.html")
        self.assertEqual(expected_message_count, messages_count)
    def test_send_message_when_invalid_data_given_sent_to_user_doesnt_exist(self):
        #USER SENT_TO DOESNT'T EXIST
        self.client.force_login(user=self.user3)
        message_to_send = self.message_data1
        invalid_id = 999
        expected_message_count = 9
        expected_status_code = 403
        send_message_url = reverse('send_message', kwargs={'id': invalid_id})
        print(send_message_url)
        response = self.client.post(send_message_url, data=message_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/send_message.html")
        self.assertEqual(expected_message_count, messages_count)

    def test_send_replay_message_when_valid_data_given(self):
        self.client.force_login(user=self.user1)
        message_i_respond_on = self.message1
        replay_to_send = self.message_respond_1
        expected_message_count = 10
        expected_status_code = 302
        send_replay_url = reverse('replay', kwargs={'id': message_i_respond_on.id})
        response = self.client.post(send_replay_url, data=replay_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/replay_message.html")
        self.assertEqual(expected_message_count, messages_count)

    def test_send_replay_message_when_invalid_data_given_access_denied(self):
        #WRONG USER (ACCESS DENIED)
        self.client.force_login(user=self.user2)
        message_i_respond_on = self.message1
        replay_to_send = self.message_respond_1
        expected_message_count = 9
        expected_status_code = 403
        send_replay_url = reverse('replay', kwargs={'id': message_i_respond_on.id})
        response = self.client.post(send_replay_url, data=replay_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/replay_message.html")
        self.assertEqual(expected_message_count, messages_count)
    def test_send_replay_message_when_invalid_data_given_user_not_logged_in(self):
        #USER NOT LOGGED IN
        message_i_respond_on = self.message1
        replay_to_send = self.message_respond_1
        expected_message_count = 9
        expected_status_code = 403
        send_replay_url = reverse('replay', kwargs={'id': message_i_respond_on.id})
        response = self.client.post(send_replay_url, data=replay_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/replay_message.html")
        self.assertEqual(expected_message_count, messages_count)

    def test_send_replay_message_when_invalid_data_given_user_doesnt_exist(self):
        #USER DOESN'T EXIST
        message_i_respond_on = self.message1
        replay_to_send = self.message_respond_1
        expected_message_count = 9
        expected_status_code = 403
        del self.user3
        send_replay_url = reverse('replay', kwargs={'id': message_i_respond_on.id})
        response = self.client.post(send_replay_url, data=replay_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/replay_message.html")
        self.assertEqual(expected_message_count, messages_count)
    def test_send_replay_message_when_invalid_data_given_message_doesnt_exist(self):
        message_i_respond_on = self.message1
        replay_to_send = self.message_respond_1
        expected_message_count = 9
        expected_status_code = 403
        del self.message1
        send_replay_url = reverse('replay', kwargs={'id': message_i_respond_on.id})
        response = self.client.post(send_replay_url, data=replay_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/replay_message.html")
        self.assertEqual(expected_message_count, messages_count)
    def test_send_message_again_when_valid_data_given(self):
        self.client.force_login(user=self.user3)
        message_i_respond_on = self.message1
        replay_to_send = self.message_send_again_1
        expected_message_count = 10
        expected_status_code = 302
        send_replay_url = reverse('replay', kwargs={'id': message_i_respond_on.id})
        response = self.client.post(send_replay_url, data=replay_to_send)
        messages_count = Message.objects.count()

        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed("communication/replay_message.html")
        self.assertEqual(expected_message_count, messages_count)
        




