from audioop import reverse
from collections import Counter
from gettext import translation
import re
import sys
from django.forms import ValidationError
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib import messages

from django.db.models import Count
from django.db.models import Q

from django.conf import settings

# Formularios de autenticación. Registro y login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

# Vista de cambio de contraseña
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.password_validation import validate_password

# Formulario de registro de usuario personalizado
from .forms import CustomUserCreationForm, UserEditForm, UserAndProfileForm

# Iniciar sesión
from django.contrib.auth import login

# Cerrar sesión
from django.contrib.auth import logout

# Excepcione de integridad de datos
from django.db.utils import IntegrityError

# Modelo de usuario
from django.contrib.auth.models import User
# Modelo de perfil de usuario
from .models import BlogPost, BooksSection, BooksSectionBook, Follow, ListBook, ListBookBook, Notification, Post, Comment, Profile, GroupReaders, MemberGroup, Resenya, SolicitudWriter

# Validación de contraseña
from django.contrib.auth import password_validation

# Redirección
from django.shortcuts import redirect

from django.utils.translation import activate, get_language_info, gettext as _

# Get object or 404
from django.shortcuts import get_object_or_404

# Fecha y hora
from datetime import datetime
from django.utils import timezone

# requests para API
import requests
import json

# No permitir acceso a usuarios no autenticados
from django.contrib.auth.decorators import login_required

# Token api rest
from rest_framework.authtoken.models import Token

# Vista de inicio

def index(request):
    if request.method == 'GET':
        # Si el usuario está autenticado

        #Definir tiempo de inicio y fin de los posts que se van a obtener
        start_date = timezone.now() - timezone.timedelta(days=7)
        end_date = timezone.now()

        #Obtener post
        posts_rango = Post.objects.filter(created_at__range=(start_date, end_date), content__contains='#')

        #Obtener todos los hashtags de los posts obtenidos anteriormente
        hashtags = []
        for post in posts_rango:
            post_hashtags = re.findall(r'#(\w+)', post.content)
            hashtags.extend(post_hashtags)

        #Obtener lista de los 5 hashtags más comunes
        popular_hashtags = Counter(hashtags).most_common(5)

        if request.user.is_authenticated:
            return render(request, 'index.html', {
                'popular_hashtags': popular_hashtags,
            })
        # Si el usuario no está autenticado
        else:
            return render(request, 'indexNoAuth.html', {})

# Vista de inicio de sesión

def signin(request):
    # Si el método es GET, devolver el formulario de inicio de sesión
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm(),
        })
    elif request.method == 'POST':
        # Comprobar que el usuario existe
        try:
            # Obtener el usuario
            user = User.objects.get(username=request.POST['username'])
            # Comprobar que la contraseña es correcta
            if user.check_password(request.POST['password']):
                # Iniciar sesión
                login(request, user)

                # Almacenar token en cookie
                response = redirect('/')
                response.set_cookie('tokenUser', request.user.auth_token.key)
                response.set_cookie('username', request.user.username)
                return response

            else:
                # Si la contraseña es incorrecta
                return render(request, 'login.html', {
                    'form': AuthenticationForm(),
                    'error': 'Contraseña incorrecta'
                })
        # Si el usuario no existe
        except User.DoesNotExist:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                'error': 'Usuario no registrado'
            })


# Vista de search
def search(request):
    if request.method == 'GET':
        parametro = request.GET['q']
        # Si el usuario está autenticado
        if request.user.is_authenticated:

            return render(request, 'busqueda.html', {
                'query': parametro,
            })
        # Si el usuario no está autenticado
        else:
            return render(request, 'login.html', {})

# Vista de registro


def signup(request):
    # Si el método es GET, devolver el formulario de registro
    if request.method == 'GET':
        return render(request, 'register.html', {
            'form': CustomUserCreationForm(),
        })
    # Respuesta del formulario de registro. Registro de usuario
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Validar la contraseña con los validadores definidos en settings
                validate_password(request.POST['password1'])
            except ValidationError as e:
                return render(request, 'register.html', {
                    'form': CustomUserCreationForm(),
                    'error': e.messages[0],
                })
            '''
            # Validar sintaxis de la contraseña
            if len(request.POST['password1']) < 8:
                return render(request, 'register.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'La contraseña debe tener al menos 8 caracteres'})
            if request.POST['password1'].isalpha():
                return render(request, 'register.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'La contraseña debe tener al menos un número'})
            if request.POST['password1'].isnumeric():
                return render(request, 'register.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'La contraseña debe tener al menos una letra'})
            if request.POST['password1'].islower():
                return render(request, 'register.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'La contraseña debe tener al menos una letra mayúscula'})
            if request.POST['password1'].isupper():
                return render(request, 'register.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'La contraseña debe tener al menos una letra minúscula'})
            if request.POST['password1'].isalnum():
                return render(request, 'register.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'La contraseña debe tener al menos un carácter especial'})
            '''
            try:
                # Crear usuario
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                )
                # Guarda el usuario en la base de datos
                user.save()

                # Crear perfil de usuario
                profile = Profile.objects.create(
                    user=user,
                )

                # Crear listas de libros
                leidos = ListBook(type_list='leidos', user=user)
                leidos.save()
                leyendo = ListBook(type_list='leyendo', user=user)
                leyendo.save()
                por_leer = ListBook(type_list='por_leer', user=user)
                por_leer.save()

                # Iniciar sesión
                login(request, user)

                # Crear token para la API
                userToken = Token.objects.create(user=user)

                # Almacenar token en cookie
                response = redirect('/')
                response.set_cookie('tokenUser', request.user.auth_token.key)
                response.set_cookie('username', request.user.username)
                return response
            except IntegrityError:
                return render(request, 'register.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'Username ya registrado'
                })
        else:
            return render(request, 'register.html', {
                'form': CustomUserCreationForm(),
                'error': 'Las contraseñas no coinciden'
            })

    return render(request, 'register.html', {
        'form': CustomUserCreationForm(),
    })


@login_required(login_url='/login')
def lists(request, username):
    # Obtener el usuario
    user = User.objects.filter(username=username).first()
    # Comprobar que el usuario es el mismo que el usuario autenticado
    if user == request.user:
        return render(request, 'listas.html', {
            'user': user,
        })
    else:
        return render(request, '404.html', {})


# Vista de cierre de sesión
@login_required(login_url='/login')
def signout(request):
    # Cerrar sesión
    logout(request)
    return redirect('index')

# Vista de perfil de usuario


@login_required(login_url='/login')
def user(request, username):
    # Obtener el usuario
    user = User.objects.filter(username=username).first()
    profile = Profile.objects.filter(user=user).first()
    groups = MemberGroup.objects.filter(user=user)

    for group in groups:
        group.name = GroupReaders.objects.filter(
            id=group.group_id).first().name
        group.id = GroupReaders.objects.filter(id=group.group_id).first().id

    # Seguido por el usuario actual
    seguido = Follow.objects.filter(
        follower=request.user, following=user).first()

    # Si el usuario no existe
    if user is None:
        return render(request, '404.html', {})
    # Si el usuario existe
    else:
        return render(request, 'user.html', {
            'user': user,
            'profile': profile,
            'seguido': seguido,
            'groups': groups,
        })

# Vista de edición de perfil de usuario


@login_required(login_url='/login')
def edituser(request):
    if request.method == 'GET':
        # Obtener el usuario
        user = User.objects.filter(username=request.user.username).first()
        profile = Profile.objects.filter(user=user).first()

        # Si el usuario no existe
        if user is None:
            return render(request, '404.html', {})
        # Si el usuario existe
        else:
            # Cargar formulario con los datos del usuario por defecto
            form = UserAndProfileForm()
            form.fields['username'].initial = user.username
            form.fields['first_name'].initial = user.first_name
            form.fields['pic'].initial = profile.pic
            form.fields['email'].initial = user.email
            form.fields['bio'].initial = profile.bio
            form.fields['location'].initial = profile.location

            return render(request, 'edituser.html', {
                'user': user,
                'profile': profile,
                'form': form
            })

    if request.method == 'POST':
        # Obtener el usuario
        user = User.objects.filter(username=request.user.username).first()
        profile = Profile.objects.filter(user=user).first()

        # Si el usuario no existe
        if user is None:
            return render(request, '404.html', {})

        # Obtener el nuevo nombre de usuario del formulario
        username_nuevo = request.POST.get('username', '').lower().strip()

        # Verificar si se proporcionó un nuevo nombre de usuario
        if not username_nuevo:
            error = 'El nombre de usuario es requerido'
            return render(request, 'edituser.html', {
                'user': user,
                'profile': profile,
                'form': UserAndProfileForm(),
                'error': error
            })

        # Verificar si el nuevo nombre de usuario ya existe y no es el mismo usuario actual
        usuario_existente = User.objects.filter(username=username_nuevo).first()
        if usuario_existente and usuario_existente != user:
            error = 'Nombre de usuario ya registrado'
            return render(request, 'edituser.html', {
                'user': user,
                'profile': profile,
                'form': UserAndProfileForm(),
                'error': error
            })

        try:
            # Actualizar datos del usuario
            user.username = username_nuevo
            user.first_name = request.POST.get('first_name', '').strip()
            user.email = request.POST.get('email', '').strip()
            profile.bio = request.POST.get('bio', '').strip()
            profile.location = request.POST.get('location', '').strip()

            # Verificar si se proporcionó una nueva imagen de perfil
            if 'pic' in request.FILES:
                # Verificar si se marcó la opción de limpiar la imagen
                if request.POST.get('pic-clear') == "on":
                    #Eliminar imagen de perfil
                    profile.pic.delete()
                    profile.pic = None
                else:
                    profile.pic = request.FILES['pic']

            # Guardar cambios
            user.save()
            profile.save()
        except:
            error = 'Inténtalo de nuevo más tarde. Error: ' + str(sys.exc_info()[0])
            return render(request, 'edituser.html', {
                'user': user,
                'profile': profile,
                'form': UserAndProfileForm(),
                'error': error
            })

        return redirect('user', username=user.username)

# Vista de explorar

@login_required(login_url='/login')
def explore(request):
    '''
    # Obtener secciones
    secciones = BooksSection.objects.all()
    #Añadir libros a cada sección
    for seccion in secciones:
        seccion.libros = BooksSectionBook.objects.filter(book_section=seccion)

    print(secciones[0].libros[0])

    secciones_json = json.dumps([{'id': s.id, 'title': s.title, 'libros': [{'id': l.book} for l in s.libros]} for s in secciones])
    '''
    return render(request, 'explore.html', {
        #'secciones': secciones_json
    })


# Posts acciones
# Vista para nuevo post
@login_required(login_url='/login')
def newpost(request):
    if request.method == 'POST':
        fechaActual = datetime.now()
        # Crear post
        post = Post.objects.create(
            content=request.POST['contenido'],
            created_at=fechaActual,
            author=request.user
        )

        # Guardar post en la base de datos
        post.save()
        return redirect('post', post_id=post.id)


#Vista crear post formulario
@login_required(login_url='/login')
def newPostForm(request):
    user = request.user
    return render(request, 'newPostForm.html', {
        'user': user
    })


# Vista para ver un post según su id

def post(request, post_id):
    # Obtener el post
    post = Post.objects.get(id=post_id)
    # Agregar al post el numero de comentarios
    post.num_comments = Comment.objects.filter(post=post).count()

    # Si el post es del usuario logueado se añader el atributo is_owner
    if post.user == request.user:
        post.is_owner = True
    else:
        post.is_owner = False

    # Obtener los comentarios del post
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    # Añadir a cada comentario si el usuario logueado es su autor
    for comment in comments:
        if comment.user == request.user:
            comment.is_owner = True
        else:
            comment.is_owner = False

    # Si el post no existe
    if post is None:
        return render(request, '404.html', {})
    # Si el post existe
    else:
        return render(request, 'post.html', {
            'post': post,
            'comments': comments
        })


# Vista para hashtag
@login_required(login_url='/login')
def hashtag(request, hashtag):
    hashtag_regex = r'\b{}\b'.format(hashtag)

    # Filtrar los posts que contengan el hashtag
    posts = Post.objects.filter(content__regex=hashtag_regex)

    # Si el hashtag no existe
    if posts is None:
        return render(request, '404.html', {})
    # Si el hashtag existe
    else:
        return render(request, 'hashtag.html', {
            'hashtag': hashtag,

        })

# Vista para eliminar un post


@login_required(login_url='/login')
def deletepost(request, post_id):
    # Obtener el post
    post = Post.objects.get(id=post_id)
    # Si el post no existe
    if post is None:
        return render(request, '404.html', {})
    # Si el post existe
    else:
        # Si el usuario es el autor del post
        if post.user == request.user:
            # Eliminar post
            post.delete()
            return redirect('user', username=request.user.username)
        # Si el usuario no es el autor del post
        else:
            return render(request, '404.html', {})

# Vista para crear un comentario


@login_required(login_url='/login')
def newcomment(request, post_id):
    if request.method == 'POST':
        # Crear comentario
        try:
            comment = Comment.objects.create(
                content=request.POST['contenido'],
                user=request.user,
                post=Post.objects.get(id=post_id)
            )

            # Guardar comentario en la base de datos
            comment.save()
            # Crear notificacion
            createNotification(comment.post.user,
                               request.user, 2, comment.post)
        except:
            return render(request, '404.html', {})
        return redirect('post', post_id=post_id)

# Vista para eliminar un comentario


def deletecomment(request, comment_id):
    # Obtener el comentario
    comment = Comment.objects.get(id=comment_id)
    # Si el comentario no existe
    if comment is None:
        return render(request, '404.html', {})
    # Si el comentario existe
    else:
        # Si el usuario es el autor del comentario
        if comment.user == request.user:
            # Eliminar comentario
            comment.delete()
            return redirect('post', post_id=comment.post.id)
        # Si el usuario no es el autor del comentario
        else:
            return render(request, '404.html', {})

# Vista para seguir a un usuario


def followOrUnfollow(request, username):
    # Recuperar el usuario al que se va a seguir/dejar de seguir
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Devolver un error 404 si el usuario no existe
        return render(request, '404.html', {})

    # Verificar que el usuario no se esté siguiendo a sí mismo
    if user == request.user:
        return render(request, '404.html', {})

    # Seguir o dejar de seguir al usuario
    if Follow.objects.filter(follower=request.user, following=user).exists():
        # Si el usuario ya está siendo seguido, eliminar el seguimiento
        Follow.objects.filter(follower=request.user, following=user).delete()
    else:
        # Si el usuario no está siendo seguido, crear un nuevo seguimiento
        follow = Follow.objects.create(follower=request.user, following=user)
        # Crear notificación
        createNotification(
            to_user=user, from_user=request.user, notification_type='3')

    # Mostrar la página del usuario después de seguir/dejar de seguir
    return redirect('user', username=username)

# Vista para ver los seguidores de un usuario


@login_required(login_url='/login')
def followers(request, username):
    # Si el usuario no es el mismo que el que está logueado
    if username != request.user.username:
        # Devolver un error 404
        return render(request, '404.html', {})

    # Recuperar el usuario
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Devolver un error 404 si el usuario no existe
        return render(request, '404.html', {})

    # Recuperar los seguidores del usuario
    seguidores = Follow.objects.filter(following=user).order_by('-created_at')
    # Recuperar los seguidos por el usuario
    seguidos = Follow.objects.filter(follower=user).order_by('-created_at')

    for seguidor in seguidores:
        seguidor.username = seguidor.follower.username

    for seguido in seguidos:
        seguido.username = seguido.following.username

    # Mostrar la página de seguidores
    return render(request, 'followers.html', {
        'user': user,
        'seguidores': seguidores,
        'seguidos': seguidos
    })

# Vista para ver las notificaciones


@login_required(login_url='/login')
def notifications(request):
    notificaciones = Notification.objects.filter(
        to_user=request.user).order_by('-created_at')
    print(notificaciones)
    # Mostrar la página de notificaciones
    return render(request, 'notifications.html', {
        'notificaciones': notificaciones
    })

# Vista para ver un libro según su isbn

@login_required(login_url='/login')
def book(request, id):
    if request.method == 'GET':
        # Si el libro no existe
        if book is None:
            return render(request, '404.html', {})
        # Si el libro existe
        else:
            #Obtener en que lista está el libro
            libros_listas_usuario = ListBookBook.objects.filter(book=id, list_book__user=request.user)
            libro_en_por_leer = False
            libro_en_leyendo = False
            libro_en_leidos = False
            for libro_lista_usuario in libros_listas_usuario:
                if libro_lista_usuario.list_book.type_list == 'por_leer':
                    libro_en_por_leer = True
                if libro_lista_usuario.list_book.type_list == 'leyendo':
                    libro_en_leyendo = True
                if libro_lista_usuario.list_book.type_list == 'leidos':
                    libro_en_leidos = True


            return render(request, 'libro.html', {
                'libro_en_por_leer': libro_en_por_leer,
                'libro_en_leyendo': libro_en_leyendo,
                'libro_en_leidos': libro_en_leidos,
                'id': id,
            })

# Vista para añadir un libro a una lista o eliminarlo
@login_required(login_url='/login')
def addOrRemoveBook(request):

    #Obtener id del libro
    id = request.POST.get("libro_id")

    #Añadir libro a la lista
    # Obtener lista de usuario
    list_book_type = request.POST.get("lista")
    if list_book_type in ('por_leer', 'leyendo', 'leidos'):
        list_book, _ = ListBook.objects.get_or_create(user=request.user, type_list=list_book_type)
    else:
        return render(request, '404.html', {})

    #Comprobar si el libro ya está en la lista
    if ListBookBook.objects.filter(list_book=list_book, book=request.POST.get("libro_id")).exists():
        #Eliminar libro de la lista
        ListBookBook.objects.filter(list_book=list_book, book=request.POST.get("libro_id")).delete()
    else: 
        # Añadir libro a la lista
        ListBookBook.objects.create(
            list_book=list_book,
            book=request.POST.get("libro_id")
        )

    #Redirigir a la página del libro
    if id is not None and id != '':
        return redirect('book', id=id)
    else:
        return render(request, '404.html', {})

# Vista para ver los grupos
@login_required(login_url='/login')
def groups(request):
    # Obtener los grupos
    grupos = GroupReaders.objects.all()
    # Añadir numero de miembros a cada grupo
    for grupo in grupos:
        grupo.numMembers = MemberGroup.objects.filter(group=grupo).count()
        grupo.isMember = MemberGroup.objects.filter(
            group=grupo, user=request.user).exists()

    # Si no hay grupos
    if grupos is None:
        return render(request, '404.html', {})
    # Si hay grupos
    else:
        return render(request, 'grupos.html', {
            'grupos': grupos,
        })


def rulesGroups(request):
    return render(request, 'gruposRules.html', {})


@login_required(login_url='/login')
def group(request, id):
    # Obtener grupo
    grupo = GroupReaders.objects.get(id=id)

    # Comprobar si el usuario no es miembro del grupo
    if not MemberGroup.objects.filter(group=grupo, user=request.user).exists():
        return render(request, '404.html', {})
    else:
        # Si el usuario es miembro del grupo
        # Obtener miembros del grupo
        miembros = MemberGroup.objects.filter(group=grupo)
        # Obtener posts del grupo
        posts = Post.objects.filter(group=grupo).order_by('-created_at')

        # Si el grupo no existe
        if grupo is None:
            return render(request, '404.html', {})
        # Si el grupo existe
        else:
            return render(request, 'grupo.html', {
                'grupo': grupo,
                'miembros': miembros,
                'posts': posts,
            })

# Funcion para unirse o salir de un grupo


def joinOrLeaveGroup(request, id):
    # Obtener grupo
    grupo = GroupReaders.objects.get(id=id)
    # Si el usuario no es miembro del grupo
    if not MemberGroup.objects.filter(group=grupo, user=request.user).exists():
        # Crear miembro del grupo
        member = MemberGroup.objects.create(group=grupo, user=request.user)
        # Redirigir a la página del grupo
        return redirect('group', id=id)

    else:
        # Eliminar miembro del grupo
        MemberGroup.objects.filter(group=grupo, user=request.user).delete()
        # Redirigir a la página de grupos
        return redirect('groups')

# Vista para crear cerrar sesión después de cambiar la contraseña


@login_required
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Actualizar la sesión del usuario con la nueva contraseña
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('/')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {
        'form': form,
    })

@login_required
def PasswordChangeDoneView(request):
    # Cerrar sesión
    logout(request)
    # Redirigir a la página de inicio de sesión
    return redirect('/')


# Vista para eliminar la cuenta
@login_required
def deleteuser(request, username):
    # Comprobar si el usuario es el mismo que el que está logueado
    if username != request.user.username:
        # Devolver un error 404
        return render(request, '404.html', {})
    # Si el usuario es el mismo que el que está logueado
    else:
        # Obtener el usuario
        user = User.objects.get(username=username)
        # Cerrar sesión
        user.delete()

        # Redirigir a la página de inicio de sesión
        return redirect('/')


def blog(request):
    BlogPosts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog/blog.html', {
        'blogposts': BlogPosts,
    })


def postBlog(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, 'blog/postBlog.html', {
        'blogpost': post,
    })

# Vista para crear solicitud el perfil de escritor
def requestWriter(request, username):
    # Comprobar si el usuario no es el mismo que el que está logueado
    if username != request.user.username:
        # Devolver un error 404
        print("No es el mismo")
        return render(request, '404.html', {})
    # Si el usuario es el mismo que el que está logueado
    else:
        # Crear solicitud
        requestWriter = SolicitudWriter.objects.create(
            user=request.user,
            resuelta=False
        )
        # Guardar solicitud en la base de datos
        requestWriter.save()
        # Redirigir a la página de editar perfil
        return redirect('edituser')


#Vista para ver ranking de usuarios
@login_required(login_url='/login')
def ranking(request):
    # Obtener usuarios con más reseñas (limite 10)
    ranking_resenyas = Resenya.objects.values('user__username').annotate(num_resenias=Count('id')).order_by('-num_resenias')[:10]

    #Obtener usuarios con más libros leídos (limite 10)
    users_with_most_read_books = ListBook.objects.filter(type_list='leidos').values('user__username').annotate(num_books_read=Count('listbookbook')).order_by('-num_books_read').filter(num_books_read__gt=0)[:10]

    return render(request, 'ranking.html', {
        'ranking_resenyas': ranking_resenyas,
        'ranking_libros_leidos': users_with_most_read_books,
    })
    

# Vista de error 404
def error404(request):
    return render(request, '404.html', {})

# Funcion para crear una notificación


def createNotification(to_user, from_user, notification_type, post=None, comment=None, request=None):
    # Comprobar si el usuario no es el mismo que el que está logueado
    if to_user != from_user:
        # Crear notificación
        notification = Notification.objects.create(
            to_user=to_user,
            from_user=from_user,
            notification_type=notification_type,
            post=post,
            comment=comment
        )

        # Guardar notificación en la base de datos
        notification.save()
