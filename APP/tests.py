from django.test import TestCase
from django.contrib.auth.models import User
from .models import Hostel, Floor, Room, Booking, Review
from django.contrib.auth.models import User
from .models import Userprofile

# Unit testing where the each model is tested 
"""
class UserProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='password')
        Userprofile.objects.create(
            user=user, 
            name='Test User', 
            reg_number=12345, 
            Email_address='testuser@example.com',
            contact_no=1234567890, 
            gender='M',
            Father_name='Father Test', 
            Father_email_address='father@example.com', 
            Father_contact_no=1234567890,
            Mother_name='Mother Test', 
            Mother_email_address='mother@example.com', 
            Mother_contact_no=1234567890
        )

    def test_user_profile_creation(self):
        user_profile = Userprofile.objects.get(reg_number=12345)
        self.assertEqual(user_profile.name, 'Test User')
        self.assertEqual(user_profile.Email_address, 'testuser@example.com')

class HostelTestCase(TestCase):
    def setUp(self):
        Hostel.objects.create(name='Test Hostel', gender='M', description='A test hostel')

    def test_hostel_creation(self):
        hostel = Hostel.objects.get(name='Test Hostel')
        self.assertEqual(hostel.description, 'A test hostel')

class RoomTestCase(TestCase):
    def setUp(self):
        hostel = Hostel.objects.create(name='Test Hostel', gender='M', description='A test hostel')
        floor = Floor.objects.create(hostel=hostel, number=1)
        Room.objects.create(floor=floor, room='101', max_capacity=3, current_bookings=0, status='Vacant')

    def test_room_creation(self):
        room = Room.objects.get(room='101')
        self.assertEqual(room.max_capacity, 3)
        self.assertEqual(room.status, 'Vacant')

class BookingTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='password')
        hostel = Hostel.objects.create(name='Test Hostel', gender='M', description='A test hostel')
        floor = Floor.objects.create(hostel=hostel, number=1)
        room = Room.objects.create(floor=floor, room='101', max_capacity=3, current_bookings=0, status='Vacant')
        Booking.objects.create(user=user, room=room)

    def test_booking_creation(self):
        booking = Booking.objects.get(user__username='testuser')
        self.assertEqual(booking.room.room, '101')
        self.assertEqual(booking.user.username, 'testuser')

class ReviewTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', password='password')
        hostel = Hostel.objects.create(name='Test Hostel', gender='M', description='A test hostel')
        Review.objects.create(user=user, hostel=hostel, comment='Great hostel', reviews=5)

    def test_review_creation(self):
        review = Review.objects.get(user__username='testuser')
        self.assertEqual(review.comment, 'Great hostel')
        self.assertEqual(review.reviews, 5)
"""

# Integration testing where it sees the integration of different models and system

"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Userprofile, Hostel, Floor, Room, Booking, Review, Counselor
from .forms import CreateUserForm
from django.utils import timezone
import datetime

# Test Case for the Booking Room View
class BookingRoomViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile = Userprofile.objects.create(
            user=self.user, name='Test User', reg_number=12345, Email_address='testuser@example.com',
            contact_no=1234567890, gender='M'
        )
        self.client.login(username='testuser', password='password')
        
        self.hostel = Hostel.objects.create(name='Test Hostel', gender='M', description='A test hostel')
        self.floor = Floor.objects.create(hostel=self.hostel, number=1)
        self.room = Room.objects.create(floor=self.floor, room='101', max_capacity=1, current_bookings=0, status='Vacant')

    def test_booking_room_gender_mismatch(self):
        self.user_profile.gender = 'F'
        self.user_profile.save()
        response = self.client.get(reverse('booking_room', args=[self.room.id]))
        self.assertContains(response, "Gender mismatch error.")

    def test_booking_room_double_booking(self):
        Booking.objects.create(user=self.user, room=self.room, check_in=timezone.now(), check_out=timezone.now() + datetime.timedelta(days=1))
        response = self.client.get(reverse('booking_room', args=[self.room.id]))
        self.assertContains(response, "You cannot book a room more than twice")

    def test_booking_room_max_capacity(self):
        self.room.current_bookings = self.room.max_capacity
        self.room.save()
        response = self.client.get(reverse('booking_room', args=[self.room.id]))
        self.assertContains(response, "Maximum room capacity reached.")

    def test_successful_booking(self):
        response = self.client.post(reverse('booking_room', args=[self.room.id]), {
            'check_in': '2024-01-01',
            'check_out': '2024-06-01'
        })
        self.assertContains(response, "Booking have been successfully done")
        self.assertTrue(Booking.objects.filter(user=self.user, room=self.room).exists())
"""
# End-to-End testing
"""

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class EndToEndTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()  # or webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_registration_login_booking(self):
        # Navigate to the registration page
        self.browser.get(f'{self.live_server_url}/register/')
        time.sleep(1)

        # Fill out the registration form
        self.browser.find_element(By.NAME, 'username').send_keys('testuser')
        self.browser.find_element(By.NAME, 'password1').send_keys('password123')
        self.browser.find_element(By.NAME, 'password2').send_keys('password123')
        self.browser.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.browser.find_element(By.NAME, 'reg_number').send_keys('12345')
        self.browser.find_element(By.NAME, 'contact_no').send_keys('1234567890')
        self.browser.find_element(By.NAME, 'gender').send_keys('M')
        self.browser.find_element(By.NAME, 'father_name').send_keys('Father Test')
        self.browser.find_element(By.NAME, 'father_email').send_keys('father@example.com')
        self.browser.find_element(By.NAME, 'father_contact').send_keys('1234567890')
        self.browser.find_element(By.NAME, 'mother_name').send_keys('Mother Test')
        self.browser.find_element(By.NAME, 'mother_email').send_keys('mother@example.com')
        self.browser.find_element(By.NAME, 'mother_contact').send_keys('1234567890')
        self.browser.find_element(By.NAME, 'submit').click()
        time.sleep(2)

        # Navigate to the login page and log in
        self.browser.get(f'{self.live_server_url}/login/')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'username').send_keys('testuser')
        self.browser.find_element(By.NAME, 'password').send_keys('password123')
        self.browser.find_element(By.NAME, 'submit').click()
        time.sleep(2)

        # Check if login was successful by checking for a logout button
        self.assertIn('Logout', self.browser.page_source)

        # Navigate to the booking page
        self.browser.get(f'{self.live_server_url}/booking/')
        time.sleep(1)

        # Fill out the booking form (assuming room with id 1 exists)
        self.browser.get(f'{self.live_server_url}/booking_room/1/')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'check_in').send_keys('2024-01-01')
        self.browser.find_element(By.NAME, 'check_out').send_keys('2024-06-01')
        self.browser.find_element(By.NAME, 'submit').click()
        time.sleep(2)

        # Check if the booking was successful by checking for confirmation message
        self.assertIn('Booking have been successfully done', self.browser.page_source)
"""




