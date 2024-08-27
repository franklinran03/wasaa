from .forms import PostForm, PostResForm

def add_post_form(request):
    return {'Post_form': PostForm(), 'Res_form': PostResForm()}

