from rest_framework import routers
from .api import NotificacionesViewSet, PostViewSet, PostWithUserViewSet, PostUserViewSet, PostHashtagViewSet, PostSearchViewSet, UserSearchViewSet, PostGroupViewSet, GroupUserViewSet, ResenyaLibroViewSet, LibrosUserViewSet, BlogViewSet, LibrosSecciones, ListBookViewSet

router = routers.DefaultRouter()

#Posts todos
router.register('api/posts', PostViewSet, 'posts')

#Posts con información de usuario
router.register('api/muro', PostWithUserViewSet, 'postusuarios')

#Posts por usuario
router.register('api/postusuario/(?P<username>[\w-]+)', PostUserViewSet, 'postusuario')

#Posts por hashtag
router.register('api/posts/hashtag/(?P<hashtag>[\w-]+)', PostHashtagViewSet, 'posthashtag')

#Posts por grupo
router.register('api/posts/grupo/(?P<group>[\w-]+)', PostGroupViewSet, 'postgroup')

#Posts por busqueda de contenido
router.register('api/posts/busqueda/(?P<busqueda>[\w\s-]+)', PostSearchViewSet, 'postsearch')

#Users por busqueda de nombre
router.register('api/users/busqueda/(?P<busqueda>[\w\s-]+)', UserSearchViewSet, 'usersearch')

#Grupos a los que pertenece un usuario
router.register('api/grupos/(?P<username>[\w-]+)', GroupUserViewSet, 'groupuser')

#Añadir un libro a una lista
router.register('api/listbook/(?P<username>[\w-]+)', ListBookViewSet, 'listbook')

#Resenya de un libro
router.register('api/resenya/(?P<idLibro>[\w-]+)', ResenyaLibroViewSet, 'resenya')

#Libros de un perfil de escritor
router.register('api/libros/user/(?P<username>[\w-]+)', LibrosUserViewSet, 'libros')

#Secciones predefinidas en la base de datos
router.register('api/libros/secciones', LibrosSecciones, 'secciones')

#Libros entradas del blog
router.register('api/blog', BlogViewSet, 'blog')

#Notificaciones
router.register('api/notificaciones', NotificacionesViewSet, 'notificaciones')

urlpatterns = router.urls