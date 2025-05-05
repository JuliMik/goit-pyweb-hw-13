from django.forms import ModelForm, CharField, TextInput, ModelChoiceField
from .models import Tag, Author, Quote


# Форма для створення або редагування тегів
class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


# Форма для створення або редагування авторів
class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, required=True, widget=TextInput())
    born_date = CharField(min_length=3, required=True, widget=TextInput())
    born_location = CharField(min_length=3, required=True, widget=TextInput())
    description = CharField(min_length=3, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


# Форма для створення або редагування цитат
class QuoteForm(ModelForm):
    quote = CharField(min_length=10, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author', 'tags']


