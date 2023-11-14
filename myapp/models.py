from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

#Modelo de perfil de usuario
class Profile(models.Model):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(default=False)
    writer = models.BooleanField(default=False)
    pic = models.ImageField(upload_to='myapp/static/imgs/profiles', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #Metodo para representar el objeto en formato JSON usado en la API
    def to_json(self):
        return {
            'user_id': self.user.id,
            'bio': self.bio,
            'location': self.location,
            'verified': self.verified,
        }

    def __str__(self):
        return self.user.username
    
#Modelo de posts
class Post(models.Model):
    content = models.TextField(max_length=340)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey('GroupReaders', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.content
    
#Modelo de comentarios
class Comment(models.Model):
    content = models.TextField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
 
#Modelo para relacionar seguidos
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.follower} sigue a {self.following}'
    
#Modelo de notificaciones
class Notification(models.Model):
    # 1 = Mencion, , 2 = Comentario , 3 = Follow
    notification_type = models.IntegerField(null=True, blank=True)
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.from_user} {self.notification_type} {self.to_user}'
    
#Modelo de grupos de lectores
class GroupReaders(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='myapp/static/imgs/groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, through='MemberGroup', related_name='group_members')

    #Metodo para representar el objeto en formato JSON usado en la API
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __str__(self):
        return self.name
    
#Modelo para relacionar un grupo con sus miembros
class MemberGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupReaders, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user} {self.group}'
    
#Modelo de listas de libros de usuarios
class ListBook(models.Model):
    #El tipo de lista puede ser: leidos, leyendo, por leer
    types = [
        ('leidos', 'Leidos'),
        ('leyendo', 'Leyendo'),
        ('por_leer', 'Por leer'),
    ]
    type_list = models.CharField(max_length=10, choices=types)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.type_list}'
    
#Modelo para relacionar listas de libros con libros
class ListBookBook(models.Model):
    list_book = models.ForeignKey(ListBook, on_delete=models.CASCADE)
    book = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.list_book} {self.book}'
    
#Modelo para las reseñas de los libros
class Resenya(models.Model):
    content = models.TextField(max_length=240)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.CharField(max_length=50)
    stars = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
#Modelo para relacionar un perfil de un usuario escritor con sus libros
class UserLibro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
#Modelo para seccion de libros
class BooksSection(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, default='')
    #Color tematico, opcion enter: verde, rojo, azul, amarillo, morado.
    colors = [
        ('verde', 'Verde'),
        ('rojo', 'Rojo'),
        ('azul', 'Azul'),
        ('amarillo', 'Amarillo'),
        ('morado', 'Morado'),
    ]
    color = models.CharField(max_length=10, choices=colors, default='verde')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

#Modelo para relacionar seccion de libros con libros
class BooksSectionBook(models.Model):
    book_section = models.ForeignKey(BooksSection, on_delete=models.CASCADE)
    book = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.book_section} {self.book}'

#Modelo para posts del blog
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=3000)
    image = models.ImageField(upload_to='myapp/static/imgs/blog', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.TextField(max_length=100)

    def __str__(self):
        return self.title
    
#Modelo de solicitudes de perfiles de escritor
class SolicitudWriter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    resuelta = models.BooleanField(default=False)
