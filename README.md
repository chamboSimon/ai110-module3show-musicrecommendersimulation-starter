# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project builds a content-based music recommender in Python. It loads an 18-song catalog from a CSV file, scores each song against a user taste profile using a weighted proximity formula, and returns a ranked, explained list of suggestions in the terminal. Three normal listener profiles and three adversarial edge cases were used to test the system and expose scoring weaknesses including filter bubbles, genre equity gaps, and label-override failures.

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
| `genre` | str | Categorical — earns +1.0 pt on exact match |
| `mood` | str | Categorical — earns +1.0 pt on exact match |
| `energy` | float 0–1 | Numeric similarity, up to +2.0 pts (primary axis) |
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

if song.genre == user.favorite_genre  →  score += 1.0   # genre match
if song.mood  == user.favorite_mood   →  score += 1.0   # mood match

score += 2.0 × (1 - |song.energy       - user.target_energy|)
score += 1.0 × (1 - |song.valence      - user.target_valence|)
score += 0.5 × (1 - |song.acousticness - user.target_acousticness|)
score += 0.5 × (1 - |song.danceability - user.target_danceability|)

maximum possible score: 6.0 pts
```

**Why these weights?** Energy leads at 2.0× because it is the axis users feel most immediately — a calm song recommended to someone who wants intensity is a worse failure than a wrong genre. Genre and mood each earn 1.0 pt on exact match: they are strong identity signals but should not override a large energy mismatch. Valence refines the emotional tone within an energy level. Acousticness and danceability are texture preferences that break ties. The original genre weight was +2.0 and energy was 1.5× — this was rebalanced after adversarial testing showed genre bonuses were overriding the primary perceptual axis.

### Ranking Rule (full catalog)

1. Call `score_song(user_prefs, song)` for every song in the catalog — no songs are skipped
2. Collect all `(song, score, explanation)` tuples into a list
3. Sort the list by score descending
4. Return the top `k` results

### Known Biases

- **Label-override risk.** Even after rebalancing, genre + mood bonuses combined (+2.0 pts) equal the energy maximum (+2.0 pts). A song with very wrong energy can still rank highly if both labels match — proved in the Energy-Mood Conflict experiment.
- **Exact-match brittleness.** Genre and mood comparisons are case-sensitive string equality. Adjacent moods like "relaxed" and "chill" earn zero shared credit even though a listener would likely enjoy both.
- **Catalog skew.** The 18-song catalog has uneven genre coverage — 3 lofi songs vs 1 of almost every other genre. Users who prefer low-energy music get a lofi filter bubble regardless of their genre preference.
- **No diversity control.** The ranking is a pure score sort, so the top 5 results can cluster in one genre when the genre bonus fires repeatedly. See model_card.md for a full bias analysis.

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
       Score : 5.79 / 6.0
       Why   : genre match (+1.0), mood match (+1.0), energy similarity (+1.88)

  #2  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score : 4.79 / 6.0
       Why   : genre match (+1.0), energy similarity (+1.90)

  #3  Rooftop Lights  —  Indigo Parade
       Genre: indie pop  |  Mood: happy
       Score : 4.56 / 6.0
       Why   : mood match (+1.0), energy similarity (+1.76)

  #4  Zenith Drop  —  Pulse Circuit
       Genre: edm  |  Mood: euphoric
       Score : 3.77 / 6.0
       Why   : energy similarity (+1.86)

  #5  Street Frequency  —  DJ Mosaic
       Genre: hip-hop  |  Mood: energized
       Score : 3.57 / 6.0
       Why   : energy similarity (+1.80)
```

**Observation:** Works as expected. Sunrise City is a near-perfect match (5.79/6.0). Gym Hero earns #2 via genre match plus near-perfect energy, despite its mood being "intense" not "happy" — showing genre is still a strong signal even after rebalancing.

---

### CORE 2 — Chill Lofi

Profile: `genre=lofi  mood=chill  energy=0.38  valence=0.58`

```
  #1  Library Rain  —  Paper Lanterns
       Genre: lofi  |  Mood: chill
       Score : 5.89 / 6.0
       Why   : genre match (+1.0), mood match (+1.0), energy similarity (+1.94)

  #2  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score : 5.84 / 6.0
       Why   : genre match (+1.0), mood match (+1.0), energy similarity (+1.92)

  #3  Focus Flow  —  LoRoom
       Genre: lofi  |  Mood: focused
       Score : 4.93 / 6.0
       Why   : genre match (+1.0), energy similarity (+1.96)

  #4  Spacewalk Thoughts  —  Orbit Bloom
       Genre: ambient  |  Mood: chill
       Score : 4.58 / 6.0
       Why   : mood match (+1.0), energy similarity (+1.80)

  #5  Coffee Shop Stories  —  Slow Stereo
       Genre: jazz  |  Mood: relaxed
       Score : 3.79 / 6.0
       Why   : energy similarity (+1.98)
```

**Observation:** Top 3 are all lofi — the catalog only has 3 lofi songs and all cluster at low energy, so genre bonus locks them in. Spacewalk Thoughts at #4 (4.58) is now closer to #3 Focus Flow (4.93) than before the weight rebalance — the reduced genre bonus narrowed the gap between lofi and adjacent low-energy songs.

---

### CORE 3 — Deep Intense Rock

Profile: `genre=rock  mood=intense  energy=0.92  valence=0.42`

```
  #1  Storm Runner  —  Voltline
       Genre: rock  |  Mood: intense
       Score : 5.91 / 6.0
       Why   : genre match (+1.0), mood match (+1.0), energy similarity (+1.98)

  #2  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score : 4.48 / 6.0
       Why   : mood match (+1.0), energy similarity (+1.98)

  #3  Iron Collapse  —  Fracture Point
       Genre: metal  |  Mood: angry
       Score : 3.63 / 6.0
       Why   : energy similarity (+1.90)

  #4  Night Drive Loop  —  Neon Echo
       Genre: synthwave  |  Mood: moody
       Score : 3.50 / 6.0
       Why   : energy similarity (+1.66)

  #5  Street Frequency  —  DJ Mosaic
       Genre: hip-hop  |  Mood: energized
       Score : 3.39 / 6.0
       Why   : energy similarity (+1.72)
```

**Observation:** Storm Runner is the obvious #1 (5.91/6.0) — genre, mood, and near-perfect energy all align. Only one rock song exists in the catalog, so #2 onward comes from other genres. Gym Hero reaches #2 on mood match plus identical energy proximity, showing that a single mood label is enough to separate it from the rest of the field.

---

### EDGE 1 — Ghost Genre (k-pop not in catalog)

Profile: `genre=k-pop  mood=happy  energy=0.80  valence=0.82`

```
  #1  Sunrise City  —  Neon Echo
       Genre: pop  |  Mood: happy
       Score : 4.89 / 6.0
       Why   : mood match (+1.0), energy similarity (+1.96)

  #2  Rooftop Lights  —  Indigo Parade
       Genre: indie pop  |  Mood: happy
       Score : 4.80 / 6.0
       Why   : mood match (+1.0), energy similarity (+1.92)

  #3  Street Frequency  —  DJ Mosaic
       Genre: hip-hop  |  Mood: energized
       Score : 3.77 / 6.0
       Why   : energy similarity (+1.96)

  #4  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense
       Score : 3.62 / 6.0
       Why   : energy similarity (+1.74)

  #5  Zenith Drop  —  Pulse Circuit
       Genre: edm  |  Mood: euphoric
       Score : 3.54 / 6.0
       Why   : energy similarity (+1.70)
```

**Finding:** No song earns the genre bonus — k-pop does not exist in the catalog. The maximum achievable score is 5.0 (mood + perfect numeric) instead of 6.0. The system surfaces the sonically closest songs correctly, but gives the user no warning that their preferred genre was never represented.

---

### EDGE 2 — Energy-Mood Conflict (energy=0.95, mood=chill)

Profile: `genre=ambient  mood=chill  energy=0.95  valence=0.50`

```
  #1  Spacewalk Thoughts  —  Orbit Bloom
       Genre: ambient  |  Mood: chill
       Score : 4.25 / 6.0
       Why   : genre match (+1.0), mood match (+1.0), energy similarity (+0.66)

  #2  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score : 3.71 / 6.0
       Why   : mood match (+1.0), energy similarity (+0.94)

  #3  Storm Runner  —  Voltline
       Genre: rock  |  Mood: intense
       Score : 3.62 / 6.0
       Why   : energy similarity (+1.92)

  #4  Library Rain  —  Paper Lanterns
       Genre: lofi  |  Mood: chill
       Score : 3.48 / 6.0
       Why   : mood match (+1.0), energy similarity (+0.80)

  #5  Iron Collapse  —  Fracture Point
       Genre: metal  |  Mood: angry
       Score : 3.47 / 6.0
       Why   : energy similarity (+1.96)
```

**Finding — the system is still tricked, but less so.** Spacewalk Thoughts (energy=0.28) still wins at #1 despite the user asking for energy=0.95. After the weight rebalance, its lead over Storm Runner (the energetically correct answer) shrank from 1.95 pts down to 0.63 pts. Storm Runner now reaches #3 instead of #4, but the label-matching song still wins because genre + mood bonuses (+2.0 combined) beat the energy mismatch penalty.

---

### EDGE 3 — Dead Centre (all features = 0.5)

Profile: `genre=jazz  mood=relaxed  energy=0.50  valence=0.50`

```
  #1  Coffee Shop Stories  —  Slow Stereo
       Genre: jazz  |  Mood: relaxed
       Score : 5.31 / 6.0
       Why   : genre match (+1.0), mood match (+1.0), energy similarity (+1.74)

  #2  Midnight Coding  —  LoRoom
       Genre: lofi  |  Mood: chill
       Score : 3.61 / 6.0
       Why   : energy similarity (+1.84)

  #3  Dusty Road Home  —  The Riverbend Boys
       Genre: country  |  Mood: nostalgic
       Score : 3.53 / 6.0
       Why   : energy similarity (+1.90)

  #4  Tide & Time  —  Coral Drift
       Genre: reggae  |  Mood: dreamy
       Score : 3.53 / 6.0
       Why   : energy similarity (+1.96)

  #5  Focus Flow  —  LoRoom
       Genre: lofi  |  Mood: focused
       Score : 3.52 / 6.0
       Why   : energy similarity (+1.80)
```

**Finding — scores compress, categories dominate.** Coffee Shop Stories leads at 5.31 while #2–#5 sit within 0.09 points of each other (3.52–3.61) — essentially a four-way tie. With all numeric features at 0.5, every song is equally "close" and labels become the only real differentiator. The gap between #1 and the field (1.70 pts) is entirely due to Coffee Shop Stories matching both genre and mood labels.

---

## Limitations and Risks

- **Tiny catalog.** 18 songs is far too small for meaningful variety. Most genres have exactly one entry, so the genre bonus almost always resolves to the same single song with no competition.
- **No audio understanding.** The system reads numbers from a CSV file. It does not listen to music. All feature values (energy, valence, acousticness) were assigned by hand and reflect one person's judgment, not measured audio properties.
- **Label brittleness.** Genre and mood are exact string matches. A user who types "Lo-Fi" instead of "lofi" earns zero genre bonus. Adjacent moods like "chill" and "relaxed" share no credit despite overlapping heavily in practice.
- **Silent failures.** When the system cannot find a good match — missing genre, sparse valence range, conflicting preferences — it returns results anyway with no warning. The output looks the same whether the top result is excellent or just the least-bad option.
- **No session memory.** Every run is stateless. The system cannot exclude songs you just heard, adapt to a changing mood within a session, or learn from skips and replays.

See [model_card.md](model_card.md) for a full bias analysis including the lofi filter bubble, genre equity gap, and dark valence desert.

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



