from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link news to user
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
 
    def edit(self, title, description, image):
        self.title = title
        self.description = description
        self.image = image
        self.save()
        
    def delete(self):
    # Perform any pre-delete actions here
        super().delete()
    # Perform any post-delete actions here

        
    def short_description(self):
        # Split the description into words
        words = self.description.split()
        if len(words) > 40:
            # Join the first 50 words and add "..." at the end
            return ' '.join(words[:20]) + '...'
        else:
            # If the description is already less than 50 words, return it as is
            return self.description
        
    def total_likes(self):
            return self.likes.all().count()

    def total_comments(self):
            return self.comments.all().count()
        

class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.news.title}'


class Like(models.Model):
    news = models.ForeignKey(News, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.news.title}'