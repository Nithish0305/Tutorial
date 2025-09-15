from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Journal, Songs, Quotes
import json
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_connection import get_db_connection, insert_journal_entry

def index(request):
    """Home page view"""
    moods = ['Happy', 'Sad', 'Relax', 'Energetic', 'Romantic', 'Angry', 'Chill', 'Motivated', 'Melancholy', 'Excited']
    return render(request, 'journal/index.html', {'moods': moods})

def submit_mood(request):
    """Handle mood submission"""
    if request.method == 'POST':
        username = request.POST.get('username')
        mood = request.POST.get('mood')
        
        print(f"Received mood submission: Username={username}, Mood={mood}")  # Debug log
        
        # Validate input data
        if not username:
            print("Error: Username is missing")
            return JsonResponse({'status': 'error', 'message': 'Username is required'})
            
        if not mood:
            print("Error: Mood is missing")
            return JsonResponse({'status': 'error', 'message': 'Please select a mood'})
        
        # Ensure mood is properly capitalized for database lookup
        mood = mood.capitalize()
        
        # Get corresponding song and quote for the mood
        try:
            # Case-insensitive lookup for mood
            print(f"Looking up song and quote for mood: {mood}")
            song = Songs.objects.filter(mood__iexact=mood).first()
            quote = Quotes.objects.filter(mood__iexact=mood).first()
            
            print(f"Song lookup result: {song}, Quote lookup result: {quote}")  # Debug log
            
            if not song:
                print(f"Error: Song not found for mood '{mood}'")
                return JsonResponse({'status': 'error', 'message': f"Song not found for mood '{mood}'. Please try another mood."})
                
            if not quote:
                print(f"Error: Quote not found for mood '{mood}'")
                return JsonResponse({'status': 'error', 'message': f"Quote not found for mood '{mood}'. Please try another mood."})
            
            # Try to save using Django ORM first
            try:
                # Create journal entry using Django ORM
                journal = Journal(
                    username=username,
                    mood=mood,
                    song=song,
                    quote=quote
                )
                journal.save()
                print(f"Journal entry saved successfully via Django ORM: {journal.journal_id}")  # Debug log
                journal_id = journal.journal_id
            except Exception as orm_error:
                print(f"Django ORM save failed: {str(orm_error)}, trying direct PostgreSQL connection")
                
                # Fallback to direct PostgreSQL connection
                try:
                    print(f"About to insert journal entry with username={username}, mood={mood}")
                    journal_id = insert_journal_entry(username, mood, song.song_id if song else None, quote.quote_id if quote else None)
                    if not journal_id:
                        print("Error: Failed to insert journal entry")
                        return JsonResponse({'status': 'error', 'message': 'Failed to save your mood'})
                    print(f"Successfully inserted journal entry with ID: {journal_id}")
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Your mood has been recorded!',
                        'song': {'title': song.title, 'artist': song.artist, 'url': song.url} if song else None,
                        'quote': {'text': quote.text, 'author': quote.author} if quote else None
                    })
                except Exception as pg_error:
                    print(f"PostgreSQL direct save failed: {str(pg_error)}")
                    return JsonResponse({'status': 'error', 'message': 'Failed to save your mood'})
            
            response_data = {
                'status': 'success',
                'mood': mood,
                'quote': quote.quote,
                'song_path': song.file_path,
                'journal_id': journal_id
            }
            print(f"Sending response: {response_data}")  # Debug log
            return JsonResponse(response_data)
            
        except Exception as e:
            print(f"Error processing mood submission: {str(e)}")  # Debug log
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': f"An error occurred: {str(e)}. Please try again."})
    
    print("Invalid request method for submit_mood")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def history(request):
    """View journal history"""
    username = request.GET.get('username', '')
    if username:
        entries = Journal.objects.filter(username=username).order_by('-request_time')
        return render(request, 'journal/history.html', {'entries': entries, 'username': username})
    return render(request, 'journal/history.html', {'username': username})
