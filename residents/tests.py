from datetime import date

from django.utils import unittest

from .models import Room

from django.contrib.auth import get_user_model


class UserTest(unittest.TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username="1username1", password="password1")
        self.user2 = get_user_model().objects.create_user(username="2username2", password="password2")
        self.user3 = get_user_model().objects.create_user(username="3username3", password="password3")
        self.user4 = get_user_model().objects.create_user(username="4username4", password="password4")
        self.room1 = Room.objects.create(number=1)
        self.room2 = Room.objects.create(number=2)
        self.room3 = Room.objects.create(number=3)
        self.room1.add_user(self.user1, date(2000, 10, 1))
        self.room1.add_user(self.user2, date(2003, 11, 2))
        self.room1.add_user(self.user3, date(2005, 12, 3))
        self.room2.add_user(self.user2, date(2003, 12, 3))
        self.room2.add_user(self.user3, date(2009, 1, 4))

    def test_fields(self):
        """
        Check calculated properties
        """
        self.assertEqual(self.user1.startdate, date(2000, 10, 1))
        self.assertEqual(self.user2.startdate, date(2003, 11, 2))
        self.assertEqual(self.user3.startdate, date(2005, 12, 3))
        self.assertEqual(self.user4.startdate, None)

        self.assertEqual(self.user1.enddate, date(2003, 11, 2))
        self.assertEqual(self.user2.enddate, date(2009, 1, 4))
        self.assertEqual(self.user3.enddate, None)
        self.assertEqual(self.user4.enddate, None)

        self.assertEqual(self.room1.current_user(date(2002, 11, 2)), self.user1)
        self.assertEqual(self.room1.current_user(), self.user3)
        self.assertEqual(self.room2.current_user(), self.user3)
        self.assertEqual(self.room3.current_user(), None)

        self.assertEqual(self.user1.current_room(date(2002, 11, 2)), self.room1)
        self.assertEqual(self.user1.current_room(), None)
        self.assertEqual(self.user2.current_room(), None)
        self.assertEqual(self.user2.current_room(date(2008, 1, 1)), self.room2)
        self.assertEqual(self.user3.current_room(date(2008, 1, 1)), self.room1)

        self.assertTrue(self.user1.is_resident(date(2002, 11, 2)))
        self.assertFalse(self.user1.is_resident())
        self.assertFalse(self.user2.is_resident())
        self.assertTrue(self.user3.is_resident())
        self.assertFalse(self.user4.is_resident())
