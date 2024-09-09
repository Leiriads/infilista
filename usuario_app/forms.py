from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UsuarioForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        choices=[('0', 'cmei'), ('1', 'admin')],
        label='Tipo de Usuário'
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tipo_usuario']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Remove espaços extras ou substitua por um caractere
        if ' ' in username:
            raise ValidationError("O nome de usuário não pode conter espaços.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if self.cleaned_data['tipo_usuario'] == '1':
            user.is_superuser = True
        else:
            user.is_superuser = False

        if commit:
            user.save()
        return user
