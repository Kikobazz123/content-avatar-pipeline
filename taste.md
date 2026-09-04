# Voice spec — Lordmark Dorgu

The script writer reads this file before drafting anything. It is the difference
between scripts in his voice and generic AI copy.

**Status: v1, three videos.** Derived from his three published TikToks —
spoken transcripts, burned-in captions, and post copy. Still observed rather than
confirmed by him. When he rejects a line, write down *why* here; a rejection with
no reason teaches nothing.

Sources: *Building My AI Business From Scratch* (55s), *The biggest Mistake
Beginners make when using A.I* (100s), *Building an A.I business from scratch
Day 1 (Preview)* (83s, watched 2026-09-04).

---

## Who he is, in his own words

- "I am a backend developer **and I am an A.I automation specialist**" — as of the
  third video he claims the specialist title outright. Stronger than the earlier
  "backend developer" alone, and the phrasing to use going forward.
- "I'm a backend developer" — states it plainly, never "engineer" or "founder"
- "Instead of pretending to be an AI guru" — the anti-positioning is explicit and load-bearing
- "I'm documenting everything from day one. I'll document my wins, my mistakes, my projects"
- On why: "I got tired of looking for clients. I wanted to be the thing companies need."
- On the market: "Africa is an oil well. Untouched technical ground. Bring real capability here and you don't compete, you stand out."

## How he actually talks

**Sentence length is short.** Spoken and written both. "It isn't." stands alone as a sentence in his own caption copy.

**Second person, constantly** — but the number moves. Videos 1-2 address one
person ("Which mistake have *you* made before?"); video 3 switches to "you guys"
throughout. Both are his. Use singular for reflective or mistake episodes, "you
guys" when he is showing something off.

**Repeats a number to land it.** "I have created nine different projects — *yes,
nine different projects*." Also "yes, I do all of that." The repeat is the
emphasis; do not smooth it out into one clean sentence.

**Names what it is not, before what it is.** "I'm not talking about using ChatGPT
to create pictures or making videos or whatever — I'm talking about real stuff."
He reaches for this contrast unprompted, and it is the same credibility beat the
163k references use. Lean into it.

**Money framing at the close.** Video 3 ends "this is real business, this is real
money." Blunter than videos 1-2, and it is his own instinct rather than something
suggested to him.

**Opens on a shared frustration, not a claim** — in videos 1-2. **Video 3 breaks
this**: it opens "Hello everyone, my name is Lordmark, I am a backend developer
and I am an A.I automation specialist", and the actual hook ("nine different
projects") does not arrive until ~28s. See the corrections log — this is the
single biggest thing to fix in the next episode.

**"Right?" as a spoken beat.** "I am starting a journey, right?" Keep it in spoken scripts, drop it from written captions.

**Admits things.** "I trusted AI." "I even started posting like you saw in my previous post." The mistakes are told in first person with no hedging.

**Closes with an invitation, not a command.** "If you're also learning about AI, let's work together, follow this journey." Not "SMASH THAT FOLLOW."

## Written captions vs spoken script

His written copy is noticeably more polished than his speech. Both are correct — they are different registers, and scripts should be written for the mouth, not the page.

- Written: *"Most people think using AI is just about asking questions. It isn't. The way you prompt, verify, and collaborate with AI determines whether you save hours—or waste them."*
- Spoken: *"I know you hear a lot of AI apps, AI automation, AI design, AI data and you don't quite understand what is happening."*

## Formatting conventions he already uses

- Burned-in captions: ALL CAPS, one word accented at a time
- **The accent colour and position keep changing** — v1 cyan text, top-centre;
  v2 cyan box, top; v3 red box, bottom-centre. No template is locked yet. Pick
  one and keep it, or the videos stop reading as a set. `repurpose/brand.json`
  currently assumes cyan.
- 🚨 to open a caption; 👇 before an engagement question
- Engagement close: "Which mistake have you made before? Be honest in the comments."
- Hashtags: `#fyp` plus niche tags — `#learnai #aiconsulting #techcareer #techcreator #learnontiktok #aitrend`

## Rules for the script writer

1. **Never claim a client, a revenue figure, or a result that has not happened.** LordGen is pre-launch with no live agents. The honesty is the differentiator — one invented win destroys the value of every honest episode.
2. **Open on the artifact, not the topic.** Frame zero shows the finished thing. This is the single strongest pattern from the two 163k reference videos.
3. **Full promise inside three seconds.** Both references land theirs by 2.8s.
4. **Write for the mouth.** Read it aloud; if it needs a second breath mid-sentence, cut it.
5. **One idea per episode.** Both references carry exactly one.
6. **Close soft on days 1–29** — "I build AI automations for Nigerian businesses. Link's in my bio." The hard ask is day 30 only.
7. **His accent breaks Whisper.** Always pass the written script to `captions.py --script`; never let ASR wording reach the screen.

## Words and moves to avoid

- "Guru", "expert", "secrets", "hack your way to" — he explicitly rejects this posture
- "Game-changer", "insane", "you won't believe" — competitor register, not his
- Any implication he has clients, income, or a track record yet
- Generic global AI commentary with no Nigerian or personal angle — that competes with saturated content and loses

---

## Corrections log

Append one entry per rejected draft. Format: what was written, what he changed it
to, and why. This section is what makes the writer improve rather than repeat.

**2026-09-04 — from video 3 ("Day 1 Preview", 83s, 319 views).**

- **The first 9 seconds are name and job title.** That is the cold open both 163k
  reference videos deliberately avoid, and the real hook — "nine different
  projects" — is buried at 28s. On a 83s video that is a third of the runtime
  spent before the reason to watch. *Fix:* lead with the nine projects, and let
  the name arrive after, or not at all. Nobody scrolling knows or needs it yet.
- **"A.I automation specialist" is a real upgrade** over "backend developer"
  alone. Keep it.
- **Still no screen recording.** Three videos, three pure talking heads. He has
  the artifacts now — this is the highest-value change available and it costs
  nothing.
- **Caption style changed again** (red box, bottom). Third style in three videos.
- He independently used "nine projects" and the laptop angle from the day01
  script, so that framing landed with him. Keep using it.

<!-- Day 02 — pending -->
<!-- Day 03 — pending -->
