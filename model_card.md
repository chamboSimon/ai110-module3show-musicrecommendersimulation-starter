# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
