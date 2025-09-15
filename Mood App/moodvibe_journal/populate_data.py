import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moodvibe.settings')
django.setup()

from journal.models import Songs, Quotes

# Define quotes for each mood
quotes_data = {
    'Happy': "Happiness is not something ready-made. It comes from your own actions.",
    'Sad': "The pain you feel today is the strength you feel tomorrow.",
    'Relax': "The time to relax is when you don't have time for it.",
    'Energetic': "Energy and persistence conquer all things.",
    'Romantic': "Love is composed of a single soul inhabiting two bodies.",
    'Angry': "Speak when you are angry and you will make the best speech you will ever regret.",
    'Chill': "Life is better when you're chilling.",
    'Motivated': "The harder you work for something, the greater you'll feel when you achieve it.",
    'Melancholy': "The heart has its reasons which reason knows not of.",
    'Excited': "The future belongs to those who believe in the beauty of their dreams."
}

# Define song paths for each mood
songs_data = {
    'Happy': "media/happy.mp3",
    'Sad': "media/sad.mp3",
    'Relax': "media/relax.mp3",
    'Energetic': "media/energetic.mp3",
    'Romantic': "media/romantic.mp3",
    'Angry': "media/angry.mp3",
    'Chill': "media/chill.mp3",
    'Motivated': "media/motivated.mp3",
    'Melancholy': "media/melancholy.mp3",
    'Excited': "media/excited.mp3"
}

def populate_database():
    # Clear existing data
    Songs.objects.all().delete()
    Quotes.objects.all().delete()
    
    print("Populating database with mood data...")
    
    # Add quotes
    for mood, quote_text in quotes_data.items():
        quote = Quotes(mood=mood, quote=quote_text)
        quote.save()
        print(f"Added quote for {mood}")
    
    # Add songs
    for mood, song_path in songs_data.items():
        song = Songs(mood=mood, file_path=song_path)
        song.save()
        print(f"Added song for {mood}")
    
    print("\nDatabase population complete!")

if __name__ == "__main__":
    populate_database()