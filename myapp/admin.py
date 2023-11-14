from django.contrib import admin

from .models import Profile, Post, Comment, Follow, Notification, GroupReaders, MemberGroup, ListBook, ListBookBook, Resenya, UserLibro, BlogPost, SolicitudWriter, BooksSection, BooksSectionBook

#Registro de modelos para panel de administracion
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Notification)
admin.site.register(GroupReaders)
admin.site.register(MemberGroup)
admin.site.register(ListBook)
admin.site.register(ListBookBook)
admin.site.register(Resenya)
admin.site.register(UserLibro)
admin.site.register(BlogPost)
admin.site.register(SolicitudWriter)
admin.site.register(BooksSection)
admin.site.register(BooksSectionBook)
