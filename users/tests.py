from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestCreateQuizView(TestCase):
    def test_anonymous_cannot_create_edit_profile(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, "/login/?next=/profile/")
        response = self.client.get(reverse("view-profile",args=['myprofile']))
        self.assertRedirects(response, "/login/?next=/profile/myprofile/")
    def test_logged_in_user_redirects(self):
        user=User.objects.create(username="Atufaaa")
        self.client.force_login(user=user)
        response = self.client.get(reverse("login"),follow_redirects=True)
        self.assertRedirects(response, "/")
