from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime

# Create your tests here.

from .models import Profile, Post


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.usr = User(username='bob')
        cls.usr.save()
        p1 = Profile.objects.get(id=1)
        p1.phone_number = '+79652493901'
        p1.save()
        cls.usr2 = User(username='tom')
        cls.usr2.save()
        p2 = Profile.objects.get(id=2)
        p2.phone_number = '+79654493901'
        p2.save()
        #cls.profile2 = Profile(user=cls.usr2, phone_number='+79752493902')
        # cls.u = User.objects.create(username='bob')
        # cls.u1 = Profile.objects.create(user=cls.u, phone_number='+79652493901')
        # p1 = Post.objects.create(author=u1, body='some text')

    def test_it_has_information_fields(self):
        self.profile = Profile.objects.get(id=1)
        self.assertIsInstance(self.profile.username, str)
        self.assertIsInstance(self.profile.bio, str)


    def test_it_has_timestamps(self):
        self.profile = Profile.objects.get(id=1)
        self.assertIsInstance(self.profile.created, datetime)

    # def test_username_label(self):
    #     user = Profile.objects.get(id=1)
    #     field_label = user._meta.get_field('username').verbose_name
    #     self.assertEquals(field_label, 'username')

    def test_bio_adding(self):
        user = Profile.objects.get(id=1)
        user.bio = 'This is my bio'
        self.assertEquals(user.bio, 'This is my bio')

    def test_avatar_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('avatar').verbose_name
        self.assertEquals(field_label, 'avatar')

