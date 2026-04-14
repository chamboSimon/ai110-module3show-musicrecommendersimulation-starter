"""
Command line runner for the Music Recommender Simulation.

Runs six user profiles in sequence:
  Core    — High-Energy Pop, Chill Lofi, Deep Intense Rock
  Edge    — Ghost Genre, Energy-Mood Conflict, Dead Centre
"""

from src.recommender import load_songs, recommend_songs


def run_profile(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a ranked recommendation block for one user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n{'=' * 52}")
    print(f"  {label}")
    print(f"  genre={user_prefs['genre']}  mood={user_prefs['mood']}")
    print(f"  energy={user_prefs['energy']}  valence={user_prefs['valence']}")
    print(f"{'=' * 52}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Score : {score:.2f} / 6.5")
        print(f"       Why   : {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.")

    # ── CORE PROFILE 1 ───────────────────────────────────────────────────────
    # High-energy, bright, danceable pop. The "Friday night" listener.
    run_profile(
        label="CORE 1 — High-Energy Pop",
        user_prefs={
            "genre":        "pop",
            "mood":         "happy",
            "energy":       0.88,
            "valence":      0.85,
            "acousticness": 0.10,
            "danceability": 0.88,
        },
        songs=songs,
    )

    # ── CORE PROFILE 2 ───────────────────────────────────────────────────────
    # Low energy, warm acoustics, chill mood. The "study session" listener.
    run_profile(
        label="CORE 2 — Chill Lofi",
        user_prefs={
            "genre":        "lofi",
            "mood":         "chill",
            "energy":       0.38,
            "valence":      0.58,
            "acousticness": 0.80,
            "danceability": 0.58,
        },
        songs=songs,
    )

    # ── CORE PROFILE 3 ───────────────────────────────────────────────────────
    # High energy, dark valence, raw acoustics. The "gym/drive" rock listener.
    run_profile(
        label="CORE 3 — Deep Intense Rock",
        user_prefs={
            "genre":        "rock",
            "mood":         "intense",
            "energy":       0.92,
            "valence":      0.42,
            "acousticness": 0.12,
            "danceability": 0.65,
        },
        songs=songs,
    )

    # ── EDGE PROFILE 1 ── Ghost Genre ────────────────────────────────────────
    # "k-pop" does not exist in the catalog — no song earns the +2.0 genre bonus.
    # Pure numeric proximity carries every result. Reveals catalog blind spots.
    run_profile(
        label="EDGE 1 — Ghost Genre (k-pop not in catalog)",
        user_prefs={
            "genre":        "k-pop",
            "mood":         "happy",
            "energy":       0.80,
            "valence":      0.82,
            "acousticness": 0.15,
            "danceability": 0.85,
        },
        songs=songs,
    )

    # ── EDGE PROFILE 2 ── Energy-Mood Conflict ───────────────────────────────
    # energy=0.95 (intense activation) vs mood="chill" (calm label).
    # Tests whether the +1.0 mood bonus can override the dominant energy weight.
    run_profile(
        label="EDGE 2 — Energy-Mood Conflict (energy=0.95, mood=chill)",
        user_prefs={
            "genre":        "ambient",
            "mood":         "chill",
            "energy":       0.95,
            "valence":      0.50,
            "acousticness": 0.50,
            "danceability": 0.50,
        },
        songs=songs,
    )

    # ── EDGE PROFILE 3 ── Dead Centre ────────────────────────────────────────
    # All numeric features = 0.5. No song sits at the midpoint on every axis.
    # Scores compress into a narrow band — categorical bonuses become the only
    # tiebreaker. Reveals whether the system degenerates under a neutral profile.
    run_profile(
        label="EDGE 3 — Dead Centre (all features = 0.5)",
        user_prefs={
            "genre":        "jazz",
            "mood":         "relaxed",
            "energy":       0.50,
            "valence":      0.50,
            "acousticness": 0.50,
            "danceability": 0.50,
        },
        songs=songs,
    )


if __name__ == "__main__":
    main()
