from django import forms
from.models import Post, UserProfile, Comment, PostRes

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'res'] 
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control bg-dark', 'style': 'height: 100px; color: white;', 'placeholder': 'What is up?', 'required': False,}),
            'res': forms.FileInput(attrs={'class': 'form-control mt-3','accept': 'image/png, image/jpeg, video/mp4, video/mkv',}),
        }

class PostResForm(forms.ModelForm):
    class Meta:
        model = PostRes
        fields = ['resource']
        widgets = {
            'resource': forms.FileInput(attrs={'class': 'form-control mt-3', 'accept': 'image/png, image/jpeg, video/mp4, video/mkv',}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name',]  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your name',}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'photo', 'banner'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your name',}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'formFilePhoto', 'accept': 'image/png, image/jpeg, image/jpg',}),
            'banner': forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'formFileBanner', 'accept': 'image/png, image/jpeg, image/jpg',}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark border-dark opacity-10 reply', 
                'style': 'height: 50px; color: white; outline: none; box-shadow: none; resize: none;', 
                'placeholder': 'Post your reply',
                'oninput': 'autoExpand(this)',
                }),
        }





