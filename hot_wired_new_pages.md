# Hot Wired — Draft Pages, Batch 1

Each block below is written to slot into the existing playtest PDF. The bracketed note under each heading says what it replaces or where it inserts. Numbers (Crypto costs, Downtime action count, Heat thresholds) are first-pass and meant to be tuned at the table.

---

## [Task Roll] — revised resolution rule
**Replaces the "Scoring a Hit / A Miss / A Push" bullets on page 4.**

Both pools are rolled and the results are compared to determine the outcome of the Task. Each die showing a **1 or a 6** counts as a Success.

*(Anything can go sideways in The City, sometimes in your favor. A rolled 1 isn't clean skill, it's a glitch: a misfire that still grazes, a guard's reflexes failing half a second too late. Narrate 1-successes as something breaking weird, not as a sharpshooter's instinct.)*

- **Scoring a Hit** - If there are more Successes in the Boost pool than the Challenge pool, score Hits equal to the difference. [We call additional Hits after the first, "Bonus Hits"]
- **A Miss** - If there are more Successes in the Challenge pool than the Boost pool, score no Hits and suffer a Consequence.
- **A Push** - If there are the same number of Successes in both pools [including 0], score 1 Hit and also suffer a Consequence.

---

## [Grit] — addendum
**Insert as a second paragraph under the existing Grit rule on page 6.**

Because Grit is spent at the player's discretion, it only ever helps: it adds to a die's result, it never subtracts, so it can turn a non-Success into a 6 but it can never turn a 1 into something worse. In practice, players spend Grit on dice sitting at 5 (cheapest, 1 Grit) or stack it on a 2, 3, or 4 when the extra cost is worth it. There's never a reason to spend Grit on a die that's already showing a 1.

---

## [Riskometer & Heat]
**Replaces the "Riskometer Level [0-2]" bullet on page 4 and the standalone [Riskometer] section at the end of the book. One track, defined once.**

**Heat** is the unit of danger and attention a crew accumulates during a Gig: noise made, witnesses left, alarms tripped, faces seen. The **Riskometer** is the 0-15 gauge that tracks it.

Add 1 Challenge Die to the Challenge Pool for every 5 Heat the crew has accumulated, rounded down. At 15 Heat, the current Gig collapses. Narrate what happened (the crew gets made, the building goes into lockdown, the law shows up in force) and cut to the consequences.

**Gaining Heat**
The GM adds Heat once per Gig for each of the following, as fits the situation:

- +1 Heat - Public use of firearms.
- +1 Heat - Massive property damage.
- +1 Heat - Destroying or stealing notable corporate assets.
- +1 Heat (+1 more if the body belonged to someone rich or notable) - Dropped bodies.
- +1 or more Heat - Failed Flashbacks.
- GM's call - Failures during a Gig often give the player a choice between Heat and a different Consequence instead.

**Heat between Gigs**
Heat does not reset on its own. It carries from one Gig into the next until the crew buys it down during Downtime (see [Downtime]: Reduce Heat, ¢50 per PC per point of Heat removed).

---

## [Down]
**Insert into [Conditions and Injuries], directly before "PC Death."**

A PC carrying **3 unstabilized Injuries is Down**: unconscious, pinned, or otherwise removed from active participation in the scene until stabilized. A Down PC can be Stabilized by another PC's aid (a standard Task Roll, per *Stabilize an Injury*) or by Medical Treatment during Downtime.

If a Down PC suffers a **4th** unstabilized Injury before being Stabilized, that's the kind of extreme circumstance PC Death is built for.

A GM looking to apply pressure against a PC who is Down, but who isn't ready to call for PC Death, can advance the Riskometer instead. That keeps the danger of the moment real without requiring more rolls against a character who's already out of the fight.

---

## [Gigs]
**New section, inserted directly before [Downtime] (below), replacing the near-empty page 27.**

A Gig is the basic unit of play in Hot Wired: a job, score, or mission the crew takes on, usually offered by a Fixer, a corporate handler working an angle, a gang contact calling in a favor, or some desperate Have-Not who scraped together enough Crypto to ask for help. Most sessions run one Gig from offer to payout.

**The shape of a Gig**
1. **The Offer** - the crew hears about the job and decides whether to take it.
2. **The Job** - the crew executes, generating Hits, Consequences, and Heat along the way.
3. **The Payout** - on success (or partial success), the crew gets paid.
4. **Downtime** - the crew spends what they earned and prepares for the next Gig.

**Payout**
A Gig pays a base of **¢300 per PC** on a clean success, modified by:

- **+¢100 per PC**, for each tick of Heat the crew knowingly risked taking on going into the job (dangerous jobs pay more)
- **+¢100 to ¢500 per PC**, for cleanly completed bonus objectives (GM's call, scaled to difficulty)
- **-25% to the base payout** if the central objective failed but the crew survived

A Suicide Mission pays, by definition, enough to clear the crew's debts and cover everyone's medical care.

---

## [Downtime]
**New umbrella section. Buy/Build, Medical Treatment, and Reduce Heat already exist in the book (pages 28-30) and slot in underneath this as written; nothing about them changes.**

Between Gigs, the crew gets time to spend what they earned, patch themselves up, and get ready for whatever's next. This is Downtime.

Each PC gets **2 Downtime Actions** (GMs should feel free to adjust this for pacing). Each action is spent on one of the following:

- **Acquire or Build Kit** - buy or build Primo Kit, Cyberware, Programs, Drugs, Mags, or Grenades.
- **Get Medical Treatment** - heal Injuries or install Cyberware.
- **Reduce Heat** - spend Crypto to buy down the crew's accumulated Heat.
- **Train** - swap a Background or Skill Description for one that better fits who the character has become.
- **Lay Low** - clear 1 Condition. No roll required, just describe how your character works through it in the gap between jobs.

PCs don't have to spend both actions the same way, and not every PC has to spend both. When the crew is done with Downtime, the next Gig begins.

---

## [Clocks]
**Insert as a short addition after the paragraph ending "...commit to the Task," on page 5.**

For any Task that requires more than 1 Hit and is likely to take more than one roll to resolve, track progress with a **Clock**: a circle divided into segments equal to the Hits required. Fill in 1 segment per Hit scored. A Clock keeps accumulating progress visible to the whole table, and works equally well for breaking into a safe, hacking a hardened network, talking down a hostile boss, or grinding through a tough enemy in a fight.

---

### Batch 2 — done, live in the redesigned rulebook
All of this batch went straight into the redesigned HTML rulebook rather than staying as markdown, since that's the version being kept current: retroboomgames.com/hot-wired/rulebook.html

- **Bugs table** — fixed to a clean 1d6 (column) then 1d10 (row) roll.
- **Boose Dice / VR capitalization typos** — fixed.
- **Drugs section** — every Boost now has a name and a specific quirk (Redline, Knuckle, Glasswire, Jackrabbit, Bull, Steady, Permafrost, Cinder, Flatline), closing the "1 specific Boost and 1 specific quirk" promise the original text made but never delivered on.
- **Quick Reference Sheet** — new Part 09, a condensed one-page cheat sheet (Task Roll, Boost/Challenge sources, ranges, fight quick-bits, Downtime actions).
- **Character sheet** — new blank, fillable sheet (on-screen or printed): Backgrounds/Skill Descriptions to the 8-point budget, Bugs, Cyberware, Grit, Kit, Conditions/Injuries, Crypto/Heat.
- **Pre-generated crew** — four ready-to-play PCs (Dash, muscle; Ohm, netrunner; Marisol Vale, the face; Bricks, techie/medic), each built to the same 8-point / 3-Cyberware-Boost budget as a player would use, doubling as worked examples of the Skill Description math.

### Still open
Nothing structural left from the original audit. Anything from here is refinement: more pre-gen crew, GM-side gig/NPC generation tables, or further balance tuning once this gets played.
