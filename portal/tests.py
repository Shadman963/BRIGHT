import copy
from django.template.context import BaseContext

# Python 3.14 compatibility patch for Django BaseContext copy during test client rendering
_original_basecontext_copy = BaseContext.__copy__
def _compat_basecontext_copy(self):
    duplicate = object.__new__(self.__class__)
    duplicate.dicts = self.dicts[:]
    return duplicate
BaseContext.__copy__ = _compat_basecontext_copy

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from portal.models import StudentApplication, StudentProfile


class PortalDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='student_test@example.com',
            email='student_test@example.com',
            password='testpassword123',
            first_name='John',
            last_name='Doe'
        )
        StudentProfile.objects.create(
            user=self.user,
            phone='+8801700000000',
            nationality='Bangladesh'
        )

    def test_dashboard_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('portal:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('portal:login'), response.url)

    def test_dashboard_authenticated_without_application(self):
        self.client.login(username='student_test@example.com', password='testpassword123')
        response = self.client.get(reverse('portal:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/dashboard.html')
        self.assertContains(response, 'Start Your Study Abroad Application')

    def test_dashboard_authenticated_with_application(self):
        app = StudentApplication.objects.create(
            student=self.user,
            preferred_university_name='Tsinghua University',
            preferred_program_name='Software Engineering',
            status='Document Checking',
            highest_qualification='HSC',
            institute_name='City College',
            graduation_year=2024,
            cgpa_or_percentage='4.00'
        )
        self.client.login(username='student_test@example.com', password='testpassword123')
        response = self.client.get(reverse('portal:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/dashboard.html')
        self.assertContains(response, app.application_id)
        self.assertContains(response, 'Current Stage')
        self.assertContains(response, 'Completed ✓')
        self.assertContains(response, 'Upcoming')
