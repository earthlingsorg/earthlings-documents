# Working Agenda

**One possible model of the future. Not a blueprint to be rolled out - a specimen of how the workings of our common home can be taken apart and tested in the first place.**

> Working agenda · for a narrow circle
>
> A specialist examination · with every joint and crack left visible

> What this document is
>
> This is a *working agenda*: an examination of the tasks the people is working on and is opening up for research, design, and testing. The document is dense and highly specialist - of a kind with the Legal Basis; it is reading for a thoughtful specialist. Its value lies in showing the kind of work itself, assembled all the way through.
>
> It deliberately leaves both the strong places and the weak ones in view. The weak ones are not a defect but the content: a map of what still needs thinking about. Any part of it can be contested, rewritten, forked.
>
> **Where it comes from and what it calls for.** This examination arose in the work on Earthlings - a cross-border voluntary community of people. But the model itself stands alone: it holds as pure reasoning, and Earthlings is neither its source nor its owner but an *environment* where models of this kind can be assembled in the small, set against one another, and tested for strength. We consider these questions important for everyone - a common home concerns each of us; and so we are ready to discuss, research, design, and test them from the first days and in the open, together with anyone who wishes to take part.

# Part 0. How to read this document

At the base lies a radical but productive metaphor: the present world order - with its whole social, political, economic, and legal fabric - is a working but old operating system. Call it "Windows 11". It is not meaningless: it boots, and billions of processes live on it. But its bugs are already known - the ones that have shown themselves over decades and cost human lives.

The question of this document: given a full staff of developers and a blank sheet, what would the next version look like - "Windows 12"? There is no ideal one - what is meant is the most correct and complete version achievable in the present situation.

The OS metaphor is taken seriously. An operating system has a real anatomy: the kernel and rings of privilege, the permission model, process isolation, the scheduler, the update mechanism, error handling, authentication. Each axis maps onto the workings of a society with surprising precision - and where the mapping breaks, it breaks instructively. At the end (Part IX) the chief flaw of the metaphor itself is examined: an OS has an owner, and humanity must not have one. The language of operating systems was chosen precisely for this precision - it is the closest and clearest way to explain a design of this kind. At the same time "Windows 12" is an analytical lens, not a slogan: in the model itself the state does not disappear but becomes a thin layer (Part III), so what is meant is the rebuilding of the whole stack as a subject of examination, complementing states rather than abolishing them.

Specialist technical terms (kernel, user space, capability, zero-knowledge, sandbox, nullifier, and the like) are deliberately left unexplained: an explanation of each would swell the length, and their meaning is easy to look up in open sources where needed. What matters here is not precision of an IT definition but the role the term plays in the design.

The document is arranged as follows: first a diagnosis of the old system (I), then an examination of what must survive from it (II), then the architecture of the new one (III) and the place of the human being in it (IV). Then three of the most heavily loaded modules opened up separately (V-VII), their mutual conflicts (VIII), the architect's trap (IX), stress tests to breaking point (X), a comparison with real living attempts (XI), and finally the open horizon of work (XII).

# Part I. Diagnosis: the bugs of "Windows 11"

I.1

## The state is not a thing but a bundle of functions

The chief error in any conversation about the future is to discuss the state as a monolith that either exists or does not. The state is not an entity but a *bundle of functions* that ended up in one pair of hands for reasons of war, taxation, and industry:

1. **A monopoly on legitimate violence** - who has the right to coerce.
2. **Jurisdiction over territory** - power over a piece of physical space.
3. **Production of common goods** - roads, networks, defence, courts, infrastructure.
4. **Belonging and identity** - who is "one of us", to whom a person is assigned.
5. **Redistribution** - care for the weak, insurance against misfortune.
6. **Law and dispute resolution** - rules and arbitration.
7. **External representation** - a voice outward, on the international stage.

There is no law of nature by which these seven functions must lie in one box. They stuck together historically - and today they are coming unstuck before our eyes: identity leaks into networks, money into protocols, disputes into private arbitration, common goods into transnational structures. Understanding the state as a *detachable* bundle rather than an atom is the foundation of everything that follows.

I.2

## A list of the bugs

Monolithic kernel

All seven functions in privileged mode at once and in one pair of hands. A single fault brings everything down. Identity is nailed to the "hardware" - to the geography of birth.

Capture of root access

Power rewrites the rules that are supposed to limit it. Regulatory and constitutional capture is a process editing its own kernel in its own favour.

Rights by the lottery of birth

Permissions are set not by a principle but by the machine a person happened to boot on. Morally this is indistinguishable from an estate system - the estate is called "citizenship".

A terrible updater

Rules can be changed systemically mostly by war, revolution, or glacial lawmaking. There is no safe reversible patch.

No process isolation

A fault is not sandboxed. The crisis of 2008, a pandemic, a local conflict - the failure cascades through the whole system.

Leaks into shared memory

Processes write into shared memory - the atmosphere, the ocean, the climate - unaccounted for. Costs are dumped into the common pool, and whoever pays, it is not the author.

A scheduler set to zero-sum

The default is competition for displacement rather than cooperation. One party's gain often literally means another's loss.

Expensive trust

An enormous share of effort goes not into creating but into verifying: intermediaries, guarantors, bureaucracy, courts, contract enforcement.

> No single bug is fatal on its own. Together they form a system that works but systematically produces unfreedom, insecurity, distrust, and war as *by-products of its own architecture* rather than as chance faults.

# Part II. What must survive from the old system

Before designing something new, one has to say honestly what cannot be thrown away. The romantic version - states simply dissolve into voluntary communities - breaks against several hard facts.

### Physical space is rival

A river, a power grid, a port, a hectare of land cannot be "forked", and one cannot be in two jurisdictions at once. As long as people have bodies and occupy space, someone manages that space and resolves conflicts over it. This is the irreducible core of territorial power: matter breeds competition for exclusive use.

### Physical safety - the extreme case where exit is impossible

A pandemic, an invasion, a catastrophe. Here a structure is needed that *cannot be left with a click*, because it has to hold in a common cost those who would prefer to flee. Freedom of exit is splendid against tyranny and lethal against a pandemic: a virus does not care which voluntary community a person belongs to.

### Care for those who cannot contribute

This is the strongest argument for something state-like, and the one least often said aloud. Voluntary communities by their nature look after the useful well and the useless badly: the sick, the old, the broken, the "unprofitable". History has compelled solidarity precisely through a structure with no exit - one from which the healthy and the wealthy cannot emigrate away from their obligations to the weak. Remove the compulsion to solidarity and you get people sorted by usefulness. That is not freedom. That is Darwinism with a good interface.

> The axial principle
>
> Coercion cannot be abolished - it can only be distributed and limited. Any system able to *guarantee* peace holds the force to impose that peace - and that force is therefore dangerous. There is no free lunch: all that can be designed is *where* coercion is legitimate, *how far* it is limited, and *who* cannot abuse it.
>
> What disappears is therefore not "the state" but its **monopoly and its fusion**. The functions move apart into layers, and the no-exit coercive kernel shrinks to the necessary minimum - but not to zero.

# Part III. The architecture of "Windows 12"

III.1

## A microkernel instead of a monolith

The first decision of any OS: what runs in ring 0 (privileged) and what runs in user space, where a process can crash without bringing the system down. A monolith is bad architecture. Here the architecture is a **microkernel**. In the kernel is only what is physically inseparable and rival, what one cannot exit:

- protection of physical safety and physical space;
- the planetary life-support systems - climate, ocean, atmosphere, orbit, spectrum, water;
- governance of the supertechnologies where the cost of an error is the species entire (artificial intelligence, bioengineering);
- and above all, maintenance of the permission model itself: the guarantee that no one becomes root.

Everything else - economy, culture, communities, ways of life, faiths, aesthetics - goes into user space. There it competes, errs, goes bankrupt, dies, and is born again, without taking the system with it. The kernel is thin; above it a seething space of free processes.

III.2

## The human being is a user, not a process

The heart of the whole model, and the point where most historical systems break.

In an operating system the sovereign is the **user**. Processes exist to serve the user; when a process obstructs the user or hangs, it is terminated - a routine operation, not a tragedy. The deepest bug in almost every design of society is that it *inverts* this relation: the human being becomes a process serving the System - the economy, the nation, the state, the party, the "great cause". People are scheduled around the system's tasks rather than the other way round.

> **First principle:** the human being is the user; institutions are processes. Not the reverse. An institution that has stopped serving people is subject to termination, like a hung process. A people, a state, a corporation, a party, a movement - these are daemons in the background: useful, they run; harmful, they are terminated. No process is entitled to declare itself the purpose for which the user exists.

III.3

## The permission model: capability-based security

The best idea in modern computer security is **rights as capabilities under the principle of least privilege**. The whole of politics is built on it.

- No actor receives more powers than a particular task requires.
- Every power is revocable, time-limited, and auditable. There are no perpetual, unconditional, heritable grants of power.
- Human rights are not an abstract declaration but concrete inalienable tokens that cannot be taken away by a jurisdiction, traded off, or made conditional on usefulness.

> **The key move:** the principle of least privilege is applied first of all to power, not to the citizen. Today it is the reverse - the citizen under the magnifying glass, power in the shadows. Here the order is inverted: maximum transparency and minimum privilege for whoever rules; maximum privacy and a protected base of rights for whoever is ruled. The transparency of the ruler is a right of the ruled, not a favour from the ruler.

III.4

## Process isolation and the right of exit

Federation, polycentricity, sandboxes. Communities, economies, and ways of life are isolated processes. One falls, the others live on. Then **the right of exit = the right to terminate a process or to leave it**. This is the most powerful limiter of tyranny: power one can walk out from under is forced to be tolerable, because otherwise it is left without people. But this has a price (Part VIII): exit everywhere leads to sorting by likeness, to the disappearance of solidarity across difference, and to the question "who is left with those everyone exits from". The right of exit is absolute in user space and impossible in the kernel - otherwise the whole of Part II collapses.

III.5

## Three layers and subsidiarity

Assembled together, the architecture yields not "no state" but **layering**. The organizing principle is **subsidiarity**: a decision is taken at the lowest level able to hold it, and rises higher only when it must.

[[BLOCK-diagram-1]]

Such a division reconciles freedom with safety better than anything else devised: it neither centralizes out of habit nor decentralizes out of dogma, but puts each task where it is actually solved.

# Part IV. The role of the human being: rights, function, duties

The model answers the direct question - what does a person become within it - with three bundles.

### Rights (capability tokens, inalienable, guaranteed by the kernel)

Exit

To leave any process except the kernel layer. The right to leave is the foundation of freedom: it is what makes any consent real rather than forced.

Voice

To take part in the rules one lives under. Voice is needed above all where exit does not work - one cannot exit the kernel.

Audit

To read the code that executes a person. No closed source in the power over them. Whatever rules must be transparent to the ruled.

Non-domination

Freedom as the absence of arbitrary power over a person, not merely the absence of momentary obstacles. One is free not when unobstructed, but when there is no one above who *can* dispose of one at their discretion.

Floor

A guaranteed minimum of resource below which the system does not let a person fall. Not charity, but the condition of everything else being honest (Module 2).

### Function

The human being is at once a **user** (sovereign over their own domain) and, collectively, the **sole source of the kernel's authority**. The kernel is legitimate exactly in so far as it is exercised on behalf of users. There is no "people above people", no "state above citizens" as a separate higher entity - there are people whose combined will is the only root. More precisely: root as an occupied position does not exist at all (Part IX); there is only a distributed source of authority that no one appropriates.

### Duties (the price of the no-exit layer - without it the whole construction is utopian)

- **Do not corrupt shared memory.** Do not dump your costs into the biosphere and into someone else's life. Internalizing externalities is neither a tax nor a moral duty but a prohibition on memory corruption: you cannot write destruction into memory that everyone shares.
- **Support the upkeep of the common.** Contribute to the kernel layer (safety, the commons, protection of the weak), from which one cannot exit - precisely because one cannot emigrate from its obligations. The only legitimate compulsion to contribute.
- **Service the system.** Participation as maintenance. An OS no one maintains degrades. Citizenship is both a login and a duty shift on the system: the minimal share of attention and labour without which the common rusts.

# Part V · Module 1. Sybil identity: a human login without a new Big Brother

### The real dilemma

This is a trilemma: three properties of which at most two are achievable at once.

Uniqueness

One living human being = one account. Without it, "one person, one vote" degenerates into "whoever has more bots".

Privacy

A person cannot be tracked, their actions correlated, a dossier assembled.

Decentralization

There is no single issuer who thereby becomes the very root the model undertook not to create.

Any real system sacrifices one for the sake of two. This looks like a structural property of the problem rather than an oversight.

### What has been tried and how it breaks

- **A centralized biometric registry.** Uniqueness - excellent. But it is exactly that root: a single point of exclusion (switch off the entry and a person becomes a civil corpse), a single point of surveillance, inevitable function creep.
- **Web-of-trust (vouching).** Decentralized, private. But Sybil resistance is weak at scale, and it reproduces the inequality of the social graph: whoever has connections gets verified; the isolated remains nobody.
- **Proof-of-personhood by biometrics.** Uniqueness at scale is solved. But: a biometric honeypot of planetary size; trust in hardware; vulnerability to coercion; irreversibility (an iris cannot be reissued); and behind it all, a company. Global biometric deduplication is itself a ready-made surveillance infrastructure.
- **A state document wrapped in selective disclosure.** It improves privacy, but leaves the state as the root of trust and inherits the lottery of citizenship.

### The least-bad option

The key move is to unstick what the word "identity" has glued into one lump: **authentication** (the same subject), **uniqueness** (the subject is one), and **attributes** (the person is 18 / is a member of this / holds right X). The crime of passport systems is driving all three through a single identifier.

- **Whoever verifies uniqueness must not become an observer of activity.** Between "who is unique" and "what they did" stands a cryptographic wall: zero-knowledge and nullifiers. The issuer hands over a proof and forgets; the proof stays with the person.
- **Plurality of issuers instead of a monopoly.** Many independent ones, k-of-n sufficing. None is root, none is a single point of exclusion.
- **Revocability instead of raw biometrics as the key.** The primary key is a reissuable credential. Biometrics fail precisely at reissue, and therefore cannot be the root.
- **Nullifiers scoped by context.** Prove uniqueness "in this election" without linking it to uniqueness "on that forum".

> What is not solved
>
> **Coercion.** Cryptography is powerless against physical force: a person will be made to log in at gunpoint. There are partial measures; fundamentally it is unsolved.
>
> **The excluded.** There are always people the system does not verify: the undocumented, the stateless, borderline cases. And here lies the deepest ethical risk: *the more important the login, the more catastrophic exclusion from it*. Personhood that gates rights breeds a class of digital non-persons.
>
> **Hence the principle:** uniqueness must be *additive, not gating* - it should unlock the extra, but basic dignity must never require a login. The moment "being human" requires successful authentication, a hell with flawless UX has been built.

# Part VI · Module 2. The scheduler-economy: what is in the floor and who pays for the kernel

### The real dilemma

Two linked questions: how to allocate scarcity (land, energy, matter, attention) and who funds the no-exit kernel. Above both stands the conflict of two failures:

market failure

A pure market fails on shared memory (externalities), on those with no purchasing power, and on concentration (success buys up the conditions of the next round).

plan failure

A pure plan fails on the knowledge problem (the centre does not know what a market aggregates through prices) and on the fact that a central allocator is a new all-powerful root.

### The least-bad option

> **The kernel sets invariants, not allocations.** The kernel is not a planner but a *constraint solver*: it sets the bounds, and within them a decentralized market distributes. This preserves both the Hayekian information of prices and the protection of the common.

1. **A protected floor.** A guaranteed minimum: food, energy, access to computation and information, basic health. The justification is not pity but freedom: one can bargain freely in a market only if there is somewhere to walk away to from a bad deal. The floor gives the power to stand up and leave; it makes the market above it honest.
2. **The common is metered and paid for.** The rival commons (atmosphere, orbit, spectrum, water, attention) is neither free nor privatized - access to it is paid for and metered. The revenue from depleting the common funds the floor and the kernel. This is rent on the common (in the spirit of George), not a tax on production: you pay not for what you created but for what you took from everyone.
3. **A concentration ceiling is a security feature, not envy.** Extreme concentration of resource = concentration of power = a potential root, and rootlessness is among the model's axioms. Limiting accumulation is anti-capture. The justification is stronger than the moral one: not "wealth is unjust" but "super-wealth is an unauthorized seizure of administrator rights".

> Separately
>
> **Attention as a scheduled resource.** In an information system the scarce good is human attention, and the old OS is infected with malware: engagement-maximizing processes hijack the scheduler. The hijacking of attention is classified as malicious software; the user's attention is protected as a floor resource. Attention belongs to the user, not to background daemons that have learned to pull at dopamine.

> What is not solved
>
> **Who pays for the no-exit kernel is the architecture's Achilles heel.** The kernel is a pure public good, and public goods invite free riding; historically that is why a coercive collector - the state - was needed. The whole voluntary, exit-based construction breaks here.
>
> **The honest answer:** the kernel is the one place where compulsion to contribute is legitimate, precisely because one cannot exit it. One cannot not breathe the atmosphere - and so one cannot not pay for its protection. But this shifts the problem rather than removing it.
>
> **The recursion of the treasury.** Whoever collects and spends the kernel's purse is themselves a candidate for root. The treasury must live under audit and least privilege: transparently, by formula, with minimal discretion. That narrows capture without eliminating it: someone still writes the rules (Module 3).
>
> **Goodhart.** As soon as the floor and the rent are set as numbers, the numbers will be gamed. A measure ceases to be a measure once it becomes a target.

# Part VII · Module 3. The update mechanism: without revolutions and without a dictatorship of improvers

### The real dilemma

too rigid

The system ossifies, and accumulated pressure tears it open in revolution. A revolution is an admission that there was no proper updater.

too plastic

Whoever controls updating controls everything. A door for "improvers" who pave over living complexity to fit their scheme (high modernism killed by the million).

### The least-bad option

- **Policy as experiment.** Staged rollout instead of "everything at once"; A/B testing on a small consenting circuit; measurement against metrics announced in advance; expansion only if it worked.
- **A bias towards reversibility.** Preference for what can be rolled back. For the irreversible, a radically higher threshold. Sunset clauses: rules expire and must be reconfirmed. The default is repeal, not accumulation; a dead institution quietly expires instead of dragging on by inertia.
- **The fork as a fuse.** Lose an update and you do not go to war; you separate on open rules. Pluralism applied to time.
- **Separating the power to change rules from the power to gain by them.** Whoever writes an amendment must not feed off it. A change is made under a partial veil of ignorance about one's own future position.
- **Who guards the updater.** The update mechanism is itself code, and whoever changes it is the real root. The meta-rule is the hardest of all to change: only a durable supermajority sustained over time. Time-locks: a change to the kernel requires support across several periods. A majority on a Tuesday does not touch the kernel.

> What is not solved
>
> **Goodhart and the tyranny of the measurable.** "Evidence-based policy" smuggles in the measurable and crushes the unmeasurable - dignity, meaning, trust, grief. The whole of politics is already hidden in the choice of metric. Plus the ethics: A/B testing on the living is experimentation on people, and consent here is a moral question.
>
> **What cannot be forked.** Forking works in user space. The atmosphere cannot be forked - *the kernel is in principle unforkable*, which is why changing it requires the highest threshold and has no emergency exit. The layer most in need of change is the most dangerous to change.
>
> **Forking fragments solidarity.** The right to leave and build your own is a good against tyranny and a poison for the common: Cells gather with the like-minded, the echo-chamber effect grows, and the question remains "who is with those everyone forked away from".

# Part VIII. How the modules fight one another

This matters more than any module on its own. The three modules are not independent problems but a bank of dials where every setting of one spoils another. An honest model is bound to show these conflicts rather than hide them.

[[BLOCK-diagram-2]]

> A final honest thought
>
> There is no ideal setting. Freedom, safety, welfare, trust, and peace cannot all be turned up to maximum at once - they physically pull the dials in different directions. The aim is therefore not to find the "right" values (there are none), but to **keep the dials in plain view, let no one seize the console, and allow them to be turned back when we get it wrong**.

# Part IX. The architect's trap

Here the OS metaphor cracks - and that crack is the most important thing in the document. An operating system has an **owner** - the one who holds root, decides what is good for the user, and rolls out updates without asking. Humanity must not have such an owner.

The most dangerous thing about the task "design a world order" is the temptation to assemble a beautiful, unified, rationally arranged system with one wise architect. That is exactly what killed by the million in history. Society is not code; values have no compiler; there is no unit test for justice; and anyone who claims to know how things ought to be and demands the right to rewrite everyone is more dangerous than the bug they undertake to fix.

> The only honest design principle
>
> The best OS for humanity is one that **resists its own architect**. It is designed so that:

- it has **no root user** at all - no centre able to rewrite the kernel to suit itself; the source of authority is distributed and appropriated by no one;
- **deliberate inefficiency and friction** are built into it - separation of powers, duplication, time-locks - so that it cannot be captured quickly; an efficient system falls efficiently into the wrong hands too, so a measure of inefficiency here is not a bug but an immune system;
- it is **pluralistic by design** - many systems rather than one; the right to fork matters more than the beauty of a unified architecture.

> The architect's task is to write a system that *does not need an architect* and lets no one become one. Not to configure everyone to one's own understanding, but to remove the very position of the one who configures everyone. The greatest feature of "Windows 12" is the absence of a button granting anyone the power to rewrite everybody else.

This applies to the document itself. It is written in a single voice - and precisely for that reason it must not be taken as a finished system. Its purpose is to be opened up, contested, and forked, not implemented.

# Part X. Stress tests: where the model breaks first

A model not run against a scenario to breaking point is not a model but a stage set. Running "Windows 12" through three hard scenarios shows honestly where it falls.

### Scenario 1. Pandemic

A fast lethal pathogen. The kernel needs instant compulsion to a common measure, while the whole architecture is built around the right of exit and minimal coercion.

where it holds

A pandemic is the canonical kernel case (planetary life support, no exit), so the legitimacy of compulsion here exists by construction.

where it breaks

Speed. The time-locks and reversibility that save in peacetime are murderously slow in an exponential outbreak. The temptation of an "emergency regime" arises - and historically that is the chief machine for producing a permanent root.

### Scenario 2. War over a physical resource

Two territorial layers claim the same river / shelf / corridor. The resource is rival, and forking is impossible.

where it holds

The planetary layer is designed for exactly this - an arbiter of no-exit conflicts; rent on the common provides a mechanism of "how much and at what price to each" rather than "whose".

where it breaks

And if the strong layer refuses to recognize the arbitration? Force sufficient to compel the strongest is sufficient to become a tyrant. The eternal paradox of world order: the arbiter is either weaker than the strongest (useless) or stronger (dangerous in itself).

### Scenario 3. Capture by an AI

A superpowerful AI is in the kernel. Whoever controls that process controls the most privileged code on the planet.

where it holds

Least privilege, auditability, and the absence of root are aimed directly against this; an AI-in-the-kernel is by construction obliged to be maximally transparent and constrained.

where it breaks

Audit presupposes that the auditor can understand the code. A superhuman AI may be opaque in principle - not closed, but incomprehensible. "The right to read the code that executes a person" is devalued if the code cannot be understood. Possibly the deepest breach of all.

> Conclusion
>
> The model is most robust in slow, distributed conflicts and weakest where *speed* is needed, or where the adversary is *stronger than the arbiter* or *incomprehensible*. This is not a verdict but a map of the forward defence: this is where the work should go.

# Part XI. A comparison with real living attempts

Nothing here is wholly new. Almost every element has already been tried by someone in real life - and almost every attempt broke on something. An honest model is bound to know its predecessors and not to pass off the old as unprecedented. The novelty, if there is any, is only in the *configuration*, not in the elements. Every living attempt is a stress test of one module already carried out.

| Living attempt | What it confirms | Where it breaks |
|---|---|---|
| Federalism, subsidiarity | Layering and "decide at the lowest capable level" work. | The upper layer either devours the lower ones or is paralysed by a right of veto. |
| Cooperatives, mutualism | An economy in which a person is a user and the vote is not bought. | They scale badly, struggle with capital, and degenerate into a managerial oligarchy. |
| Commons after Ostrom | Communities can hold the common without privatization and without a state - given the conditions. | It worked at scales one can take in; the planetary one is an untested extrapolation. |
| Georgism (rent on the common) | An exact prototype of "the common is paid for, labour is not". | It loses politically to the holders of rent; the problem is capture of the implementing mechanism. |
| DAOs, Web3 governance | Live capability permissions, the fork as a fuse, an algorithmic treasury. | Plutocracy (the vote is bought with a token), Sybil attacks, the gap between "code is law" and living justice. |
| Network states | An attempt to untie belonging from territory and to make exit the foundation. | They gather the wealthy with others like them; they are weak on care for the unprofitable. |
| Non-territorial peoples | A people without territory is not a fantasy: under declarative theory, existence is a fact of self-founding rather than a gift of recognition. | What is open is not the existence of the subject but external recognition - it accumulates separately and slowly; for groups inside states it runs through those states. |

> They say it plainly: a single element can be built but breaks at scale, on capture, or on care for the weak. The model's open question is whether the *configuration* will hold where the *parts* fell. There is no answer in advance; it is obtained only by trying.

# Part XII. The open horizon: what we are opening up for work

The value of a model lies not in its answers but in the quality of the questions it makes concrete and testable. The weak places of the previous parts are the agenda. Specific tracks open for joint research, design, and testing:

1. **Sybil without Big Brother.** Certify a person's uniqueness without building either a central surveillance registry or an excluding gate. For now, a trilemma without a solution.
2. **Additive rather than gating personhood.** So that the absence of a login never takes away basic dignity. Protection against the chief risk - a class of digital non-persons.
3. **Funding the no-exit kernel without a new tyrant-collector.** Rent on the common is a hypothesis; who collects it and how, without the treasury becoming root, is open.
4. **Kernel speed versus protection against capture.** Give the kernel swiftness in a catastrophe without creating a machine for emergency regimes.
5. **An arbiter stronger than the strongest but not a tyrant.** Perhaps the answer lies not in the arbiter's force but in a construction where breaking the rules is unprofitable for everyone at once - that has to be built and tested.
6. **Auditability of the incomprehensible.** Control over a superpowerful AI in the kernel when its code cannot be grasped by a human mind. Possibly the most important of all.
7. **A floor and exit at the same time.** Combine the right to leave with the durability of the common, so that freedom to diverge does not kill solidarity.
8. **Metrics without Goodhart.** Measure the success of policies without crushing the unmeasurable and without setting off a race to game thresholds.

> On the work and its support
>
> Every track is concrete work for the common good that can be carried out and supported as research and prototyping - in the small, in the open, with verifiable steps. Support for such work is accepted only within a strict discipline: the vote is not bought, contribution gives no power over people, and nothing is promised in advance. Supporting the delivery of a track is possible; buying the people's direction is not.

Closing frame

## The model is an example. The horizon is real.

This document is one voice and one of an infinite number of possible models. It is deliberately unfinished: with strong places that can be developed and weak ones that need opening up. Its task is done if it has shown that a world order can be taken apart as engineering, that the state is a detachable bundle of functions rather than a fate, and that an honest model differs from a utopia in showing its own cracks first.

It is here that Earthlings returns - not as the author of this model and not as its bearer, but as an *environment*: a place where models of this kind become the object of living work - assembled in the small, tested on those who consent, measured, rolled back, forked, and passed on. Not "here is the right answer", but "here is a space in which answers can be sought without staking the whole world".

Come and take apart, contest, and break whatever holds badly. The direction is towards where the dials are in plain view, the console is handed to no one, and a mistake can be rolled back.

Working agenda of the Earthlings people · a specialist examination. Not a programme for the future and not a finished project - a list of open problems and an invitation to work together.
