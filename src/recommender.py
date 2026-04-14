import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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

    Primary axes (define the emotional quadrant):
        target_energy      — arousal level, 0.0 (calm) → 1.0 (intense)
        target_valence     — emotional tone, 0.0 (dark) → 1.0 (bright)

    Texture axes (refine within the quadrant):
        target_acousticness  — 0.0 (electronic/produced) → 1.0 (organic/acoustic)
        target_danceability  — 0.0 (ambient/listening) → 1.0 (groove-forward)

    Categorical filters (applied before numeric scoring):
        favorite_mood      — soft pre-filter on mood label
        favorite_genre     — tiebreaker only, not used in distance score
        likes_acoustic     — legacy boolean kept for test compatibility
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.70
    target_acousticness: float = 0.50
    target_danceability: float = 0.70

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user profile and return the top-k results sorted by score."""
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "valence":      user.target_valence,
            "acousticness": user.target_acousticness,
            "danceability": user.target_danceability,
        }
        scored = [(score_song(user_prefs, asdict(s))[0], s) for s in self.songs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string listing which scoring rules contributed points for this song."""
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "valence":      user.target_valence,
            "acousticness": user.target_acousticness,
            "danceability": user.target_danceability,
        }
        _, reasons = score_song(user_prefs, asdict(song))
        return ", ".join(reasons) if reasons else "Numeric similarity match"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Scoring recipe (max 6.0 pts):
      +1.0  genre exact match   (was +2.0 — halved so energy leads)
      +1.0  mood exact match
      +2.0  energy similarity   (was +1.5 — doubled; primary perceptual axis)
      +1.0  valence similarity  (1.0 × (1 - |song - target|))
      +0.5  acousticness similarity
      +0.5  danceability similarity
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_pts = 2.0 * (1 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts:.2f})")

    valence_pts = 1.0 * (1 - abs(song["valence"] - user_prefs["valence"]))
    score += valence_pts

    acoustic_pts = 0.5 * (1 - abs(song["acousticness"] - user_prefs["acousticness"]))
    score += acoustic_pts

    dance_pts = 0.5 * (1 - abs(song["danceability"] - user_prefs["danceability"]))
    score += dance_pts

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
