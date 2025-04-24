from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Quote, Author, Tag


# Головна сторінка, яка відображає всі цитати
# Create your views here.
def main(request):
    quotes_list = Quote.objects.all()
    context = {'quotes_list': quotes_list}
    return render(request, 'app_quotes/index.html', context)


# Створення нового автора. Доступно тільки для авторизованих користувачів
@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect(to='app_quotes:main')
        else:
            return render(request, 'app_quotes/author.html', {'form': form})

    return render(request, 'app_quotes/author.html', {'form': AuthorForm()})


# Створення нової цитати. Доступно тільки для авторизованих користувачів
@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            quote_author = Author.objects.filter(fullname=request.POST['authors']).first()
            new_quote.author = quote_author
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            '''
            for tag in request.POST.getlist('tags'):
                quote_tag = Tag.objects.filter(name=tag).first()
                new_quote.tags.add(quote_tag)
            '''
            return redirect(to='app_quotes:main')
        else:
            return render(request, 'app_quotes/quote.html', {"authors": authors, "tags": tags, 'form': form})

    return render(request, 'app_quotes/quote.html', {"authors": authors, "tags": tags, 'form': QuoteForm()})


# Деталі про автора за його ідентифікатором
def about_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'app_quotes/about_author.html', {"author": author})


# Створення нового тегу. Доступно тільки для авторизованих користувачів
@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='app_quotes:main')
        else:
            return render(request, 'app_quotes/tag.html', {'form': form})

    return render(request, 'app_quotes/tag.html', {'form': TagForm()})


# Видалення цитати. Доступно тільки для авторизованих користувачів
@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id).delete()
    return redirect(to='app_quotes:main')
