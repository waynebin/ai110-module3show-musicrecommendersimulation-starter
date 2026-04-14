"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, DEFAULT_USER_PROFILE


def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_user_profile(prefs: dict) -> None:
    """Display user preferences in a formatted way."""
    print("\n📋 USER PROFILE:")
    print(f"   • Favorite Genre:  {prefs['favorite_genre']}")
    print(f"   • Favorite Mood:   {prefs['favorite_mood']}")
    print(f"   • Target Energy:   {prefs['target_energy']:.1f}")
    print(f"   • Likes Acoustic:  {'Yes' if prefs['likes_acoustic'] else 'No'}")


def print_recommendations(recommendations: list) -> None:
    """Display recommendations in a clean, readable format."""
    print_header("🎵 TOP RECOMMENDATIONS")
    
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        # Rank header
        print(f"\n#{i}. {song['title']}")
        print("   " + "─" * 75)
        
        # Song details
        print(f"   🎤 Artist:       {song['artist']}")
        print(f"   🎸 Genre:        {song['genre']} | Mood: {song['mood']}")
        print(f"   ⚡ Energy:       {song['energy']:.2f}")
        print(f"   🎹 Acousticness: {song['acousticness']:.2f}")
        print(f"   ⭐ Score:        {score:.2f} / 5.00")
        
        # Explanation with wrapping
        print(f"\n   💡 Why this song:")
        # Split explanation into parts for better readability
        reasons = explanation.split(": ", 1)
        if len(reasons) > 1:
            print(f"      {reasons[1]}")
        else:
            print(f"      {explanation}")
        
        print()


def main() -> None:
    """Main entry point for the music recommender."""
    print_header("🎵 MUSIC RECOMMENDER SIMULATION 🎵")
    
    # Load songs
    songs = load_songs("data/songs.csv")
    print(f"\n✓ Successfully loaded {len(songs)} songs from catalog")
    
    # Use default user profile
    user_prefs = DEFAULT_USER_PROFILE
    
    # Display user profile
    print_user_profile(user_prefs)
    
    # Get recommendations
    print(f"\n🔍 Finding your top 5 recommendations...")
    recommendations = recommend_songs(user_prefs, songs, k=5)
    
    # Display recommendations
    print_recommendations(recommendations)
    
    # Footer
    print("=" * 80)
    print("  Enjoy your personalized music recommendations! 🎧")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
