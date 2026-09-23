from types import SimpleNamespace

from django.test import RequestFactory, SimpleTestCase
from rest_framework.test import APIRequestFactory

from .views import PostViewSet, post_delete


class WritePermissionTests(SimpleTestCase):
    def test_delete_requires_login(self):
        request = RequestFactory().post('/post/1/delete/')
        request.user = SimpleNamespace(is_authenticated=False)
        response = post_delete(request, pk=1)
        self.assertEqual(response.status_code, 302)

    def test_delete_rejects_get_even_for_authenticated_user(self):
        request = RequestFactory().get('/post/1/delete/')
        request.user = SimpleNamespace(is_authenticated=True)
        response = post_delete(request, pk=1)
        self.assertEqual(response.status_code, 405)

    def test_anonymous_api_cannot_create_post(self):
        request = APIRequestFactory().post('/api/post/', {'title': 'test'}, format='json')
        response = PostViewSet.as_view({'post': 'create'})(request)
        self.assertIn(response.status_code, (401, 403))
