from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from .models import Todo

# Create your tests here.


class TodoViewSetTest(APITestCase):
    
    def setUp(self):
        
        self.user1 = User.objects.create(
            username = 'ali',
            password = 'pass1234',
        )
        self.user2 = User.objects.create(
            username = 'sara',
            password = 'pass4567',
        )

        self.todo1 = Todo.objects.create(
            name = "ali task",
            body = "this is frist test",
            assign_to = self.user1,
            status = 'SE',

        ) 
        self.todo2 = Todo.objects.create(
            name = "sara task",
            body = "this is second test",
            assign_to = self.user2,
            status = 'DN',

        ) 

        self.list_url = reverse('todo-list')
        self.detail_url = reverse('todo-detail',kwargs={'slug':self.todo1.slug})

    def test_guest_cannot_access_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code ,status.HTTP_401_UNAUTHORIZED)

    def test_guest_cannot_access_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_tasks(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.todo1.name)

    def test_create_task_sets_assignee(self):
        self.client.force_authenticate(user = self.user1)
        data = {
            'name':'new task',
            'body':'this is new task for ali',
            'priority':'H',
            'status':'SE',
            }
        response = self.client.post(self.list_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['assign_to'],self.user1)
    
    def test_cannot_edit_others_task(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(self.detail_url, {'name': 'هک شده'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(slug=self.todo1.slug).exists())