# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify and YouTube rely on two main strategies: collaborative filtering, which surfaces songs that users with similar taste enjoyed, and content-based filtering, which matches songs based on their sonic attributes. This simulation uses content-based filtering. Rather than recommending the most energetic or most acoustic songs in absolute terms, it scores each song by how close it sits to the user's stated preferences — then adds bonus points when categorical labels (genre, mood) match exactly.

### `Song` Features

Each `Song` object stores the following attributes read from `data/songs.csv`:

| Field | Type | Role in scoring |
|---|---|---|
| `id` | int | Unique identifier, not scored |
| `title` | str | Display name, not scored |
| `artist` | str | Display name, not scored |
| `genre` | str | Categorical — earns +2.0 pts on exact match |
| `mood` | str | Categorical — earns +1.0 pt on exact match |
| `energy` | float 0–1 | Numeric similarity, up to +1.5 pts |
| `valence` | float 0–1 | Numeric similarity, up to +1.0 pts |
| `acousticness` | float 0–1 | Numeric similarity, up to +0.5 pts |
| `danceability` | float 0–1 | Numeric similarity, up to +0.5 pts |

### `UserProfile` Features

Each `UserProfile` stores a preference value for each scored feature:

| Field | Type | Meaning |
|---|---|---|
| `favorite_genre` | str | Target genre for categorical bonus |
| `favorite_mood` | str | Target mood for categorical bonus |
| `target_energy` | float 0–1 | Desired arousal level |
| `target_valence` | float 0–1 | Desired emotional tone (dark → bright) |
| `target_acousticness` | float 0–1 | Preference for organic vs. electronic texture |
| `target_danceability` | float 0–1 | Preference for rhythmic engagement |

### Algorithm Recipe

Every song is passed through `score_song()` in `src/recommender.py`. Rules are applied in order and all points accumulate:

```
score = 0

if song.genre == user.favorite_genre  →  score += 2.0   # genre match
if song.mood  == user.favorite_mood   →  score += 1.0   # mood match

score += 1.5 × (1 - |song.energy       - user.target_energy|)
score += 1.0 × (1 - |song.valence      - user.target_valence|)
score += 0.5 × (1 - |song.acousticness - user.target_acousticness|)
score += 0.5 × (1 - |song.danceability - user.target_danceability|)

maximum possible score: 6.5 pts
```

**Why these weights?** Genre is the strongest identity signal — a jazz listener rarely accepts metal regardless of other matches, so it earns the most points. Mood is softer because the same label (e.g. "chill") appears across multiple genres. Energy is the most important numeric axis because its real-world spread in the catalog is widest and users feel it most consciously. Valence (emotional brightness) refines within an energy level. Acousticness and danceability are texture preferences that break ties.

### Ranking Rule (full catalog)

1. Call `score_song(user_prefs, song)` for every song in the catalog — no songs are skipped
2. Collect all `(song, score, explanation)` tuples into a list
3. Sort the list by score descending
4. Return the top `k` results

### Known Biases

- **Genre over-dominance.** A +2.0 genre bonus is so large it can lift a mediocre genre match above a near-perfect cross-genre song. A lofi track with the wrong energy could still outrank an ambient track that fits the user's numeric profile almost perfectly.
- **Exact-match brittleness.** Genre and mood comparisons are case-sensitive string equality. "Lofi" and "lofi" score differently, and adjacent moods like "relaxed" and "chill" earn zero shared credit even though a listener would likely enjoy both.
- **Catalog skew.** The 18-song catalog has uneven genre coverage (3 lofi songs, 1 blues, 1 reggae). Users who prefer underrepresented genres have fewer candidates to score well, so the numeric axes do more of the work and the top result may feel like a compromise.
- **No diversity control.** The ranking is a pure score sort, so the top 5 results could all be songs by the same artist or in the same sub-genre if they cluster near the user's preferences.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

