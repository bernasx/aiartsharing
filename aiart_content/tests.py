from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest import skip
from aiart_content.models import Post

import time


class PostTests(TestCase):

    # Everything get flushed after the transaction finishes so it's fine to test things together.
    # setUp and tearDown get called before every test
    def setUp(self):
        self.t1 = time.perf_counter() # save the time when we are setting up so we can measure how long the test took
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", username="normaluser", password="foo")
        user.save()

    def test_create_1_post(self):
        User = get_user_model()
        user = User.objects.get(email="normal@user.com")
        for i in range(0,1):
            post = Post.objects.create(title=f'title{i}',user=user)
        self.assertEqual(len(Post.objects.all()),1)

    def test_create_10_posts(self):
        User = get_user_model()
        user = User.objects.get(email="normal@user.com")
        for i in range(0,10):
            Post.objects.create(title=f'title{i}',user=user)
        self.assertEqual(len(Post.objects.all()),10)

    def test_create_100_posts(self):
        User = get_user_model()
        user = User.objects.get(email="normal@user.com")
        for i in range(0,100):
            Post.objects.create(title=f'title{i}',user=user)
        self.assertEqual(len(Post.objects.all()),100)

    def test_create_1k_posts(self):
        User = get_user_model()
        user = User.objects.get(email="normal@user.com")
        for i in range(0,1000):
            Post.objects.create(title=f'title{i}',user=user)
        self.assertEqual(len(Post.objects.all()),1000)

    def test_create_10k_posts(self):
        User = get_user_model()
        user = User.objects.get(email="normal@user.com")
        for i in range(0,10000):
            Post.objects.create(title=f'title{i}',user=user)
        self.assertEqual(len(Post.objects.all()),10000)
    
    def test_create_100k_posts(self):
        User = get_user_model()
        user = User.objects.get(email="normal@user.com")
        for i in range(0,100000):
            Post.objects.create(title=f'title{i}',user=user)
        self.assertEqual(len(Post.objects.all()),100000)

    @skip 
    def test_create_1m_posts(self):

        User = get_user_model()
        user = User.objects.get(email="normal@user.com")

        # generator function for posts
        def generatePosts():
            for i in range(0,1000000):
                yield Post(title=f'title{i}',user=user)
                
        
        posts = generatePosts()
        Post.objects.bulk_create(posts)
        self.assertEqual(len(Post.objects.all()),1000000)

    def tearDown(self):
        self.t2 = time.perf_counter() # time after it finished
        print(f'\n {str(Post.objects.all().count())} {str(round(self.t2-self.t1,2))}s') # print test time and current element count in a readable format