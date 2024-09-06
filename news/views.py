from django.shortcuts import render, redirect, get_object_or_404
from .models import News, Comment, Like
from .forms import NewsForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse  
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def news_list(request):
    news = News.objects.all()
    return render(request, 'news/news_list.html', {'news': news})

@login_required
def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    comments = news_item.comments.all()
    # likes = news_item.likes.count()
    print(dir(news_item))

    # Handle the comment form submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news_item
            comment.user = request.user
            comment.save()
            return redirect('news_detail', pk=news_item.pk)
    else:
        comment_form = CommentForm()

    # Check if the user has already liked this news item
    user_has_liked = news_item.likes.filter(user=request.user).exists()

    # Get all users who have liked this news item
    liked_users = news_item.likes.all().values_list('user__username', flat=True)


    return render(request, 'news/news_detail.html', {
        'news_item': news_item,
        'comments': comments,
        'total_comments': news_item.total_comments(),
        'total_likes': news_item.total_likes(),
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
        'liked_users': liked_users,  # Add this line
    })

@login_required
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    # if news.user != request.user:
    #     return HttpResponseForbidden()  # Prevent non-author users from editing
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/edit.html', {'form': form})
 
@login_required
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    return render(request, 'news/delete.html', {'news': news})


@login_required
def add_comment(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(news=news_item, user=request.user, content=content)
    return HttpResponseRedirect(reverse('news/news_detail', args=[pk]))

def toggle_like(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    like, created = Like.objects.get_or_create(news=news_item, user=request.user)

    if not created:  # If the like already exists, remove it (unlike)
        like.delete()
    
    return redirect('news_detail', pk=news_item.pk)


@login_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)  # Don’t commit yet, as we want to add the user
            news.user = request.user  # Link the news to the logged-in user
            news.save()
            messages.success(request, 'News added successfully!')
            return redirect('news_list')  # Redirect to the news list or detail page
    else:
        form = NewsForm()
    
    return render(request, 'news/add_news.html', {'form': form})
