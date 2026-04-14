"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Taste Profile: "Pop / Happy" ---
    # A listener who wants bright, upbeat, danceable pop music.
    # High energy (0.80) signals an active, engaged listening mood.
    # High valence (0.82) targets emotionally bright, feel-good songs.
    # Low acousticness (0.20) favors polished, produced pop sound.
    # High danceability (0.80) prioritizes groove and rhythm.
    user_prefs = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.80,
        "valence":      0.82,
        "acousticness": 0.20,
        "danceability": 0.80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n{'='*44}")
    print(f"  Taste Profile: {user_prefs['genre'].upper()} / {user_prefs['mood'].upper()}")
    print(f"  Energy {user_prefs['energy']}  |  Valence {user_prefs['valence']}")
    print(f"{'='*44}")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Score : {score:.2f} / 6.5")
        print(f"    Why   : {explanation}")


if __name__ == "__main__":
    main()
