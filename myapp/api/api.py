from pstats import Stats
import statistics
from django.shortcuts import get_object_or_404

from requests import Response

from myapp.models import BlogPost, BooksSection, BooksSectionBook, Follow, GroupReaders, ListBook, ListBookBook, MemberGroup, Notification, Post, Resenya, UserLibro
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers

from django.db.models import Count

from django.db.models import Avg

'''
Serializar para un post con información de usuario
'''


class PostUserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    first_name = serializers.CharField(source='user.first_name')
    verified = serializers.BooleanField(source='user.profile.verified')
    num_comments = serializers.IntegerField(read_only=True)
    # GroupReaders
    group_name = serializers.StringRelatedField(
        source='group.name', read_only=True)  # Se agrega el nombre del grupo
    # Se agrega si es mio o no
    is_mine = serializers.BooleanField(read_only=True)
    id_user = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_is_mine(self, obj):
        return obj.user == self.context['request'].user

    # Sobreescribir el metodo de representación para agregar el numero de comentarios
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['num_comments'] = instance.num_comments
        ret['is_mine'] = self.get_is_mine(instance)
        ret['id_user'] = instance.user.id
        return ret


'''
Serializer para publicar un post
'''


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


'''
ViewSet de lista de Posts
'''


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        # Obtener posts ordenados por fecha de creación
        posts = Post.objects.filter(user=user).order_by('-created_at')

        return posts

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=Stats.HTTP_201_CREATED)
        return Response(serializer.errors, status=statistics.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


'''
Serializer para resenyas de libros
'''


class ResenyaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    verified = serializers.BooleanField(
        source='user.profile.verified', read_only=True)
    stars_average = serializers.IntegerField(read_only=True)
    readed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Resenya
        fields = ['id', 'book', 'stars', 'content', 'created_at',
                  'username', 'verified', 'stars_average', 'readed']

    # Sobreescribir el metodo de representación para agregar el username y calcular la media de estrellas
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['username'] = instance.user.username
        stars_average = Resenya.objects.filter(
            book=instance.book).aggregate(stars_average=Avg('stars'))
        ret['stars_average'] = stars_average['stars_average']
        return ret


'''
ViewSet de resenyas
'''


class ResenyaLibroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ResenyaSerializer

    def get_queryset(self):
        idLibro = self.kwargs['idLibro']
        resenyas = Resenya.objects.filter(book=idLibro).order_by('-created_at')
        for resenya in resenyas:
            user = resenya.user
            # Verificar si el usuario de la reseña tiene el libro en su lista de leídos
            resenya.readed = ListBookBook.objects.filter(
                list_book__user=user, list_book__type_list='leidos', book=idLibro).exists()
        return resenyas

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


'''
ViewSet de posts con información de usuario
'''


class PostWithUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUserSerializer

    # Obtener posts muro
    def get_queryset(self):
        posts = Post.objects.filter(user=self.request.user).annotate(
            num_comments=Count('comment')).order_by('-created_at')

        # Usuarios seguidos por el usuario
        user_request = self.request.user
        users_followed = Follow.objects.filter(
            follower=user_request).values_list('following', flat=True)
        user_groups = MemberGroup.objects.filter(
            user=user_request).values_list('group', flat=True)

        # Obtener los posts de los usuarios seguidos
        for user_followed in users_followed:
            posts |= Post.objects.filter(user=user_followed).annotate(
                num_comments=Count('comment'))

        # Obtener los posts de los grupos a los que pertenece el usuario
        if user_groups:
            for group in user_groups:
                posts_group = Post.objects.filter(
                    group=group).annotate(num_comments=Count('comment'))

            posts |= posts_group

        # Ordenar los posts por fecha de creación
        posts = posts.order_by('-created_at')

        return posts


'''
UserViewSet para obtener los posts de un usuario
'''


class PostUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUserSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        print(username)
        return Post.objects.filter(user=user).annotate(num_comments=Count('comment')).order_by('-created_at')


'''
ViewSet para los posts de un hashtag
'''


class PostHashtagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUserSerializer

    def get_queryset(self):
        hashtag = self.kwargs['hashtag']
        hashtag_regex = r'\b{}\b'.format(hashtag)

        return Post.objects.filter(content__regex=hashtag_regex).annotate(num_comments=Count('comment')).order_by('-created_at')


'''
ViewSet para los posts de un grupo
'''


class PostGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUserSerializer

    def get_queryset(self):
        group = self.kwargs['group']

        return Post.objects.filter(group=group).annotate(num_comments=Count('comment')).order_by('-created_at')


'''
ViewSet para los posts de una busqueda
'''


class PostSearchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUserSerializer

    def get_queryset(self):
        busqueda = self.kwargs['busqueda']

        return Post.objects.filter(content__regex=busqueda).annotate(num_comments=Count('comment')).order_by('-created_at')


'''
Serializer de User con informacion del perfil
'''


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    profile = serializers.StringRelatedField(source='user.profile')

    class Meta:
        model = User
        exclude = ['id', 'password', 'is_staff', 'is_superuser', 'is_active',
                   'last_login', 'user_permissions', 'date_joined', 'groups']
        # Excluir el password y id

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['profile'] = instance.profile.to_json()

        return ret


'''
Serializer para obtener grupos de lectura
'''


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupReaders
        fields = '__all__'


'''
Serializer para obtener ListBookBook
'''


class ListBookBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListBookBook
        fields = ['list_book', 'book', 'created_at', 'updated_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret


'''
Serializer para obtener las listas de libros de un usuario
'''


class ListBookSerializer(serializers.ModelSerializer):
    books = ListBookBookSerializer(
        source='listbookbook_set', many=True, read_only=True)

    class Meta:
        model = ListBook
        fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


'''
Serializer para añadir un libro a una lista de libros
'''


class ListBookBookCreateSerializer(serializers.Serializer):
    book = serializers.CharField(max_length=50)

    def create(self, validated_data):
        list_book = self.context['list_book']
        return ListBookBook.objects.create(list_book=list_book)



#Serializer para obtener los libros de una lista de libros
class ListBookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ListBookSerializer

    def get_queryset(self):
        usuario = self.kwargs['username']
        user = get_object_or_404(User, username=usuario)
        return ListBook.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        list_book = get_object_or_404(ListBook, id=request.data['list_book'])
        book = request.data['book']
        serializer = ListBookBookSerializer(
            data={'list_book': list_book.pk, 'book': book}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=Stats.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


# ViewSet para los usuarios por busqueda de nombre
class UserSearchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        busqueda = self.kwargs['busqueda']

        return User.objects.filter(username__regex=busqueda).order_by('-username')


# ViewSet para los grupos de un usuario
class GroupUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)

        return GroupReaders.objects.filter(members=user).order_by('-name')


# Serializer para los libros de un escritor
class LibrosUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLibro
        fields = '__all__'


# ViewSet de libros de un escritor
class LibrosUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LibrosUserSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        id = User.objects.get(username=username).id
        librosUser = UserLibro.objects.filter(user=id).order_by('-created_at')

        return librosUser


'''
Enpoint para obtener las secciones de libros de la base de datos
'''


class BooksSectionBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksSectionBook
        fields = ('id', 'book')


class BooksSectionSerializer(serializers.ModelSerializer):
    libros = serializers.SerializerMethodField()

    class Meta:
        model = BooksSection
        fields = ['id', 'title', 'color', 'libros']

    def get_libros(self, obj):
        libros = BooksSectionBook.objects.filter(book_section=obj)
        return [{'id': libro.book} for libro in libros]


# View set para las secciones de libros
class LibrosSecciones(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BooksSectionSerializer

    def get_queryset(self):
        return BooksSection.objects.all().order_by('id')


# Serializer para las entradas del blog
class EntradasBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


# ViewSet de entradas del blog
class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = EntradasBlogSerializer

    def get_queryset(self):
        entradasBlog = BlogPost.objects.all().order_by('-created_at')

        return entradasBlog


# Serializer notificaciones de un usuario
class NotificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# ViewSet notificaciones de un usuario
class NotificacionesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificacionesSerializer

    def get_queryset(self):
        usuario = self.request.user
        return Notification.objects.filter(to_user=usuario).order_by('-created_at')

    def perform_create(self, serializer):
        usuario = self.request.user

        # Obtener el campo 'to_user'
        to_user_data = self.request.data.get('to_user')

        # Verificar si to_user es un username o un ID de usuario
        if isinstance(to_user_data, str):
            # Buscar usuario por username
            user = get_object_or_404(User, username=to_user_data)
        else:
            # Buscar usuario por ID
            user = get_object_or_404(User, id=to_user_data)

        serializer.save(from_user=usuario, to_user=user)
