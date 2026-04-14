# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

A content-based music recommender that scores songs by how closely their sonic features match a listener's stated taste preferences.

---

## 2. Intended Use

VibeFinder 1.0 is designed to suggest songs from a small catalog based on a user's self-described taste — things like how energetic, emotionally bright, or acoustic they want their music to be. It is built for classroom exploration and learning, not for real users or production deployment.

The system assumes the user can describe their preferences numerically. It does not learn from listening history or adapt over time. Each recommendation is a one-shot calculation with no memory of previous sessions.

**What it is for:**
- Demonstrating how content-based filtering works
- Exploring how different feature weights change recommendation behavior
- Understanding why scoring systems can produce unexpected or biased results

**What it is not for:**
- Discovering new or niche artists (the catalog is too small)
- Replacing human curation or editorial playlists
- Making recommendations for real listeners in a real product
- Any context where fairness, diversity, or catalog completeness actually matters

---

## 3. How the Model Works

Think of each song as having a report card with six scores: how energetic it is, how emotionally bright or dark it sounds, how acoustic or electronic the production feels, how groovy and rhythmic it is, what genre it belongs to, and what mood it has.

When a listener says what they want — "I want something calm, warm, and acoustic" — the system compares that description to every song's report card. Songs that are closer to the description score more points. Songs that are far away score fewer.

Genre and mood work slightly differently. Instead of measuring distance, they award a flat bonus if the label matches exactly. A song labeled "lofi" earns an extra point for a user who says they like lofi. A song labeled "chill" earns an extra point for a user who says they want chill. If neither label matches, no bonus is awarded.

After every song is scored, the list is sorted from highest to lowest, and the top five are returned as recommendations.

The key design choice is that **energy carries the most weight**. Being close to the user's requested energy level is worth up to 2.0 points out of 6.0. Genre and mood each contribute at most 1.0 point. This reflects the idea that energy — how calm or intense a song feels — is the feature listeners notice most when a recommendation feels wrong.

---

## 4. Data

The catalog contains **18 songs** stored in a CSV file. Ten songs came from the project starter; eight were added to improve coverage.

**What is represented:**
- 15 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, r&b, country, metal, reggae, edm, blues
- 14 moods: happy, chill, intense, relaxed, focused, moody, energized, serene, romantic, nostalgic, angry, dreamy, euphoric, melancholic
- Six numeric features per song: energy, valence (emotional brightness), acousticness, danceability, tempo in BPM

**What is missing:**
- Most genres have only one song. Lofi is the exception with three.
- There are almost no songs in the low-valence (dark/sad) range. Only two songs score below 0.40 on valence.
- No lyrics, no audio files, no images, no artist metadata beyond a name.
- All songs are fictional. The catalog reflects the choices of one person building an exercise, not real listener data.
- No songs representing genres common in non-Western music markets (Afrobeats, K-pop, Latin trap, Bollywood).

---

## 5. Strengths

The system works well when the user's preferences are clear and the catalog has a matching song.

For the three core profiles tested — High-Energy Pop, Chill Lofi, and Deep Intense Rock — the top result in every case was obviously correct and scored above 5.5 out of 6.0. The system cleanly separated opposite listener types: the pop listener's top results share nothing with the lofi listener's top results, which is exactly what should happen.

The scoring is fully transparent. Every point is explained — you can see exactly why a song ranked where it did. There are no hidden layers, no black box decisions, and no randomness. This makes it easy to understand and debug, which is useful for learning.

The system also handles features correctly as a matter of proximity, not magnitude. It does not recommend the loudest or most energetic songs by default. It recommends the songs closest to whatever the user asked for, whether that is high energy or low.

---

## 6. Limitations and Bias

**Primary weakness — categorical bonuses override the primary perceptual axis.**
The genre and mood bonuses together award up to 2.0 fixed points, while energy — the feature users feel most consciously — can contribute at most 2.0 points only when the match is perfect. In adversarial testing, a song with energy=0.28 ranked #1 for a user who requested energy=0.95, purely because it matched on genre and mood labels; the energetically correct song (energy=0.91) was buried at #4. This means the system can be "tricked" by any user whose genre preference conflicts with their energy preference — a real pattern for listeners who want, for example, calm ambient music during a workout.

**Lofi filter bubble.**
Lofi is the only genre with three catalog entries (17% of all songs), and all three sit in a narrow low-energy band (0.35–0.42). Any user who prefers low energy — regardless of whether they like lofi — will see lofi songs dominate positions #2 and #3 in almost every run. This is not because lofi is the best match; it is because it is the only genre with enough catalog depth to compete numerically. A listener who prefers quiet classical or acoustic blues is silently funneled toward a genre they may not want.

**Genre equity gap — absent genres carry a permanent scoring penalty.**
Thirteen of the fifteen genres in the catalog appear exactly once. A user whose preferred genre is not represented at all (k-pop, folk, trap, bossa nova) can never earn the +1.0 genre bonus, reducing their maximum achievable score from 6.0 to 5.0 with no explanation given. In a real system this would systematically under-serve listeners from musical cultures outside the catalog's implicit demographic, which skews toward Western popular and electronic genres.

**Dark valence desert.**
Only two songs have valence below 0.40 — Iron Collapse (0.25) and Empty Porch Blues (0.32). A user who prefers emotionally dark or melancholic music will always receive recommendations that score numerically adequate but feel emotionally wrong, because the catalog simply has no density in that quadrant. The system has no mechanism to signal this gap, so it silently substitutes mid-valence songs without transparency.

**No diversity control.**
The ranking is a pure score sort with no penalty for repeated artists, genres, or adjacent moods. In a catalog this small, the top 5 results can cluster entirely within one or two genres whenever the genre bonus fires, producing a list that feels narrow even when other areas of the catalog might provide genuine variety.

---

## 7. Evaluation

Six user profiles were run against the 18-song catalog. Three were normal listener types — High-Energy Pop, Chill Lofi, and Deep Intense Rock — and three were adversarial profiles built to expose weaknesses.

**What we tested and what we were looking for:**
For the core profiles, the check was simple: does the #1 result feel obviously correct for that listener type? For the edge profiles, the check was whether the scoring logic would break under pressure — a user with contradictory preferences, a user whose favorite genre does not exist in the catalog, and a user with no strong opinion on any feature.

**What the results confirmed:**
The three core profiles all returned an obvious, correct #1 — Sunrise City for pop, Library Rain for lofi, Storm Runner for rock. The ordering made intuitive sense and the scores were high (above 5.5 out of 6.0), meaning the top result was a strong match, not just the least-bad option.

**What surprised us:**

*The chill mood bonus beat the energy axis.* In the Energy-Mood Conflict profile (energy=0.95, mood=chill), the system ranked Spacewalk Thoughts — a very quiet, calm ambient track — at #1. The user had asked for something intense. The reason is that Spacewalk Thoughts matched on both genre (ambient) and mood (chill), earning 2.0 points from labels alone, which outweighed the energy penalty of recommending a near-silent track to someone who wanted high energy. The system was technically following the rules, but the result would feel completely wrong to a real user.

*The Dead Centre profile revealed that labels decide everything when numbers say nothing.* When all numeric preferences were set to the neutral midpoint (0.5), the scores for positions #2 through #5 collapsed into a 0.09-point band — essentially a four-way tie. The only thing that separated the songs was whether their genre or mood label matched. Coffee Shop Stories jumped to 5.31 out of 6.0 while the next song scored 3.61 — a gap of 1.7 points — purely because it happened to be a jazz track with a "relaxed" mood label. This shows that a user with genuinely neutral or eclectic taste would get results that feel arbitrary.

*The Ghost Genre profile showed that missing catalog coverage is invisible to the user.* A listener who wants k-pop got Sunrise City (a pop song) at #1 with a score of 4.89 out of 6.0, and the system gave no indication that their actual preference was never represented. In a real app, this would silently funnel a k-pop fan toward Western pop without explanation.

---

## 8. Ideas for Improvement

**Expand catalog depth per genre.**
The single most impactful change would be adding at least 3–5 songs per genre instead of one. Right now the genre bonus always points to the same single song. With more songs per genre, the numeric axes could actually differentiate between good and great matches within a genre — which is how real recommenders work.

**Add a catalog gap warning.**
When a user's preferred genre does not exist in the catalog, the system should say so. Something like "No [k-pop] songs in catalog — showing closest numeric matches instead" would tell the user why their results look different from what they asked for. Silence is the wrong default here.

**Add a diversity rule to the ranking.**
Before returning the top 5, check whether any genre or artist appears more than twice. If it does, swap the lower-ranked duplicate out for the next highest-scoring song from a different genre. This prevents the lofi filter bubble and makes the list feel more like a playlist than a repetition.

---

## 9. Personal Reflection

Building this system made it clear that recommendation is not really about finding "the best song" — it is about defining what "best" means precisely enough for a computer to calculate it. Every weight, every bonus, every scoring rule is a decision about whose taste matters and how much. Those decisions have consequences that are easy to miss until you run the wrong profile and see a quiet ambient track recommended to someone who wanted something loud.

The most surprising discovery was how easily a word can override a number. Two matching labels — genre and mood — consistently beat a large energy gap. This makes sense mathematically once you see the weights, but it does not match how humans actually experience music. A person who says "I want something chill" and "I want energy 0.95" has a contradiction in their request, but the system does not notice the contradiction — it just adds up points. Real systems must catch this with additional logic that this simulation does not have.

This changed how I think about apps like Spotify or YouTube Music. When a recommendation feels wrong, it is usually not a bug — it is the system following its own rules correctly, but the rules were not designed with that edge case in mind. Every recommendation engine is really a set of assumptions about what listeners value, encoded as numbers. The assumptions that go unexamined are the ones that cause the most frustrating results.
