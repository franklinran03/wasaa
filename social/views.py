from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import UserProfileForm,  EditProfileForm, PostForm, CommentForm, PostResForm
from .models import UserProfile, Post, Follow, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
#pagina no encontrada
def custom_404(request, exception):
    return render(request, 'notFound.html', status=404)
    #return redirect('home')

#vista de redireccionamiento en caso de no estar autenticado
def main(req):
    return render(req, 'main.html')

#registrarse
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'profile_form': UserProfileForm(),
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrar usuario
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                )
                user.save()

                # Crear y guardar el perfil del usuario
                profile_form = UserProfileForm(request.POST, request.FILES)
                if profile_form.is_valid():
                    profile = profile_form.save(commit=False)
                    profile.user = user

                    # Establecer imágenes predeterminadas si no se proporcionan
                    if not profile.photo:
                        profile.photo = '/profile_photos/default_fgvwvu.jpg'
                    if not profile.banner:
                        profile.banner = '/profile_banners/default_lad9f9.jpg'

                    profile.save()

                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'profile_form': UserProfileForm(),
                    'error': 'User already exists',
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'profile_form': UserProfileForm(),
                'error': 'Passwords do not match',
            })

#iniciar sesion
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm,
        })      
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect',
            })
        else:
            login(request, user)
            return redirect('home')

##############################################################   

#cerrar sesion
@login_required
def signout(request):
    logout(request)
    return redirect('main')

#ver todos los posts en la pagina de home
@login_required
def home(request):
    post_list = Post.objects.all().order_by('-pub_date')
    for posts in post_list:
        posts.comment_count = posts.comments.count()
    comment_form = CommentForm()
    return render(request, 'home.html', {'posts': post_list, 'comm_form': comment_form})

#crear post
@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        post_res_form = PostResForm(request.POST, request.FILES)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()

            if post_res_form.is_valid() and 'resource' in request.FILES:
                post_res = post_res_form.save(commit=False)
                post_res.post = post
                post_res.save()
                post.res = post_res
                post.save()

            return JsonResponse({'message': 'Post created successfully!'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



#editar post
'''@login_required
def edit_post(req, username, post_id):
    if req.method == 'GET':
        user = user = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, pk=post_id, user=req.user)
        form = PostForm(instance=post)
        return render(req, 'edit_post.html', {'user': user, 'post': post, 'editingForm': form})
    else:
        try:
            post = get_object_or_404(Post, pk=post_id)
            form = PostForm(req.POST, instance=post)
            form.save()
            return redirect('home')
        except ValueError:
            return render(req, 'edit_post.html', { 'Post': post, 'editingForm': form, 'error': 'Error updating post'})'''


'''@login_required
def edit_post(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        post_res_form = PostResForm(request.POST, request.FILES, instance=post.res if post.res else None)

        if post_form.is_valid() and post_res_form.is_valid():
            post_form.save()
            
            if post_res_form.cleaned_data.get('resource'):
                # Si se proporciona una nueva imagen, guárdala y asóciala al post
                post_res = post_res_form.save(commit=False)
                post_res.post = post
                post_res.save()
                post.res = post_res
                post.save()
                
            return redirect('home')
        else:
            return render(request, 'edit_post.html', {
                'user': user,
                'post': post,
                'post_form': post_form,
                'post_res_form': post_res_form,
                'error': 'Error updating post'
            })
    else:
        post_form = PostForm(instance=post)
        post_res_form = PostResForm(instance=post.res)
        return render(request, 'edit_post.html', {
            'user': user,
            'post': post,
            'post_form': post_form,
            'post_res_form': post_res_form
        })'''

@login_required
def edit_post(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        post_res_form = PostResForm(request.POST, request.FILES, instance=post.res if post.res else None)

        if post_form.is_valid() and post_res_form.is_valid():
            post_form.save()
            
            if post_res_form.cleaned_data.get('resource'):
                post_res = post_res_form.save(commit=False)
                post_res.post = post
                post_res.save()
                post.res = post_res
                post.save()
                
            return redirect('home')
        else:
            return render(request, 'edit_post.html', {
                'user': user,
                'post': post,
                'post_form': post_form,
                'post_res_form': post_res_form,
                'error': 'Error updating post'
            })
    else:
        post_form = PostForm(instance=post)
        post_res_form = PostResForm(instance=post.res)
        return render(request, 'edit_post.html', {
            'user': user,
            'post': post,
            'post_form': post_form,
            'post_res_form': post_res_form
        })


@login_required
def delete_post_image(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if post.res:
        try:
            post.res.delete()  # Esto elimina la instancia de PostRes y el archivo de Cloudinary
            post.res = None
            post.save()
        except Exception as e:
            # Registrar el error para su posterior análisis
            print(f"Error al eliminar la imagen: {e}")
            return redirect('edit_post', username=request.user.username, post_id=post_id)
    return redirect('edit_post', username=request.user.username, post_id=post_id)



#eliminar post
@login_required
def delete_post(req, username, post_id):
    user = user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, user=req.user)
    if req.method == 'GET':
        post.delete()
        return redirect('home')

#ver detalles de post
@login_required
def post_detail(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, user=user)
    
    # Obtener el perfil asociado a ese usuario
    try:
        user_profile = user.userprofile 
    except UserProfile.DoesNotExist:
        user_profile = None

    # Manejar la creación de comentarios
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been posted successfully.')
            return redirect('post_detail', username=user.username, post_id=post.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        comment_form = CommentForm()

    # Obtener los comentarios asociados al post
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    return render(request, 'post.html', {
        'post_user': user,
        'post': post,
        'user_profile': user_profile,
        'comments': comments,
        'comment_form': comment_form,
    })

#agregar comentarios
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('home')
    return redirect('home')

#entrar al perfil del usuario que inicio sesion
@login_required
def my_profile(request, username):
    # Verificar que el usuario solicitado sea el mismo que está autenticado
    if request.user.username != username:
        return redirect('my_profile', username=request.user.username)

    # Obtener el usuario autenticado
    user = request.user

    # Obtener el perfil asociado a ese usuario
    try:
        user_profile = user.userprofile  # Accede al perfil a través del OneToOneField
    except UserProfile.DoesNotExist:
        user_profile = None

    # Obtener los posts asociados al usuario autenticado
    post_list = Post.objects.filter(user=user).order_by('-pub_date')

    # Obtener las listas de seguidos y seguidores
    # Obtener los usuarios que el usuario autenticado está siguiendo
    followed_users = Follow.objects.filter(follower=user).select_related('followed')
    # Obtener los seguidores del usuario autenticado
    followers = Follow.objects.filter(followed=user).select_related('follower')

    # Manejar el formulario de edición de perfil
    if request.method == 'POST' and 'profile-submit' in request.POST:
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('my_profile', username=user.username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = EditProfileForm(instance=user_profile)

    # Pasar el usuario, el perfil, los posts y las listas de seguidos y seguidores al contexto del template
    context = {
        'pruser': user,
        'posts': post_list,
        'user_profile': user_profile,
        'followed_users': [follow.followed for follow in followed_users],  # Convertir a una lista de usuarios seguidos
        'followers': [follow.follower for follow in followers],  # Convertir a una lista de seguidores
        'profile_form': profile_form,  # Agregar el formulario al contexto
    }

    return render(request, 'profile.html', context)

#ingresar al perfil de cualquier usuario
@login_required
def profile(request, username):
    # Obtener el usuario cuyo perfil se está visualizando
    user = get_object_or_404(User, username=username)
    
    # Obtener el perfil asociado a ese usuario
    try:
        user_profile = user.userprofile  # Accede al perfil a través del OneToOneField
    except UserProfile.DoesNotExist:
        user_profile = None

    # Obtener los posts asociados al usuario cuyo perfil se está visualizando
    post_list = Post.objects.filter(user=user).order_by('-pub_date')

    # Obtener los usuarios que sigue el usuario cuyo perfil se está visualizando
    followed_users = user_profile.followed_users.all() if user_profile else []

    # Obtener los seguidores del usuario cuyo perfil se está visualizando
    followers = Follow.objects.filter(followed=user).select_related('follower')

    # Verificar si el usuario autenticado está siguiendo al usuario del perfil
    is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

    # Pasar el usuario, el perfil, los posts y las listas de seguidos y seguidores al contexto del template
    context = {
        'pruser': user,
        'posts': post_list,
        'user_profile': user_profile,
        'followed_users': followed_users,
        'followers': [follow.follower for follow in followers],  # Convertir a una lista de usuarios
        'is_following': is_following,
    }

    return render(request, 'profile.html', context)

#editar perfil
@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('my_profile', username=user.username)
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        profile_form = EditProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'user': user,
    })

#cambio de contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('edit_profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form,})

#eliminar usuario y perfil
@login_required
def delete_user(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        # Verificar si el usuario autenticado es el mismo que se va a eliminar
        if request.user == user:
            # Verificar las credenciales adicionales antes de eliminar
            username = request.POST['username']
            password = request.POST['password']

            # Autenticar al usuario nuevamente para confirmar la eliminación
            user_to_delete = authenticate(username=username, password=password)

            if user_to_delete is not None and user_to_delete == user:
                # Eliminar el usuario
                user.delete()
                messages.success(request, 'Your account has been deleted.')
                return redirect('logout')  # Redirigir a la página de logout o a donde desees
            else:
                messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'delete_user.html', {'user': user})

#dar like y dislike
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user  # Asumiendo que tienes autenticación de usuario

    if user in post.likers.all():
        # El usuario ya dio like, entonces remueve el like
        post.likers.remove(user)
    else:
        # El usuario no ha dado like aún, entonces añade el like
        post.likers.add(user)
    total_likes = post.likers.count()

    # Devuelve un JsonResponse con el nuevo total de likes
    return JsonResponse({'total_likes': total_likes})


    #return redirect('post_detail', username=Post.user.username, post_id=Post.pk)

#seguir usuarios
@login_required
def follow_user(request, username):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=username)

        # Evitar que un usuario se siga a sí mismo
        if request.user == user_to_follow:
            return redirect('profile', username=username)

        # Verificar si ya sigue al usuario
        if Follow.objects.filter(follower=request.user, followed=user_to_follow).exists():
            return redirect('profile', username=username)

        # Crear la relación de seguimiento
        follow = Follow(follower=request.user, followed=user_to_follow)
        follow.save()

        return redirect('profile', username=username)
    return redirect('profile', username=username)

#dejar de seguir usuarios
@login_required
def unfollow_user(request, username):
    if request.method == 'POST':
        user_to_unfollow = get_object_or_404(User, username=username)

        # Verificar si existe la relación de seguimiento
        follow = Follow.objects.filter(follower=request.user, followed=user_to_unfollow)
        if not follow.exists():
            return redirect('profile', username=username)

        # Eliminar la relación de seguimiento
        follow.delete()

        return redirect('profile', username=username)
    return redirect('profile', username=username)





