from .models import Tweet
from .forms import UserRegistrationForm, TweetForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
import logging

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    try:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'tweet_list.html', {'tweets': tweets})
    except Exception as e:
        messages.error(request, "There was an issue loading tweets. Please try again.")
        return render(request, 'tweet_list.html', {'tweets': []})

@login_required
def tweet_create(request):
    try:
        if request.method == 'POST':
            form = TweetForm(request.POST, request.FILES)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Tweet created successfully!")
                return redirect('tweet_list')
            else:
                # Handle form errors in a user-friendly way
                for field, errors in form.errors.items():
                    for error in errors:
                        field_name = field
                        if field in form.fields:
                            field_name = form.fields[field].label or field
                        messages.error(request, f"{field_name}: {error}")
        else:
            form = TweetForm()
        return render(request, 'tweet_from.html', {'form': form})
    except Exception as e:
        # Log the error for server-side debugging but don't show it to users
        logger = logging.getLogger(__name__)
        logger.error(f"Error in tweet_create: {str(e)}")
        
        messages.error(request, "An error occurred while creating your tweet. Please try again.")
        return redirect('tweet_list')

@login_required
def tweet_edit(request, pk):
    try:
        tweet = get_object_or_404(Tweet, pk=pk)
        
        # Check if user is the owner of the tweet
        if tweet.user != request.user:
            messages.error(request, "You don't have permission to edit this tweet.")
            return redirect('tweet_list')
            
        if request.method == 'POST':
            form = TweetForm(request.POST, request.FILES, instance=tweet)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Tweet updated successfully!")
                return redirect('tweet_list')
            else:
                # Handle form errors in a user-friendly way
                for field, errors in form.errors.items():
                    for error in errors:
                        field_name = field
                        if field in form.fields:
                            field_name = form.fields[field].label or field
                        messages.error(request, f"{field_name}: {error}")
        else:
            form = TweetForm(instance=tweet)
        return render(request, 'tweet_from.html', {'form': form})
    except Http404:
        messages.error(request, "Tweet not found.")
        return redirect('tweet_list')
    except Exception as e:
        # Log the error for server-side debugging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in tweet_edit: {str(e)}")
        
        messages.error(request, "An error occurred while updating your tweet. Please try again.")
        return redirect('tweet_list')

@login_required
def tweet_delete(request, pk):
    try:
        tweet = get_object_or_404(Tweet, pk=pk)
        
        # Check if user is the owner of the tweet
        if tweet.user != request.user:
            messages.error(request, "You don't have permission to delete this tweet.")
            return redirect('tweet_list')
            
        if request.method == 'POST':
            tweet.delete()
            messages.success(request, "Tweet deleted successfully!")
            return redirect('tweet_list')
        return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})
    except Http404:
        messages.error(request, "Tweet not found.")
        return redirect('tweet_list')
    except Exception as e:
        messages.error(request, "An error occurred while deleting your tweet. Please try again.")
        return redirect('tweet_list')

def register(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Your account has been created successfully!")
                return redirect('tweet_list')
            else:
                for field in form:
                    for error in field.errors:
                        messages.error(request, f"{field.label}: {error}")
        else:
            form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
    except Exception as e:
        messages.error(request, "An error occurred during registration. Please try again.")
        return render(request, 'registration/register.html', {'form': UserCreationForm()})

def about(request):
    try:
        return render(request, 'about.html')
    except Exception as e:
        messages.error(request, "Unable to load the about page. Please try again.")
        return redirect('tweet_list')
