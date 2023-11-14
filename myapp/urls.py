from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

from django.contrib.auth.views import PasswordChangeView

# Rutas de la aplicación myapp
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.signin, name='signin'),
    path('register', views.signup, name='signup'),
    path('logout', views.signout, name='signout'),

    #Ruta para perfil de usuario
    path('user/<str:username>', views.user, name='user'),
    #Ruta para ver seguidores de usuario
    path('user/<str:username>/followers', views.followers, name='followers'),
    
    #Ruta para editar perfil de usuario
    path('edit/user/', views.edituser, name='edituser'),
    #Ruta para ver notificaciones
    path('notificaciones', views.notifications, name='notifications'),

    #Ruta para ver explorar
    path('explorar', views.explore, name='explore'),

    #Ruta para search
    path('search', views.search, name='search'),

    #Ruta para nuevo post
    path('newpost', views.newpost, name='newpost'),
    #Ruta para ver post
    path('post/<int:post_id>', views.post, name='post'),

    #Ruta para eliminar post
    path('post/<int:post_id>/delete', views.deletepost, name='deletepost'),

    #Ruta para seguir usuario
    path('user/<str:username>/follow', views.followOrUnfollow, name='followOrUnfollow'),

    #Ruta para hashtag
    path('hashtag/<str:hashtag>', views.hashtag, name='hashtag'),

    #Ruta para crear comentario
    path('post/<int:post_id>/comment', views.newcomment, name='newcomment'),
    #Ruta para eliminar comentario
    path('comment/<int:comment_id>/delete', views.deletecomment, name='deletecomment'),

    #Ruta para ver un libro
    path('libro/<str:id>', views.book, name='book'),

    #Ruta para añadir un libro a una lista o eliminarlo
    path('libro/actions/addOrRemove', views.addOrRemoveBook, name='addOrRemoveBook'),

    #Ruta para ver grupos
    path('grupos', views.groups, name='groups'),
    #Ruta para ver un grupo
    path('grupo/<str:id>', views.group, name='group'),
    #Ruta para unirse a un grupo
    path('grupo/<str:id>/join', views.joinOrLeaveGroup, name='joinOrLeaveGroup'),

    #Ruta para ver listas de libros de usuario
    path('user/<str:username>/lists', views.lists, name='lists'),

    #Reglas grupos
    path('grupos/reglas', views.rulesGroups, name='reglas'),

    #Ruta change password
    path('changePassword', views.ChangePassword, name='ChangePassword'),

    #Ruta para cambiar contraseña
    path('password/', views.ChangePassword, name='change_password'),
    
    #Ruta para redirigir a la página de inicio de sesión después de cambiar la contraseña
    path('password/done/', views.PasswordChangeDoneView, name='password_change_done'),

    #Ruta para eliminar cuenta
    path('delete/<str:username>/user', views.deleteuser, name='deleteuser'),

    #Ruta blog
    path('blog', views.blog, name='blog'),

    #Ruta para crear un post
    path('new', views.newPostForm, name='newPostForm'),

    #Ruta para ver un post del blog
    path('blog/<int:post_id>', views.postBlog, name='postBlog'),

    #Ruta para solicitud de perfil de escritor
    path('writer/<str:username>/solicitud', views.requestWriter, name='requestWriter'),

    #Ruta para ranking de usuarios
    path('ranking', views.ranking, name='ranking'),

    #404
    path('404', views.error404, name='404'),
    
  
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


