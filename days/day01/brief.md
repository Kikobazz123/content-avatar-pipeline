# Writing brief — Day 1
**Topic:** Why I stopped looking for clients
**Screen recording:** terminal, empty project
**Angle:** Show it running on your machine. You are a backend developer; the terminal is the proof.
**Close:** "I build AI automations for Nigerian businesses. Link's in my bio." One line, then stop talking.

---

## Structure

```
1. FRAME ZERO — the finished artifact, on screen, before a word is spoken.
   Not a title card, not your face alone, not "hey guys". Reference A opened on
   a website the viewer assumes is Apple's; Reference B opened on a terminal
   that had already printed its result.

2. THE PROMISE — complete, inside 3 seconds, spoken over that visual.
   A: "Here's how I build 3D animated websites with Claude Code."  (0.0-2.7s)
   B: "Google's new tool lets you connect to anything instantly."  (0.0-2.8s)

3. RETENTION DEVICE — pick exactly one:
   (a) DECEPTION-REVEAL — let the viewer believe something for 10-15s, then
       turn it. A spent 11 seconds narrating "Apple's site" before saying
       "this website is not Apple". Use when your result looks like it came
       from somewhere more established than you.
   (b) DELAYED AGITATION — name the pain at roughly 35% in, once they are
       already invested. B waited until 0:40 to say "it literally just looks
       like raw markdown and it's obviously horrible". Use when demoing a
       tool that fixes a known annoyance.

4. MECHANISM, NAMED AGAINST WHAT THEY TRIED — B: "not via API call, not via
   MCP, but via a bash command." Name the thing, and contrast it with the two
   approaches the audience already failed with. This is the credibility beat.

5. CLOSE — soft CTA on days 1-29, hard ask on day 30 only.
```

## Hard rules

- Never claim a client, revenue figure, or result that has not happened.
  LordGen is pre-launch with no live agents. One invented win destroys the
  value of every honest episode.
- One idea per episode. Both references carry exactly one.
- Write for the mouth. Read it aloud; if it needs a second breath mid-sentence,
  cut it.
- Target 90-150 seconds. Both references run near two minutes, not thirty
  seconds — Shorts allow three.
- Every angle routes through the market, the build, or the reason. Generic
  global AI commentary competes with saturated content and loses.


---

## Voice spec

# Voice spec — Lordmark Dorgu

The script writer reads this file before drafting anything. It is the difference
between scripts in his voice and generic AI copy.

**Status: v0, inferred.** Everything below was derived from his two published
TikToks — spoken transcripts, burned-in captions, and post copy. None of it has
been confirmed by him yet. Days 1–3 exist to correct it. When he rejects a line,
write down *why* here; a rejection with no reason teaches nothing.

---

## Who he is, in his own words

- "I'm a backend developer" — states it plainly, never "engineer" or "founder"
- "Instead of pretending to be an AI guru" — the anti-positioning is explicit and load-bearing
- "I'm documenting everything from day one. I'll document my wins, my mistakes, my projects"
- On why: "I got tired of looking for clients. I wanted to be the thing companies need."
- On the market: "Africa is an oil well. Untouched technical ground. Bring real capability here and you don't compete, you stand out."

## How he actually talks

**Sentence length is short.** Spoken and written both. "It isn't." stands alone as a sentence in his own caption copy.

**Second person, constantly.** "I know *you* hear a lot of AI…", "Which mistake have *you* made before?" He talks to one person, not an audience.

**Opens on a shared frustration, not a claim.** Video 1 begins with the confusion the viewer already feels before he says anything about himself.

**"Right?" as a spoken beat.** "I am starting a journey, right?" Keep it in spoken scripts, drop it from written captions.

**Admits things.** "I trusted AI." "I even started posting like you saw in my previous post." The mistakes are told in first person with no hedging.

**Closes with an invitation, not a command.** "If you're also learning about AI, let's work together, follow this journey." Not "SMASH THAT FOLLOW."

## Written captions vs spoken script

His written copy is noticeably more polished than his speech. Both are correct — they are different registers, and scripts should be written for the mouth, not the page.

- Written: *"Most people think using AI is just about asking questions. It isn't. The way you prompt, verify, and collaborate with AI determines whether you save hours—or waste them."*
- Spoken: *"I know you hear a lot of AI apps, AI automation, AI design, AI data and you don't quite understand what is happening."*

## Formatting conventions he already uses

- Burned-in captions: ALL CAPS, one word accented at a time
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

<!-- Day 01 — pending -->
<!-- Day 02 — pending -->
<!-- Day 03 — pending -->

---

## Deliverable

Write the spoken script only — no shot directions, no stage notes, no
emoji. Plain lines, one sentence per line, exactly as it will be said.
Save it to `days/dayNN/script.txt` so `captions.py --script` can use it
as ground truth; Whisper mishears this accent badly and its wording must
never reach the screen.
