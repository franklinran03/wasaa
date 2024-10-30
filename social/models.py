from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Create your models here.
#para usuarios
class UserProfile(models.Model):
    name = models.CharField(max_length=100, blank=False)
    photo = models.ImageField(upload_to='profile_photos', blank=True) 
    banner = models.ImageField(upload_to='profile_banners', blank=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile') # relacion con usuario
    followed_users = models.ManyToManyField(User, related_name='following_profiles', blank=True) # relacion para seguidores

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return '/profile_photos/default.jpeg'  # Ruta de la imagen predeterminada

    def get_banner_url(self):
        if self.banner:
            return self.banner.url
        return '/profile_banners/default.jpeg'  # Ruta de la imagen predeterminada

# para imagenes de un post
class PostRes(models.Model):
    resource = models.FileField(upload_to='post_resources/', blank=True, null=True)

    def __str__(self):
        return self.resource.name if self.resource else 'No resource'

#para los posts
class Post(models.Model):
    pub_date = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    res = models.OneToOneField(PostRes, related_name='post_res', blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likers = models.ManyToManyField(User, related_name='liked_posts')

    def __str__(self):
        return f'Post by {self.user.username}'

    def total_likes(self):
        return self.likers.count()





#para comentarios
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'

#para seguir a otros usuarios
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE) #usuarios seguidos
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE) #usuarios seguidores

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'

    class Meta:
        unique_together = ('follower', 'followed')






