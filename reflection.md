# Reflection: Profile Comparisons

---

## Pair 1 — High-Energy Pop vs Chill Lofi

These two profiles are near-opposites on every axis, and the results reflect that clearly.

The High-Energy Pop listener got Sunrise City at #1 — a bright, upbeat pop song at energy 0.82. The Chill Lofi listener got Library Rain at #1 — a quiet, warm, acoustic track at energy 0.35. The two top results share almost nothing: different genre, opposite energy, different production style.

What this tells us is that energy is doing its job as the primary axis. When you move the energy target from 0.88 down to 0.38, the entire top-5 list shifts — not just #1, but every position. High-energy tracks like Gym Hero and Zenith Drop, which appeared in the Pop top-5, disappear completely and are replaced by low-energy tracks like Focus Flow and Spacewalk Thoughts.

Why does this make sense? Energy is essentially the volume dial of your emotional experience with music. A person who wants calm study music and a person who wants music to run to are looking for completely different things, and the numbers capture that gap accurately.

---

## Pair 2 — Deep Intense Rock vs Ghost Genre (k-pop)

These two profiles have very similar numeric preferences — both want high energy (0.92 vs 0.80), bright-to-mid valence, and low acousticness — but one has a genre that exists in the catalog (rock) and one does not (k-pop).

The Rock listener got Storm Runner at #1 with a score of 5.91 out of 6.0. The k-pop listener got Sunrise City at #1 with a score of only 4.89 out of 6.0.

The difference is entirely the genre bonus. Storm Runner earned an extra point just for being labeled "rock," which pushed it far ahead of the field. The k-pop listener got no such bonus — no song in the catalog is labeled k-pop — so the system had to rely purely on which songs happened to have similar energy and mood values.

The practical effect: the Rock listener's #1 result was clearly the best possible answer. The k-pop listener's #1 result was a reasonable substitute, but the system offered no acknowledgment that it was a substitute. Imagine going to a restaurant, asking for Thai food, and being served Italian because it was the closest thing they had — without being told Thai was unavailable. That is what this system does to the k-pop listener.

---

## Pair 3 — Chill Lofi vs Energy-Mood Conflict

This is the most revealing comparison because both profiles share a mood preference of "chill," but one has a matching energy (0.38) and the other has a completely contradictory energy (0.95).

The Chill Lofi listener got Library Rain at #1 — quiet, warm, acoustic. Makes sense.

The Energy-Mood Conflict listener also got Spacewalk Thoughts (ambient, chill) at #1 — even quieter than Library Rain, with energy only 0.28. This is a listener who asked for energy=0.95 — essentially the opposite of quiet.

Why did this happen? Because the genre label "ambient" and mood label "chill" together earned 2.0 points in bonuses, which is the same maximum contribution as the energy feature. The system saw the labels match and rewarded the song before checking whether the energy was anywhere close to what was requested.

This is not a small rounding error. The winning song (energy=0.28) and what the user actually wanted (energy=0.95) are 0.67 apart on a 0-to-1 scale — more than two-thirds of the full range. In plain terms: the user asked for a fast, pumping track and the system recommended something you would play in a quiet meditation room.

This is the clearest example of why label-matching can trick a scoring system. A human who read the request would immediately know the conflict. The algorithm read two matching words and stopped there.

---

## Pair 4 — Deep Intense Rock vs Dead Centre

The Rock listener gave the system a very clear signal: high energy, dark tone, raw sound, intense mood. The Dead Centre listener gave the system no useful signal at all — every preference was set to exactly 0.5, the midpoint.

The difference in results is dramatic. The Rock listener's top-5 covered a range of scores from 5.91 down to 3.39 — a spread of 2.52 points. The Dead Centre listener's top-5 ranged from 5.31 down to 3.52 — a spread of 1.79 points, and positions #2 through #5 were packed within 0.09 points of each other.

What this means: a decisive listener gets a decisive ranking. The system has a clear winner and a clear order. An indecisive listener — or one with genuinely eclectic taste — gets a pile of results that are essentially equivalent, and the top result only "won" because its genre label happened to match.

This matters for real systems. Spotify and YouTube do not show you a single ranked list and say "here are your top 5." They run additional logic to inject diversity, surface new artists, and avoid showing you five nearly identical songs. This simulation has none of that. For the Chill Lofi listener, positions #1, #2, and #3 were all lofi songs. That is a filter bubble forming in real time — the system optimized for its own scoring rules rather than for what a human would experience as a satisfying and varied set of suggestions.

---

## Overall Observation

Looking across all six profiles, one pattern holds consistently: the system works best when the user's preferences are specific, internally consistent, and represented in the catalog. The moment any of those three conditions breaks — the preferences are vague, they contradict each other, or the genre does not exist — the recommendations become a best-guess with no transparency about why the guess was made.

Real recommenders handle this with fallback logic, explanations, and catalog coverage metrics. This simulation does not, which makes it a useful teaching tool for understanding exactly why those features exist in production systems.
