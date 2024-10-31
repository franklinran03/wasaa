from django import forms
from.models import Post, UserProfile, Comment, PostRes, PostResVideo

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'res', 'res_video'] 
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control bg-dark', 'style': 'height: 100px; color: white;', 'placeholder': 'What is up?',}),
            'res': forms.FileInput(attrs={'class': 'form-control mt-3','accept': 'image/png, image/jpeg,',}),
            'res_video': forms.FileInput(attrs={'class': 'form-control mt-3','accept': 'video,',}),
        }

class PostResForm(forms.ModelForm):
    class Meta:
        model = PostRes, PostResVideo
        fields = ['resource']
        widgets = {
            'resource': forms.FileInput(attrs={'class': 'form-control mt-3 img-form', 'accept': 'image/png, image/jpeg,',}),
        }

class PostVidForm(forms.ModelForm):
    class Meta:
        model = PostResVideo
        fields = ['resource']
        widgets = {
            'resource': forms.FileInput(attrs={'class': 'form-control mt-3 vid-form', 'accept': 'video/mp4 ,',}),
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





