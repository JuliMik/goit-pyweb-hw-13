from django import template

register = template.Library()


# Функція, яка буде використовуватись як фільтр у шаблоні
def tags(quote_tags):
    return ', '.join([str(name) for name in quote_tags.all()])


register.filter('tags', tags)
