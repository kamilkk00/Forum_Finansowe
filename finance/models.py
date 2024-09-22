from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver


# Creating a SQL table for profile along with information about whether it is a professional profile (automatically becomes a professional profile upon creation)
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
    if_professional = models.BooleanField(default=False)
    
    def __str__(self):
        return f"ID: {self.id}, User: {self.username}, e-mail: {self.email}, password: {self.password}, if professional: {self.if_professional}"

# SQL table for posts
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="POST")
    temat = models.CharField(max_length=500)
    post = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(default=timezone.now)

    CATEGORY_CHOICES = [ 
        ('zakladanie_firmy', 'Zakładanie firmy'),
        ('finance_inwestycje', 'Finanse i inwestycje'),
        ('marketing_sprzedaz', 'Marketing i sprzedaż'),
        ('zarządzanie_operacje', 'Zarządzanie i operacje'),
        ('prawo_regulacje', 'Prawo i regulacje'),
        ('rozwoj_osobisty', 'Rozwój osobisty i networking'),
        ('inne', 'Inne')
    ]    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='inne')
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"ID: {self.id}, User: {self.user.username}, temat: {self.temat} post: {self.post}, timestamp: {self.timestamp}, category:{self.category}, likes:{self.like_count} "
    
# Database for comments
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    comment = models.CharField(max_length=3000)
    timestamp = models.DateTimeField(default=timezone.now)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"ID: {self.id}, User: {self.user.username}, post: {self.post.id}, comment: {self.comment}, likes:{self.like_count}, timestamp: {self.timestamp}"

# SQL table for professional users
class ProfessionalUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="professional_profile")
    company_name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length= 255)
    specialization = models.CharField(max_length=255)
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    availability = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.URLField(blank = True)
    social_media = models.URLField(blank=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    certifications = models.TextField(blank=True)

    def __str__(self):
        return f"ID: {self.id}, User: {self.user.username}, Specialization: {self.specialization}, City: {self.city}"
    
# SQL table for post likes
class Like(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "post_like")
    if_like = models.BooleanField(default=True)
    
    def __str__(self):
        return f"ID: {self.id}, User: {self.user.username}, Post: {self.post.id}, if like: {self.if_like}"
    
# Logic for counting likes under posts
@receiver(pre_save, sender = Like)
def before_like_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Like.objects.get(pk=instance.pk)
        if old_instance.if_like != instance.if_like:
            if instance.if_like:
                instance.post.like_count += 1
            else:
                instance.post.like_count -= 1
            instance.post.save()

# Logic for updating like 
@receiver(post_save, sender=Like)
def update_like_count_on_save(sender, instance, created, **kwargs): 
    if created: 
        instance.post.like_count = instance.post.post_like.filter(if_like=True).count()
        instance.post.save()

# Logic for updating like after delete
@receiver(post_delete, sender=Like)
def update_like_count_on_delete(sender, instance, **kwargs):
    instance.post.like_count = instance.post.post_like.filter(if_like=True).count()
    instance.post.save()

# SQL table for likes under comments
class Like_Comment(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_comment")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    if_like = models.BooleanField(default=True)

    def __str__(self):
        return f"ID: {self.id}, User: {self.user.username}, Comment {self.comment.id}, if like: {self.if_like}"


# Logic for counting likes under comments 
@receiver(pre_save, sender= Like_Comment)
def before_comment_like_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Like_Comment.objects.get(pk=instance.pk)
        if old_instance.if_like != instance.if_like:
            if instance.if_like:
                instance.comment.like_count +=1 
            else:
                instance.comment.like_count -= 1
            instance.comment.save()

@receiver(post_save, sender=Like_Comment)
def update_comment_like_count_on_save(sender, instance, created, **kwargs):
    if created:
        instance.comment.like_count = instance.comment.likes.filter(if_like=True).count()
        instance.comment.save()

@receiver(post_delete, sender=Like_Comment)
def update_comment_like_count_on_delete(sender, instance, **kwargs):
    instance.comment.like_count = instance.comment.likes.filter(if_like=True).count()
    instance.comment.save()

# SQL table for saving posts
class Save_Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="save_post")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="save_post")
    if_save = models.BooleanField(default=True)

    def __str__(self):
        return f"ID:{self.id}, User:{self.user.username}, Post: {self.post.id}, If Save: {self.if_save}"
    
# SQL table for rating professional users
class Rating_User(models.Model):
    id = models.AutoField(primary_key=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="give_rate_professional")
    professional_user = models.ForeignKey(ProfessionalUser, on_delete = models.CASCADE, related_name="give_rate_professional")
    value = models.PositiveSmallIntegerField()
    opinion = models.CharField(max_length=1000)
    if_used = models.BooleanField(default=False)

    def __str__(self):
        return f"ID: {self.id}, Reviewer: {self.reviewer.username}, Professional: {self.professional_user.user.username}, value: {self.value}, opinion: {self.opinion}, If used: {self.if_used}"