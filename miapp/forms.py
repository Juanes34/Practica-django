from django import forms
from django.core import validators

class FormArticle(forms.Form):
    title = forms.CharField(
        label='Titulo',
        max_length=100,
        required=True,
        widget = forms.TextInput(
            attrs={
                'placeholder':'Mete el titulo',
                'class': 'Titulo_for_article'
            }
        ),
        validators=[
            validators.MinLengthValidator(4,'El titulo es demasiado corto'),
            validators.RegexValidator('^[A-Za-z0-9 ]*$','El titulo está mal formado','invalid_title'),
        ]
        )
    content = forms.CharField(
        label='Contenido',
        widget=forms.Textarea,
        required=False,
        validators=[
            validators.MaxLengthValidator(50,'Te has pasado, mucho texto')
        ]
        )
    content.widget.attrs.update({
            'placeholder' : 'Mete el contenido',
            'class' : 'Contenido_for_article',
        })

    public_options = [
        (1,'Si'),
        (0,'No'),
    ]
    public = forms.TypedChoiceField(
        label='Publicado',
        choices = public_options,
    )