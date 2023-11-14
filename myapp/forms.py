from django import forms

from django.utils.translation import gettext as _

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from .models import Profile

#Formulario de busqueda
class SearchForm(forms.Form):
    parametro = forms.CharField(max_length=100, required=True, label='Buscar')

#Formulario de registro de usuario personalizado
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=15, required=True, help_text=_("15 caracteres o menos. Letras solamente."))
    first_name = forms.CharField(max_length=30, required=True, label=_('Nombre'), help_text=_("Requerido. 30 caracteres o menos."))
    password1 = forms.CharField(max_length=60, label=_('Contraseña'), widget=forms.PasswordInput, help_text=_("Requerido. 8 caracteres o más. No puede ser una contraseña común o parecida."))
    password2 = forms.CharField(label=_('Confirmar contraseña'), widget=forms.PasswordInput, help_text=_("Requerido. Introduzca la misma contraseña que antes."))

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name',)

#Formulario de edición de usuario
class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=15, required=False, help_text='15 caracteres o menos. Letras solamente.')

    first_name = forms.CharField(max_length=30, required=False, label='Nombre', help_text='Requerido. 30 caracteres o menos.')

    last_name = forms.CharField(max_length=30, required=False, label='Apellido', help_text='Requerido. 30 caracteres o menos.')

    email = forms.EmailField(max_length=254, required=False, help_text='Requerido. Introduzca una dirección de correo válida.')

    password = forms.CharField(max_length=60, required=False, label='Contraseña', widget=forms.PasswordInput, help_text='Requerido. 8 caracteres o más. No puede ser una contraseña común o parecida.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')



#Formulario de usuario y perfil
class UserAndProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    #User campos
    username = forms.CharField(max_length=15, required=True, label='username', help_text=_('15 caracteres o menos. Letras solamente.'))

    first_name = forms.CharField(max_length=30, required=True, label='Nombre', help_text=_('Requerido. 30 caracteres o menos.'))

    email = forms.EmailField(max_length=254, required=False, help_text=_('Requerido. Introduzca una dirección de correo válida.'))

    # Campos adicionales del formulario de perfil
    bio = forms.CharField(max_length=500, required=False, label='Biografía', help_text=_('500 caracteres o menos.'))

    pic = forms.ImageField(required=False, label='Foto de perfil')

    location = forms.CharField(max_length=20, required=False, label='Ubicación', help_text='20 caracteres o menos.')



