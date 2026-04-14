from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

# Default taste profile for testing and demonstrations
DEFAULT_USER_PROFILE = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.4,
    "likes_acoustic": True
}

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Score and rank songs based on the user's profile and return
        the top k recommendations.
        
        Scoring weights:
        - Genre match: 2.0
        - Mood match: 1.5
        - Energy similarity: 1.0
        - Acoustic preference: 0.5
        """
        scored_songs = []
        
        for song in self.songs:
            score = 0.0
            
            # Genre matching (highest weight)
            if song.genre == user.favorite_genre:
                score += 2.0
            
            # Mood matching (second priority)
            if song.mood == user.favorite_mood:
                score += 1.5
            
            # Energy similarity (distance-based)
            energy_similarity = 1.0 - abs(user.target_energy - song.energy)
            score += 1.0 * energy_similarity
            
            # Acoustic preference bonus
            if user.likes_acoustic and song.acousticness > 0.5:
                score += 0.5
            elif not user.likes_acoustic and song.acousticness < 0.5:
                score += 0.5
            
            # Store song with its score
            scored_songs.append((song, score))
        
        # Sort by score (highest first)
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k songs (without scores)
        top_k_songs = [song for song, score in scored_songs[:k]]
        
        return top_k_songs

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Generate a human-readable explanation for why a song was recommended.
        """
        reasons = []
        
        # Genre match
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({user.favorite_genre})")
        
        # Mood match
        if song.mood == user.favorite_mood:
            reasons.append(f"has your preferred mood ({user.favorite_mood})")
        
        # Energy similarity
        energy_diff = abs(user.target_energy - song.energy)
        if energy_diff < 0.2:
            reasons.append(f"has similar energy level ({song.energy:.2f} vs your target {user.target_energy:.2f})")
        
        # Acoustic preference
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append(f"is acoustic ({song.acousticness:.2f})")
        elif not user.likes_acoustic and song.acousticness < 0.5:
            reasons.append(f"is electronic/produced ({song.acousticness:.2f})")
        
        if reasons:
            return f"'{song.title}' by {song.artist}: " + ", ".join(reasons) + "."
        else:
            return f"'{song.title}' by {song.artist} was selected based on overall compatibility."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)
    
    print(f"✓ Loaded {len(songs)} songs")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    
    Args:
        user_prefs: Dictionary with keys: favorite_genre, favorite_mood, target_energy, likes_acoustic
        songs: List of song dictionaries from load_songs()
        k: Number of recommendations to return
    
    Returns:
        List of tuples: (song_dict, score, explanation)
    """
    scored_results = []
    
    for song in songs:
        score = 0.0
        reasons = []
        
        # Genre matching (highest weight)
        if song['genre'] == user_prefs['favorite_genre']:
            score += 2.0
            reasons.append(f"matches your favorite genre ({user_prefs['favorite_genre']})")
        
        # Mood matching (second priority)
        if song['mood'] == user_prefs['favorite_mood']:
            score += 1.5
            reasons.append(f"has your preferred mood ({user_prefs['favorite_mood']})")
        
        # Energy similarity (distance-based)
        energy_similarity = 1.0 - abs(user_prefs['target_energy'] - song['energy'])
        score += 1.0 * energy_similarity
        
        energy_diff = abs(user_prefs['target_energy'] - song['energy'])
        if energy_diff < 0.2:
            reasons.append(f"has similar energy level ({song['energy']:.2f} vs your target {user_prefs['target_energy']:.2f})")
        
        # Acoustic preference bonus
        if user_prefs['likes_acoustic'] and song['acousticness'] > 0.5:
            score += 0.5
            reasons.append(f"is acoustic ({song['acousticness']:.2f})")
        elif not user_prefs['likes_acoustic'] and song['acousticness'] < 0.5:
            score += 0.5
            reasons.append(f"is electronic/produced ({song['acousticness']:.2f})")
        
        # Generate explanation
        if reasons:
            explanation = f"'{song['title']}' by {song['artist']}: " + ", ".join(reasons) + "."
        else:
            explanation = f"'{song['title']}' by {song['artist']} was selected based on overall compatibility."
        
        scored_results.append((song, score, explanation))
    
    # Sort by score (highest first)
    scored_results.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k results
    return scored_results[:k]
