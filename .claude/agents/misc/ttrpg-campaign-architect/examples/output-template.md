# Campaign Output Template

**Purpose**: Standard structure for all ttrpg-campaign-architect outputs. Use this template when generating campaign materials.

---

## Template Structure

Every output follows this hierarchy:

```
Campaign: [Name]
├── World Elements (if world_building or both)
│   ├── Setting Overview
│   ├── Geography
│   ├── Creatures & Species
│   ├── Factions
│   └── Magic Systems
├── Story Buckets (if story_building or both)
│   ├── Early Game
│   ├── Mid Game
│   └── End Game
├── SCAMPER Iterations (if scamper_refine)
└── GM Notes
```

---

# FIELD REQUIREMENTS LEGEND

**Required** (✱) = Must be filled before export
**Optional** (○) = Include when user provides info or when relevant

---

# WORLD ELEMENTS TEMPLATE

## Setting Overview

```yaml
setting:
  name: "[Campaign/World Name]"                    # ✱ Required
  genre: "[genre]"                                 # ✱ Required
  tone: "[tone]"                                   # ✱ Required
  key_themes:                                      # ✱ Required (1-3)
    - "[Theme 1]"
    - "[Theme 2]"
    - "[Theme 3]"
  brief_overview: "[2-3 sentence world summary]"   # ✱ Required
  system_context:                                  # ○ Optional - only if user provides
    system_name: "[D&D 5e, Pathfinder 2e, Custom, etc.]"
    source_provided: "[rulebook, character sheet, verbal, etc.]"
    key_mechanics: ["[Relevant rules that affect world design]"]
```

## Geography

**Format for each location**:

```yaml
geography:
  - name: "[Location Name]"                        # ✱ Required
    type: region | landmark | route | settlement   # ✱ Required
    description: "[1-2 sentences]"                 # ✱ Required
    key_features:                                  # ✱ Required (2-3)
      - "[Distinctive feature 1]"
      - "[Distinctive feature 2]"
      - "[Distinctive feature 3]"
    connections: ["[Connected locations]"]         # ○ Optional
    plot_hooks: ["[Story connection]"]             # ○ Optional
    system_details:                                # ○ Optional - if system provided
      encounter_level: "[Appropriate party level]"
      hazards: ["[System-specific environmental rules]"]
```



## Creatures & Species

**Format for each creature/species**:

```yaml
creatures_species:
  - name: "[Name]"                                 # ✱ Required
    type: creature | species | race                # ✱ Required
    description: "[1 sentence]"                    # ✱ Required
    physical_traits:                               # ✱ Required (1-2)
      - "[Trait 1]"
      - "[Trait 2]"
    behaviors:                                     # ○ Optional
      - "[How they act/react]"
      - "[Notable patterns]"
    habitats: ["[Where found]"]                    # ○ Optional
    cultural_significance: "[How society views]"   # ○ Optional
    system_stats:                                  # ○ Optional - if system provided
      stat_block: "[Follow user's system format]"
      abilities: ["[System-specific abilities]"]
      challenge: "[CR, Level, or equivalent]"
```

## Factions

**Format for each faction**:

```yaml
factions:
  - name: "[Faction Name]"                         # ✱ Required
    type: political | religious | mercantile | etc # ✱ Required
    goals:                                         # ✱ Required (1-2)
      - "[Primary objective]"
      - "[Secondary objective]"
    resources:                                     # ○ Optional
      - "[Asset 1]"
      - "[Asset 2]"
    key_figures:                                   # ○ Optional (1-2)
      - "[Name] - [1-line role description]"
    relationships:                                 # ○ Optional
      allies: ["[Faction name]"]
      enemies: ["[Faction name]"]
    tension_points:                                # ○ Optional
      - "[Internal or external conflict]"
```

## Magic Systems

**Format for magic/special rules**:

```yaml
magic_systems:
  - name: "[System Name]"                          # ✱ Required
    source: "[Where power comes from]"             # ✱ Required
    costs:                                         # ✱ Required (1-2)
      - "[What using it requires]"
      - "[Price paid]"
    limitations:                                   # ○ Optional
      - "[What it cannot do]"
      - "[Constraints on use]"
    societal_impact: "[How society relates]"       # ○ Optional
    system_mechanics:                              # ○ Optional - if system provided
      spell_schools: ["[System-specific categories]"]
      casting_rules: "[How magic works mechanically]"
```

---

# STORY BUCKETS TEMPLATE

## Early Game

```yaml
early_game:
  phase_summary: "[What this phase accomplishes narratively]"
  sessions_estimate: "1-4"
  plot_hooks:
    - name: "[Hook Title]"
      type: positive | negative | neutral
      trigger: "[What initiates this plot]"
      key_elements:
        - "[Critical detail 1]"
        - "[Critical detail 2]"
        - "[Critical detail 3]"
      potential_outcomes:
        - "[Direction A if players choose X]"
        - "[Direction B if players choose Y]"
```



## Mid Game

```yaml
mid_game:
  phase_summary: "[What this phase accomplishes narratively]"
  sessions_estimate: "5-12"
  escalation_plots:
    - name: "[Plot Title]"
      type: positive | negative | neutral
      trigger: "[What initiates this escalation]"
      key_elements:
        - "[Critical detail 1]"
        - "[Critical detail 2]"
        - "[Critical detail 3]"
      potential_outcomes:
        - "[Direction A]"
        - "[Direction B]"
      builds_on: ["[Early game hook name]"]
      stakes_raised: "[How stakes increase from early game]"
```

## End Game

```yaml
end_game:
  phase_summary: "[What this phase accomplishes narratively]"
  sessions_estimate: "13+"
  climactic_plots:
    - name: "[Climax Title]"
      type: positive | negative | neutral
      trigger: "[What brings this to a head]"
      key_elements:
        - "[Critical detail 1]"
        - "[Critical detail 2]"
        - "[Critical detail 3]"
      potential_outcomes:
        - "[Victory condition]"
        - "[Pyrrhic victory]"
        - "[Failure state]"
      resolves: ["[Thread from early/mid game]", "[Another thread]"]
```

---

# SCAMPER ITERATIONS TEMPLATE

**Format for each transformation**:

```yaml
scamper_iterations:
  - technique_used: "S | C | A | M | P | E | R"
    original_element:
      type: "[What kind of element]"
      content: "[The original idea]"
    transformed_element:
      type: "[Same type]"
      content: "[The new version]"
    rationale: "[Why this transformation improves the element]"
    improvement_assessment: "[What's better now]"
```

---

# CHARACTERS TEMPLATE

```yaml
characters:
  - name: "[Character Name]"                       # ✱ Required
    archetype: "[Archetype from framework]"        # ○ Optional
    background:
      origin: "[Where they're from]"               # ✱ Required
      defining_moment: "[What shaped them]"        # ✱ Required
      faction_connection: "[Faction/relationship]" # ○ Optional
    motivation:
      wants: "[Concrete external goal]"            # ✱ Required
      needs: "[Internal growth needed]"            # ✱ Required
      fears: "[Exploitable weakness]"              # ✱ Required
    relationships:                                 # ○ Optional (1-3)
      - npc: "[NPC Name]"
        type: ally | rival | complicated
        description: "[Brief description]"
    campaign_hooks:                                # ✱ Required
      early_game: "[Personal stake in opening]"
      mid_game: "[Complication that tests arc]"
      end_game: "[How story resolves]"
    system_stats:                                  # ○ Optional - if system provided
      class: "[Class/archetype in their system]"
      abilities: "[Stat array or key abilities]"
      skills: ["[Relevant proficiencies]"]
      equipment: ["[Starting gear]"]

party_dynamics:
  bonds:                                           # ○ Optional
    - characters: ["[Character A]", "[Character B]"]
      connection: "[What connects them]"
      tension: "[What creates friction]"
      growth: "[How they help each other]"
  shared_secret: "[Something 2+ know]"             # ○ Optional
  party_flaw: "[Collective weakness]"              # ○ Optional
```

---

# REVIEW TEMPLATE

```yaml
review:
  dreamer:
    verdict: pass | needs_work
    note: "[What inspires or what's missing]"
  realist:
    verdict: pass | needs_work
    note: "[What works or what's impractical]"
  critic:
    verdict: pass | needs_work
    note: "[What's solid or what has holes]"

  overall: ready | refine_recommended
  top_suggestion: "[Single highest-impact improvement, or 'None - ready to run!']"
```

---

# GM NOTES TEMPLATE

```yaml
gm_notes:
  session_zero_topics:
    - "[Topic to discuss with players before starting]"
    - "[Tone/content expectations]"
    - "[Character connection opportunities]"
  pacing_recommendations:
    - "[When to introduce X element]"
    - "[Signs players are ready for escalation]"
  optional_expansions:
    - "[Idea for extending campaign]"
    - "[Unexplored thread that could become major]"
  consistency_reminders:
    - "[Important world rule to maintain]"
    - "[Faction behavior pattern]"
```

---

# COMPLETE EXAMPLE

Below is a minimal but complete example showing proper structure:

```yaml
# Campaign: The Shattered Crown
# Genre: Dark Fantasy | Tone: Gritty

setting:
  name: "The Shattered Crown"
  genre: "dark fantasy"
  tone: "gritty"
  key_themes: ["survival", "moral ambiguity", "fallen glory"]
  brief_overview: "Once-great kingdom torn apart by civil war. Three factions 
    fight over fragments of the royal crown, each piece granting power."

geography:
  - name: "The Scar"
    type: landmark
    description: "Mile-wide chasm where the capital once stood"
    key_features:
      - Magical residue causes mutations in those who linger
      - Scavengers risk death for pre-war artifacts
      - No faction claims it - too dangerous
    connections: ["Dust Roads", "The Pallid Marsh"]

factions:
  - name: "The Reclaimers"
    type: political
    goals:
      - Reunite the kingdom under "rightful" rule
      - Recover all crown fragments
    resources:
      - Largest army (poorly equipped)
      - Claim to royal bloodline
    key_figures:
      - "Marshal Vren - pragmatic military leader"
      - "The Pretender - disputed heir, rarely seen"
    relationships:
      enemies: ["The Free Cities"]
    tension_points:
      - Internal debate over Pretender's legitimacy

early_game:
  phase_summary: "Heroes encounter faction conflict, acquire first crown fragment"
  plot_hooks:
    - name: "The Dead Courier"
      type: negative
      trigger: "Party finds dying messenger on road"
      key_elements:
        - Messenger carries sealed letter revealing fragment location
        - Assassin tracks party after they take letter
        - Letter is encoded - need to find translator
      potential_outcomes:
        - Decode letter, race to fragment location
        - Sell information to faction, become targets
        - Destroy letter, assassin still hunting

gm_notes:
  session_zero_topics:
    - "This campaign involves moral compromise - no clear heroes"
    - "Death is possible - bring backup character concepts"
  pacing_recommendations:
    - "Introduce all three factions by session 3"
    - "First crown fragment should be acquired by session 4-5"
```

---

## Output Quality Checklist

Before delivering output, verify:

- [ ] All elements use bullet points, not paragraphs
- [ ] Each plot point has: name, type, trigger, key_elements, outcomes
- [ ] Key elements limited to 3-5 bullets per item
- [ ] Potential outcomes offer 2-3 distinct directions
- [ ] Story buckets progress logically (setup → escalation → climax)
- [ ] World elements connect to story where relevant
- [ ] GM notes included with actionable recommendations
- [ ] Tone maintained consistently throughout
