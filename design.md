# Agent

## Traits

Each agent can have common + rare traits. Common traits are shared by all agents, rare traits are randomly given to each agent(each run will have different rare traits).

### Common

- Age - range(18-55)
- Gender - Male/Female
- Weight - 50-100kgs
- Overall Mood - Depressed, Anxious, Neutral, Content, Happy
- Education - Each run 30% will have highschool + university, 60% only highschool, 10% no education(an agent without education can still be highly succesful but rate is very low)
- Health - scale of 1-10
- Diseases - list of diseases 60% of the time no diseases to an agent, otherwise a list of diseases randomly given(can be fatal as well but fatal keep it <=2)
  - Non-fatal: Diabetes, Hypertension, Asthma, Chronic back pain, Migraine, Anxiety disorder, Depression, Arthritis
  - Fatal (max 1 per agent, kept rare): Cancer, Severe heart disease, Stroke
- Marritial Status - Single, Married, Divorced
- Family - True or False
- Has job - true or false
- salary class - low, medium, high
- Savings - None, Some, Allot
- Risk tolerance - scale 1-10
- Social Support - None, Little, Large
- Spending per month - (this can be salary - savings i need to come up with a formula for this meaning if an agent has allot of savings he wont save allot from that months salary, he would spend, so when a shock hits he wont reduce consumption)

### Rare

- High IQ - true or false
- Born in High income family - true or false
- Chronic optimist / pessimist - True/False (affects how mood recovers after a shock independent of actual outcome)
- Physical disability - True/False
- Past trauma history - True/False(could make an agent more sensitive to shocks even with otherwise strong stats)
- Strong Mindset - Scale 1-10. if 1 the agent gets affected by the shock more, 10 - the agent is still learning but doesnt go into depression or anything he finds a way out

## Action Space

A small, fixed set of choices every agent picks from when a shock hits. Same options for everyone, but which one gets picked (and how well it pays off) differs per agent:

- Ignore - doesnt really care about the shock
- Reduce consumption - lowers budget
- Seek support - Ask family for support, if no family then social support
- Professional Help - Seek therapy, will add up spending but help better up mood
- Self adapt - see whats happening, adapt to whatever is necessary to improve mood

## Reward

reward = Δmood_score + Δhealth - action_cost

- Δmood_score - numeric mapping of mood scale (Depressed=-2, Anxious=-1, Neutral=0, Content=1, Happy=2), change from before → after the action
- Δhealth - change in the 1–10 health scale
- action_cost - a fixed cost per action (Ignore=0, Reduce consumption=small mood cost, Seek support=small cost unless Family/Social Support is strong, Professional help=spending cost but strong mood/health recovery, Self adapt=small cost, moderate recovery)

## Threshold

Composite score built from traits an agent already has
threshold = (health/10) + (savings_weight) + (risk_tolerance/10) + (social_support_weight) + (education_weight)
− (disease_penalty)
− (trauma_penalty)

## Shock

A shared event applied identically to the whole population

- Type - [Gas price increase, Food supply decreases, Food price increases, Global Pandamic(since u asked to startt with one ill start with this), Job loss, Divorce(if married), War]
- Intensity - scale of 1-10 how bad the shock is, normally its below 5 but sometimes it can be above
- Duration - Scale 1-10 (1 = 1 week, 10 = 10 week)
