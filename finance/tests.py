from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import User, Post, Comment, ProfessionalUser, Like, Like_Comment, Save_Post, Rating_User

User = get_user_model()

class LoginTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username="user1", email="user1@example.com", password="password123")
        self.user_2 = User.objects.create_user(username="user2", email="user2@example.com", password="password123")

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(self.user_1.username, "user1")
        self.assertEqual(self.user_2.username, "user2")

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="password123")
        self.post = Post.objects.create(user=self.user, temat="Test Post", post="This is a test post.")

    def test_post_creation(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.temat, "Test Post")

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="password123")
        self.post = Post.objects.create(user=self.user, temat = "Test Post", post= "This is a test post.")
        self.comment = Comment.objects.create(user=self.user, post=self.post, comment="This is a test comment.")

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.comment, "This is a test comment.")

class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="password123")
        self.post = Post.objects.create(user= self.user, temat="Test Post", post="This is a test post.")
        self.like = Like.objects.create(user=self.user, post=self.post, if_like = True)

    def test_like_creation(self):
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.like.if_like, True)

    def test_like_count_increment(self):
        self.assertEqual(self.post.like_count, 1)
    
    def test_like_count_decrement(self):
        self.like.if_like = False
        self.like.save()
        self.assertEqual(self.post.like_count, 0)

class LikeCommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="password123")
        self.post = Post.objects.create(user = self.user, temat = "Test Post", post= "This is a test post.")
        self.comment = Comment.objects.create(user=self.user, post=self.post, comment="This is a test comment.")
        self.like_comment = Like_Comment.objects.create(user= self.user, comment=self.comment, if_like = True)

    def test_like_comment_creation(self):
        self.assertEqual(Like_Comment.objects.count(), 1)
        self.assertEqual(self.like_comment.if_like, True)

    def test_like_comment_count_increment(self):
        self.assertEqual(self.comment.like_count, 1)

    def test_like_comment_count_decrement(self):
        self.like_comment.if_like = False
        self.like_comment.save()
        self.assertEqual(self.comment.like_count, 0)

class LoginTestCase(TestCase):
    def setUp(self):
        self.user= User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")

    def test_login(self):
        login = self.client.login(username="testuser", password="password123")
        self.assertTrue(login) 

    def test_invalid_login(self):
        login = self.client.login(username="testuser", password="wrongpassword")
        self.assertFalse(login)

class SavePostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email='test@example.com', password="testpassword")
        self.post = Post.objects.create(user=self.user, temat="Test Temat", post="Test Post")

    def test_save_post_creation(self):
        save_post = Save_Post.objects.create(user=self.user, post=self.post, if_save=True)
        self.assertEqual(save_post.user, self.user)
        self.assertEqual(save_post.post, self.post)
        self.assertTrue(save_post.if_save)

    def test_save_post_str_method(self):
        save_post = Save_Post.objects.create(user=self.user, post=self.post, if_save=True)
        self.assertEqual(str(save_post), f"ID:{save_post.id}, User:{self.user.username}, Post: {self.post.id}, If Save: {save_post.if_save}")

class RatingUserModelTest(TestCase):
    def setUp(self):
        self.reviewer = User.objects.create_user(username='reviewer', email='reviewer@example.com', password='testpassword')
        self.professional_user = User.objects.create_user(username='professional', email="professional@example.com", password="testpassword")

        self.professional_profile = ProfessionalUser.objects.create(
            user= self.professional_user,
            company_name = "Test Company",
            city = "Test City", 
            specialization = "Test Specialization"
        )

    def test_rating_user_creating(self):
        rating_user = Rating_User.objects.create(
            reviewer = self.reviewer,
            professional_user = self.professional_profile,
            value = 5,
            opinion = "Great service!",
            if_used = True
        )
        self.assertEqual(rating_user.reviewer, self.reviewer)
        self.assertEqual(rating_user.professional_user, self.professional_profile)
        self.assertEqual(rating_user.value, 5)
        self.assertEqual(rating_user.opinion, "Great service!")
        self.assertTrue(rating_user.if_used)

    def test_rating_user_str_method(self):
        rating_user = Rating_User.objects.create(
            reviewer = self.reviewer,
            professional_user = self.professional_profile,
            value=5,
            opinion = "Great service!",
            if_used = True
        )
        expected_str = f"ID: {rating_user.id}, Reviewer: {self.reviewer.username}, Professional: {self.professional_profile.user.username}, value: {rating_user.value}, opinion: {rating_user.opinion}, If used: {rating_user.if_used}"
        self.assertEqual(str(rating_user), expected_str)