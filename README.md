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

Six profiles were run against the 18-song catalog: three core listener types and three adversarial edge cases designed to expose weaknesses in the scoring logic.

---

### CORE 1 — High-Energy Pop

Profile: `genre=pop  mood=happy  energy=0.88  valence=0.85`

```
  #1  Sunrise City  —  Neon Echo
       Genre: pop  |  Mood: happy
       Score : 6.32 / 6.5
       Why   : genre match (+2.0), mood match (+1.0), energy similarity (+1.41)

  #2  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score : 5.32 / 6.5
       Why   : genre match (+2.0), energy similarity (+1.42)

  #3  Rooftop Lights  —  Indigo Parade
       Genre: indie pop  |  Mood: happy
       Score : 4.12 / 6.5
       Why   : mood match (+1.0), energy similarity (+1.32)

  #4  Zenith Drop  —  Pulse Circuit
       Genre: edm  |  Mood: euphoric
       Score : 3.30 / 6.5
       Why   : energy similarity (+1.40)

  #5  Street Frequency  —  DJ Mosaic
       Genre: hip-hop  |  Mood: energized
       Score : 3.13 / 6.5
       Why   : energy similarity (+1.35)
```

**Observation:** Works as expected. Sunrise City is a near-perfect match (6.32/6.5). Gym Hero earns #2 on genre alone despite its mood being "intense" — demonstrating that the +2.0 genre bonus can compensate for a mood mismatch.

---

### CORE 2 — Chill Lofi

Profile: `genre=lofi  mood=chill  energy=0.38  valence=0.58`

```
  #1  Library Rain  —  Paper Lanterns
       Genre: lofi  |  Mood: chill
       Score : 6.41 / 6.5
       Why   : genre match (+2.0), mood match (+1.0), energy similarity (+1.46)

  #2  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score : 6.36 / 6.5
       Why   : genre match (+2.0), mood match (+1.0), energy similarity (+1.44)

  #3  Focus Flow  —  LoRoom
       Genre: lofi  |  Mood: focused
       Score : 5.44 / 6.5
       Why   : genre match (+2.0), energy similarity (+1.47)

  #4  Spacewalk Thoughts  —  Orbit Bloom
       Genre: ambient  |  Mood: chill
       Score : 4.13 / 6.5
       Why   : mood match (+1.0), energy similarity (+1.35)

  #5  Coffee Shop Stories  —  Slow Stereo
       Genre: jazz  |  Mood: relaxed
       Score : 3.29 / 6.5
       Why   : energy similarity (+1.48)
```

**Observation:** Top 3 are all lofi — the genre bonus creates a strong cluster. Focus Flow at #3 scores 5.44 despite a mood mismatch ("focused" ≠ "chill"), purely on genre + energy proximity. The gap between #3 (5.44) and #4 (4.13) shows how much the genre bonus dominates.

---

### CORE 3 — Deep Intense Rock

Profile: `genre=rock  mood=intense  energy=0.92  valence=0.42`

```
  #1  Storm Runner  —  Voltline
       Genre: rock  |  Mood: intense
       Score : 6.41 / 6.5
       Why   : genre match (+2.0), mood match (+1.0), energy similarity (+1.48)

  #2  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score : 3.98 / 6.5
       Why   : mood match (+1.0), energy similarity (+1.48)

  #3  Iron Collapse  —  Fracture Point
       Genre: metal  |  Mood: angry
       Score : 3.15 / 6.5
       Why   : energy similarity (+1.43)

  #4  Night Drive Loop  —  Neon Echo
       Genre: synthwave  |  Mood: moody
       Score : 3.08 / 6.5
       Why   : energy similarity (+1.24)

  #5  Street Frequency  —  DJ Mosaic
       Genre: hip-hop  |  Mood: energized
       Score : 2.96 / 6.5
       Why   : energy similarity (+1.29)
```

**Observation:** Storm Runner is the obvious #1 with 6.41/6.5. Only one rock song exists in the catalog — so #2 onward is drawn from adjacent energy levels across unrelated genres. Iron Collapse (metal) reaches #3 on energy alone, even though its valence (0.25) is far darker than the profile target (0.42).

---

### EDGE 1 — Ghost Genre (k-pop not in catalog)

Profile: `genre=k-pop  mood=happy  energy=0.80  valence=0.82`

```
  #1  Sunrise City  —  Neon Echo
       Genre: pop  |  Mood: happy
       Score : 4.41 / 6.5
       Why   : mood match (+1.0), energy similarity (+1.47)

  #2  Rooftop Lights  —  Indigo Parade
       Genre: indie pop  |  Mood: happy
       Score : 4.32 / 6.5
       Why   : mood match (+1.0), energy similarity (+1.44)

  #3  Street Frequency  —  DJ Mosaic
       Genre: hip-hop  |  Mood: energized
       Score : 3.28 / 6.5
       Why   : energy similarity (+1.47)

  #4  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score : 3.19 / 6.5
       Why   : energy similarity (+1.30)

  #5  Zenith Drop  —  Pulse Circuit
       Genre: edm  |  Mood: euphoric
       Score : 3.11 / 6.5
       Why   : energy similarity (+1.28)
```

**Finding:** No song earns the +2.0 genre bonus — the maximum achievable score drops to 4.5. The top result (4.41/6.5) would be a mediocre result in any other profile. The numeric axes hold up well, surfacing the sonically closest songs (pop, indie pop), but the system has no way to signal to the user that their preferred genre is absent.

---

### EDGE 2 — Energy-Mood Conflict (energy=0.95, mood=chill)

Profile: `genre=ambient  mood=chill  energy=0.95  valence=0.50`

```
  #1  Spacewalk Thoughts  —  Orbit Bloom
       Genre: ambient  |  Mood: chill
       Score : 5.09 / 6.5
       Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.50)

  #2  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score : 3.48 / 6.5
       Why   : mood match (+1.0), energy similarity (+0.70)

  #3  Library Rain  —  Paper Lanterns
       Genre: lofi  |  Mood: chill
       Score : 3.28 / 6.5
       Why   : mood match (+1.0), energy similarity (+0.60)

  #4  Storm Runner  —  Voltline
       Genre: rock  |  Mood: intense
       Score : 3.14 / 6.5
       Why   : energy similarity (+1.44)

  #5  Iron Collapse  —  Fracture Point
       Genre: metal  |  Mood: angry
       Score : 2.98 / 6.5
       Why   : energy similarity (+1.47)
```

**Finding — the system is "tricked."** Spacewalk Thoughts (energy=0.28) wins at #1 despite the user asking for energy=0.95. It earns genre (+2.0) and mood (+1.0) bonuses worth 3.0 pts, which completely overrides its 0.50 energy penalty. The categorical bonuses can outweigh a large numeric mismatch when both genre and mood align. Storm Runner (the energetically correct answer) sits at #4 earning only energy points.

---

### EDGE 3 — Dead Centre (all features = 0.5)

Profile: `genre=jazz  mood=relaxed  energy=0.50  valence=0.50`

```
  #1  Coffee Shop Stories  —  Slow Stereo
       Genre: jazz  |  Mood: relaxed
       Score : 5.88 / 6.5
       Why   : genre match (+2.0), mood match (+1.0), energy similarity (+1.30)

  #2  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score : 3.15 / 6.5
       Why   : energy similarity (+1.38)

  #3  Focus Flow  —  LoRoom
       Genre: lofi  |  Mood: focused
       Score : 3.07 / 6.5
       Why   : energy similarity (+1.35)

  #4  Dusty Road Home  —  The Riverbend Boys
       Genre: country  |  Mood: nostalgic
       Score : 3.06 / 6.5
       Why   : energy similarity (+1.42)

  #5  Tide & Time  —  Coral Drift
       Genre: reggae  |  Mood: dreamy
       Score : 3.04 / 6.5
       Why   : energy similarity (+1.47)
```

**Finding — scores compress, categories dominate.** Coffee Shop Stories surges to #1 (5.88/6.5) while #2–#5 are packed in a 0.11-point band (3.04–3.15). With all numeric preferences at the neutral midpoint, every song looks equally "close" on the continuous features — making genre and mood the only real differentiator. The result is correct but fragile: change the genre from "jazz" to anything else and the #1 result swaps entirely.

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

---

### The Biggest Learning Moment

The clearest turning point came during the Edge 2 adversarial test — the "Energy-Mood Conflict" profile where we asked for `energy=0.95` but `mood=chill`. Spacewalk Thoughts, a near-silent ambient track with `energy=0.28`, ranked #1. The energetically correct song sat at #4.

That result made something abstract suddenly concrete: **feature weights are assumptions, and unexamined assumptions produce confident-sounding mistakes.** The system did not malfunction. It followed its rules exactly. The problem was that the rules allowed two label matches to award more points than a large numeric mismatch could subtract. Once you see that happen in real output — once you watch a meditation-room track win over something genuinely intense — the idea of "bias baked into the math" stops being theoretical and becomes obvious.

The lesson: a recommender is not a neutral arbiter. It is a set of priorities written in numbers. Whoever chose the numbers chose the priorities, and the system will defend those priorities even when the result makes no human sense.

---

### How AI Tools Helped — and When to Double-Check Them

AI assistance was most useful during the design phase: thinking through the two-axis model of vibe (arousal × valence), identifying which features carry independent signal versus which are correlated, and suggesting adversarial profile ideas like the Ghost Genre and Dead Centre tests. Those suggestions turned out to be genuinely revealing — the Dead Centre profile in particular exposed a compression problem in the scores that would have been easy to miss by only testing "normal" profiles.

Where human verification mattered:

- **The math.** When the genre weight was halved from +2.0 to +1.0 and energy was doubled from 1.5× to 2.0×, the new maximum score changed from 6.5 to 6.0. The output header still said "/ 6.5" until we caught and corrected it. AI tools generate plausible-looking numbers — checking that they are also correct numbers is always a human responsibility.
- **Interpreting results.** The Edge 2 output showed Spacewalk Thoughts at #1 with a score of 5.09. Whether that result is "wrong" requires musical judgment, not calculation. The system cannot tell you whether it failed — it can only tell you the score.
- **Catalog bias.** Choosing which songs to add required noticing what was missing: dark valence, non-Western genres, genre depth beyond lofi. That kind of gap analysis requires knowing what a well-rounded catalog should look like, which is domain knowledge the tool does not have on its own.

---

### What Is Surprising About Simple Algorithms Feeling Like Recommendations

Six numbers and two label comparisons — that is the entire scoring system. No neural network, no listening history, no audio analysis. And yet for the three core profiles, the results pass a basic reasonableness test immediately: the right song is #1, the ordering makes sense, and the explanations feel accurate.

This is both reassuring and unsettling.

It is reassuring because it means the core idea of content-based filtering — match features, rank by closeness — actually works even at tiny scale. You do not need millions of users or deep learning to produce results that feel intuitively right most of the time.

**The surprising part is what "most of the time" conceals.**

The system produces confident-looking output for every profile, including the broken ones. When the wrong song wins, the output does not look different from when the right song wins. The formatting is identical, the explanation reads logically ("genre match (+1.0), mood match (+1.0), energy similarity (+0.66)"), and the score is a reasonable-looking number. There is no signal in the output that tells you whether to trust the result.

This is how real algorithmic harms accumulate. A user who gets a bad recommendation does not see a warning — they see a song title and a confident suggestion. The system never hedges. This is why model cards, bias audits, and adversarial testing exist: the output of a working system and the output of a silently biased one can look completely identical.

**One genuinely unexpected finding:** genre is functioning as a proxy for cultural identity, not just sound. When the system gives a lofi listener a +1.0 bonus and gives a K-pop listener a +0.0 bonus — despite potentially identical energy, valence, and acousticness preferences — it is encoding a hierarchy. One community's taste is represented; the other's is not. The math does not know this. The math is just adding numbers. But the effect is that users from underrepresented musical cultures receive structurally worse recommendations with no explanation, which is a real fairness issue in production systems at scale.

---

### What Would Come Next

**1. Catalog depth over catalog breadth.**
Adding more songs to each existing genre would do more than adding entirely new genres. Right now the genre bonus always resolves to a single song. With five songs per genre, the numeric axes would actually compete within a genre — which is how Spotify-scale systems work.

**2. A "group session" profile.**
Blend preferences from two or three users by averaging their target values, then measure how much the recommended songs diverge from each individual's preferences. This would surface a real tension that collaborative systems deal with constantly: optimizing for a group always under-serves someone.

**3. A novelty dial.**
Add a parameter from 0.0 (pure similarity) to 1.0 (pure surprise) that penalizes songs too close to what the user already likes. Slide it toward 1.0 and the system should start surfacing songs from adjacent but unfamiliar areas of the feature space — modeling the explore/exploit tradeoff that every real recommendation engine has to solve.

**4. Replace hand-crafted features with audio embeddings.**
Instead of assigning energy and valence by hand, run actual audio files through a pre-trained model (like a MusicNN or a CLAP embedding) and let the model derive the features automatically. The catalog would become self-describing, and features like "sounds like late 90s trip-hop" could emerge without being explicitly programmed.


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

