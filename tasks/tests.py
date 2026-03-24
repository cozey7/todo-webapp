from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskModelTests(TestCase):
	def test_task_str_returns_title(self):
		user = User.objects.create_user(username='alice', password='pw12345')
		task = Task.objects.create(
			user=user,
			title='Buy groceries',
			description='Milk and eggs',
			due_date=timezone.now().date(),
		)

		self.assertEqual(str(task), 'Buy groceries')

	def test_task_completed_defaults_to_false(self):
		user = User.objects.create_user(username='bob', password='pw12345')
		task = Task.objects.create(
			user=user,
			title='Read chapter 1',
			due_date=timezone.now().date(),
		)

		self.assertFalse(task.completed)


class TaskAPITests(APITestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', password='pass12345')
		self.user2 = User.objects.create_user(username='user2', password='pass12345')
		self.list_url = reverse('task-list')
		self.today_url = reverse('task-today')

	def test_task_list_requires_authentication(self):
		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_create_task_sets_user_to_authenticated_user(self):
		self.client.force_authenticate(user=self.user1)
		payload = {
			'title': 'Finish homework',
			'description': 'Math exercises',
			'due_date': timezone.now().date().isoformat(),
			'completed': False,
		}

		response = self.client.post(self.list_url, payload, format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Task.objects.count(), 1)
		created_task = Task.objects.first()
		self.assertEqual(created_task.user, self.user1)

	def test_list_only_returns_tasks_for_current_user(self):
		today = timezone.now().date()
		Task.objects.create(user=self.user1, title='u1 task', due_date=today)
		Task.objects.create(user=self.user2, title='u2 task', due_date=today)

		self.client.force_authenticate(user=self.user1)
		response = self.client.get(self.list_url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]['title'], 'u1 task')

	def test_today_endpoint_returns_only_today_tasks(self):
		today = timezone.now().date()
		tomorrow = today + timedelta(days=1)

		Task.objects.create(user=self.user1, title='today task', due_date=today)
		Task.objects.create(user=self.user1, title='tomorrow task', due_date=tomorrow)

		self.client.force_authenticate(user=self.user1)
		response = self.client.get(self.today_url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]['title'], 'today task')
