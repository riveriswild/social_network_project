import random
from itertools import chain
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=False, blank=False)
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')
    phone_number = PhoneNumberField(blank=False, null=False)
    following = models.ManyToManyField(User, related_name='folusr', blank=True)
    bio = models.TextField(default='No bio yet...')
    created = models.DateTimeField(auto_now=True)
    ignored = models.ManyToManyField(User, related_name='ignores', blank=True)
    banned = models.ManyToManyField(User, related_name='bans', blank=True)

    def __str__(self):
        return str(self.user)

    def get_my_posts(self):  # returns all posts by this user
        return self.post_set.all()

    @property
    def number_of_posts(self):  # returns the number of posts by the user
        return self.post_set.all().count()

    @property
    def get_following(self):  # returns all users the user follows
        return self.following.all()

    def get_following_users(self):  # returns the list of users the user follows
        following_list = [p for p in self.get_following()]
        return following_list

    def get_my_feed(self):  # user's feed
        users = [user for user in self.get_following()
                 if (user not in self.get_banned()
                     or user not in self.get_ignored())]  # exclude banned & ignored users
        posts = []
        qs = None
        for u in users:
            p = Profile.objects.get(user=u)
            p_posts = p.post_set.all()
            posts.append(p_posts)
        my_posts = self.post_set.all()
        posts.append(my_posts)
        if len(posts) > 0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)
        return qs

    def get_recommended_videos(self):    # recommended videos feed
        profiles = Profile.objects.all().exclude(user=self.user)  # all profiles except the user
        following_list = [p for p in self.get_following()]    # all users u follows
        banned_list = [p for p in self.get_banned()]          # all banned users
        ignored_list = [p for p in self.get_ignored()]        # all ignored users
        users = [user for user in profiles                    # users except all above
                 if (user not in banned_list
                     or user not in ignored_list
                     or user not in following_list)]
        posts = []
        qs = None
        for u in users:
            p = Profile.objects.get(user=u)
            p_posts = p.post_set.all()
            posts.append(p_posts)
            if len(posts) > 0:
                qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)
            return qs

    def get_proposals_for_following(self):      # proposals for following
        profiles = Profile.objects.all().exclude(user=self.user)
        following_list = [p for p in self.get_following()]
        available = [p.user for p in profiles if p.user not in following_list
                     or p.user not in self.get_banned()  # check if this works
                     or p.user not in self.get_ignored()]
        random.shuffle(available)
        return available[:3]

    @property
    def following_count(self):          # number of users u follows
        return self.get_following().count()

    def get_followers(self):            # get all followers
        qs = Profile.objects.all()
        followers_list = []
        for profile in qs:
            if self.user in profile.get_following():
                followers_list.append(profile)
        return followers_list

    @property
    def followers_count(self):        # number of followers
        return len(self.get_followers())

    def get_banned(self):            # banned users
        return self.banned.all()

    def get_banned_users(self):      # list of banned users
        banned_list = [p for p in self.get_banned()]
        return banned_list

    def get_ignored(self):          # ignored users
        return self.ignored.all()

    def get_ignored_users(self):    # list of ignored users
        ignored_list = [p for p in self.get_ignored()]
        return ignored_list


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    video = models.FileField(upload_to='videos', validators=[
        FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    body = models.TextField(blank=True, null=True)
    postCategory = models.ManyToManyField(Category)
    liked = models.ManyToManyField(User, default=None)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.pk)

    def get_liked(self):
        return self.liked.all()

    @property
    def like_count(self):
        return self.liked.all().count()


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Комментарий')              # add max_length
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)



# Create your models here.
