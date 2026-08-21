# The Earthlings Digital Platform

**Infrastructure of identity, participation, and projects for the Earthlings people**

> This document describes the technical implementation of the rules laid down by the Earthlings Charter. Where they diverge, the Charter applies; where the Charter diverges from the Declaration, the Declaration applies. The platform does not establish rules: it executes them.

---

# SECTION 01. Purpose of the platform

The Earthlings digital platform is the core in which four levels of the people come together:

- **identity** - confirmed and at the same time private;
- **participation** - signing the Declaration, voting, discussions, joint action;
- **projects and Cells** - initiating, forming, coordinating, carrying out, and recording results;
- **the economy of participation** - the unit of account, the common fund, reward for contribution.

The platform is not a social network or one more blockchain system. It is the instrument through which the Earthlings people can exist: with infrastructure that is transparent and at the same time protective of the person.

The main task is to make participation practical, safe, and honest: from the first signing of the Declaration to the delivery of complex international projects.

> **Limits of the platform.** The platform takes no decisions and cannot take them. Binding decisions are taken only by the DAO Assembly. The platform is the executive level: it provides the interface, records the outcome, and puts it into effect. No component of it, no automatic mechanism, and no person operating it is entitled to alter, revoke, or block a decision of the Assembly.

---

# SECTION 02. Architectural levels

The architecture is built on a multi-layer principle. Each layer solves its own task and intrudes on the others as little as possible.

**1. Presentation level.** Web interfaces, mobile applications, an API for external integrations. Here a person sees the Declaration, the map of projects, the panel of Cells, votes, and their personal account. The priority is accessibility and clarity.

**2. Application level.** Modules of functionality: profile management, submission of initiatives, the work of Cells, voting, delegation, fund management, supporting AI tools. Business logic without the storage of low-level data.

**3. Data level.** Profile stores, project metadata, Cell statuses, DAO configurations, voting results, event logs. The principles of minimization, separation, and "collect nothing superfluous".

**4. Identity and trust level.** The people's own identity-verification system, the issuance and accounting of non-transferable identity tokens, the recording of the Declaration's signing. This layer is isolated and protected to the maximum degree.

**5. Level of the economy of participation.** The infrastructure of the unit of account, the common fund, the distribution of rewards, integration with projects and Cells.

**6. DAO integration level.** The interfaces and protocols through which decisions of the Assembly are reflected in the work of the platform: settings, access rights, economic parameters, development priorities.

The layers evolve separately: the application level can be updated without touching identity, and economic mechanisms can be changed without affecting the DAO core.

### Who operates the platform

Technical operation is provided by the **Core Nodes** - elected technical coordinators (Charter, Article 2). They maintain the infrastructure and are responsible for cybersecurity and technical support of voting, but they take no decisions on behalf of the people, do not manage finances, have no special weight in votes, and cannot block DAO decisions. They are recalled by a simple majority at any time.

The **Emergency Multisig** (Charter, Article 3) is entitled to suspend particular smart contracts when a critical vulnerability or a cyberattack is discovered. Every such action requires a public report within 48 hours and confirmation by the Assembly within 7 days, failing which it is reversed.

No other persons or structures with technical powers over the platform exist.

### On AI

At the initial stage the platform uses existing artificial-intelligence models to analyse initiatives, support projects, and automate routine work. In the longer term, developing an in-house model adapted to the people's tasks is under consideration.

The limits on the use of AI are set by Article 10 of the Declaration: no digital architecture can justify hidden manipulation or the suppression of human autonomy. Hence three strict rules that apply whichever model is used:

- **AI decides nothing.** Any output it produces is advisory and is not a ground for refusal.
- **Reasons are disclosed.** A person whose initiative AI has flagged receives a statement of the reasons in intelligible form, not a refusal without explanation.
- **Human review is guaranteed.** The initiator is entitled to demand review by a human being, and such review is carried out within a set period.

---

# SECTION 03. Identity: identity verification and the non-transferable passport

Identity is built around a non-transferable digital passport (SBT) linked to a confirmed person. A strict separation is observed:

- biometrics and documents are processed by the people's own identity-verification system in real time;
- the platform receives only the fact that verification succeeded, not raw biometric data or scans;
- after verification, a passport confirming the participant's status is issued to their address;
- one person, one passport; the passport is not transferred, not sold, and not taken away.

### Separating the axes: identity, vote, economy

The architecture requires that identity, the vote, and the economic trace not merge into a single point of power:

- **identity** is set by the passport and by identity verification;
- **the vote** follows from earthling status: one person, one vote;
- **economic activity** is reflected in the unit of account and gives no additional votes, whatever its volume.

### Burning a passport

As a general rule a passport is burned only by the holder themselves, with their own key, from their own wallet. The platform stores no participant keys and is technically unable either to perform the burning for them or to prevent it.

The Charter (Article 21) establishes two and only two exceptions, which the platform is obliged to support and is not entitled to extend:

1. **annulment of an invalid issuance** - where it is established that the passport was issued in breach of the conditions of issuance; only by decision of the Assembly with a sanction majority, by secret ballot, with a right of appeal;
2. **technical reissue** - at the holder's own request on loss of access to a wallet or on migration of the contract; belonging is not interrupted.

No other grounds for burning by someone other than the holder are implemented in the platform, and against the holder's will a passport is burned only upon annulment of an invalid issuance. The death of the holder is not among the grounds: the platform does not and cannot hold information about deaths, and the ending of participation is handled by the inactivity mechanism (Charter, Article 20).

---

# SECTION 04. Personal account and profile

The personal account is a person's principal point of contact with the ecosystem.

### Main elements of the profile

- the earthling pseudonym - a public name in the ecosystem;
- country of residence or of belonging - at the participant's choice;
- status of the Declaration's signing;
- a mark that a passport is held, without disclosing personal data;
- areas of interest and competence - optional.

### Marks of participation

- participation in Cells;
- participation in projects: role, contribution, completion status;
- participation in votes - to the extent set by the rules on openness and secrecy (section 06);
- recognition marks received.

> **Recognition marks affect nothing** and remain purely informational ([Charter, Article 8](https://earth-lings.org/documents/en/en05-charter.html)). The platform is not entitled to use reputational indicators as a condition of access to any function.

### What the account does not contain

Passport data, biometrics, and sensitive legal attributes are neither displayed nor stored. They remain in the identity-verification system and are not retained after verification. The platform works with a pseudonym, a mark that a passport is held, and aggregated indicators of participation.

Photographs and scans are not retained; biometrics are processed only at the moment of verification. What exactly is retained to prevent repeat registration is in the [Biometric Verification Policy](https://earth-lings.org/documents/en/en16-biometric-verification.html).

---

# SECTION 05. Cells and the project flow

The platform supports the full cycle: from the appearance of an idea to the completion of a project.

**1. Project application.** Any earthling may propose a project through their personal account. The application includes a description of the subject, the aim, the expected effect, the competences required, and the horizon of delivery. The initial analysis is performed by AI - for conformity with the Declaration, with ethics, and with priorities - and this analysis is advisory: it constitutes no refusal, the reasons are disclosed, and review by a human being is guaranteed (section 02).

**2. Notification of relevant participants.** After the initial analysis the application is directed to those whose declared competences match it - lawyers, engineers, programmers, analysts, and others.

**3. Forming the Cell.** The Cell is formed from those who respond. Size is from 2 to 6 people (Charter, Article 23). If a task requires more people, several linked Cells are created rather than one unwieldy one.

**4. Coordination and delivery.** A task board, timelines, communication channels, stage reporting, integration with document storage and supporting tools.

**5. Completion and recording.** The platform records the result, distributes rewards where they are provided for, updates the status of participants, and reflects the project's contribution on the general map of activity.

> **On the division into professional and project Cells.** The Charter recognizes one form - a Cell of two to six people. The division into standing professional groupings by competence and temporary project teams is **a technique for organizing work on the platform**, not a separate structure of the people. It may be changed by decision of the Assembly and creates no organs, no powers, and no representation: no Cell has a collective vote or speaks on behalf of other participants.

---

# SECTION 06. Voting and delegation

## One earthling, one vote

Every participant holding a passport and having signed the Declaration has one vote. The vote is not strengthened by a quantity of units of account, by standing within Cells, or by reputation. Economic weight and the right to vote are separated architecturally, not declaratively.

**The right to vote cannot be restricted for a person's views, for how they voted, or as a general measure of liability** (Declaration, Article 10; Charter, Articles 17 and 37). The restrictions provided for by Article 22 of the Charter affect participation in Cells, the right to submit proposals, and access to particular services, but not the vote and not access to votes themselves.

The only case in which the platform executes a suspension of the vote is a decision of the Assembly under Article 22 bis of the Charter for proven undermining of the integrity of voting, for a period of no more than 6 months. The platform executes such a decision and can neither initiate it, nor apply it on any other ground, nor extend it.

## Openness and secrecy

As a general rule votes are open: the fact of participation and the expression of will are available for verification by all participants. Openness is the way to be sure the count is honest.

But transparency extends to the actions of institutions, not to the personal data of people. The platform is therefore obliged to support **a secret ballot with a verifiable count**: the result is verified by everyone, and the link between a vote and the voter is disclosed to no one, including those who operate the platform. The cases in which the secret mode applies are set out in the [Charter, Article 6](https://earth-lings.org/documents/en/en05-charter.html).

A secret ballot applies:

- **as a requirement** - when a restriction of powers is under consideration and on annulment of an invalid issuance of a passport;
- **by decision of the Assembly** - for particular questions or categories, in particular those touching the people's position on the acts of states and on international questions.

In every case the question, the outcome, the number of those who voted, and the result of verifying the count are published.

## Delegation

The platform supports transferring a vote in a particular area to another participant. The Charter's requirements (Article 7) are implemented technically and checked on every operation:

- **by area only** - delegating a vote across all questions at once is technically impossible;
- **no self-delegation** - checked on every operation;
- **no chains** - a delegated vote received cannot be passed on further;
- **a ceiling** - 5 per cent of participants, but no fewer than 10 delegators;
- **one active delegation per area** - a second is impossible without revoking the first;
- **revocation in one step** - at any time, without giving reasons and without the consent of the person the vote was given to;
- **questions with no delegation** - amending the Charter and the basic treasury rules, funding above a set threshold, forming the Emergency Multisig, restricting powers, and annulling the issuance of a passport: on these, votes are cast only in person.

Any earthling may be a delegate: the only selection is the choice made by the delegator (Charter, Article 7).

## The feed of proposals

All proposals are displayed **in chronological order of submission**. The author's reputation does not affect a proposal's place in the feed. Filtering by reputation is available only as a viewing mode that each participant switches on for themselves.

Automatic prioritization of proposals would form the agenda without any formal responsibility for it, and is therefore not implemented in the platform.

## What the platform does within the DAO

- an interface for voting and discussion;
- public recording of decisions taken and of their execution status;
- technical implementation of decisions: changing settings, updating the rules for distributing funds, launching programmes;
- logging of key actions for subsequent audit.

The low-level infrastructure may be anything; the principles do not depend on it.

---

# SECTION 07. The unit of account in the platform

The platform is the main interface for the practical use of the unit of account. The separation between economy and power is observed strictly.

### Internal uses

- reward for contribution to projects and Cells;
- management of internal funds;
- payment for access to particular services and tools;
- support for initiatives: micro-grants, experiments, pilot programmes.

### What the unit of account does not do

- it gives no additional votes and no political weight;
- it does not determine access to basic participation: signing the Declaration, voting, discussions;
- it does not affect a proposal's place in the feed or the priority of its consideration;
- it cannot be used as an instrument of pressure or of excluding people from processes;
- it does not replace national currencies and is not imposed as a means of everyday settlement.

The unit of account reflects contribution and makes it possible to launch projects, but it does not divide people into the important and the unimportant. The platform ensures that economic logic does not destroy equality of participation.

---

# SECTION 08. Data and privacy

The platform is built with the principles of the GDPR and comparable standards in mind. The starting principle: preserving human dignity and the right to a private life matters more than the convenience of analytics.

### Main principles

- **minimization** - only what is genuinely necessary is collected;
- **separation** - identity, participation, economy, and analytics are spread across layers and stores;
- **transparency** - a participant understands what data about them exists and how it is used;
- **control** - a participant may request correction or deletion of the data processed by the platform.

### What happens to data in the distributed ledger

Honesty is needed here, not a promise that cannot be kept.

Data held in the platform's databases are corrected and deleted at a participant's request. Entries in a distributed ledger are by their nature not deletable - and that is precisely why there are no personal data in it: they hold pseudonymous addresses and marks of actions, not a name, not a document, and not biometrics.

On exit the passport is burned, and a pseudonymous mark remains in the ledger recording that belonging existed during a particular period. This is a fact of the past, not a continuing belonging. This model matches the practice settled in European disputes over church registers: the entry is preserved; the status is marked.

Freedom of association does not require the erasure of history: renouncing citizenship does not destroy state archives.

### Identity verification and data protection

- biometrics and documents are processed by the people's own system at the moment of verification; images and scans are not retained;
- the platform receives only the technical result: success or failure;
- on requests from state authorities, the people may confirm the fact of a participant's status where there are lawful grounds, but does not disclose biometric data, which it does not hold;
- entries in the registry follow the principle of pseudonymity and of minimizing personal links.

The platform is not built as a system of total record-keeping. It aims to become an example of careful handling of data in an age when almost everything is technically possible.

---

# SECTION 09. Technical architecture and scalability

Particular technologies - blockchains, databases, languages, frameworks - may change. What matters is the architectural logic:

- **modularity** - the core, the identity subsystem, the DAO component, the economic layer, and the interfaces develop independently;
- **scalability** - the architecture is designed for growth in the number of earthlings by orders of magnitude without loss of availability or security;
- **resilience** - fault-tolerant configurations, backup stores, independent nodes;
- **recovery** - backup copying, a recovery plan for critical failures, protocols for action when keys are compromised;
- **auditability** - the possibility of external technical and legal audit of key components.

The platform is not tied forever to a single technology stack. Through any migration the principles are preserved: non-transferable identity, an equal inalienable vote, verifiability of processes, and protection of the person.

> **The ability to exist without an operator.** The registry of passports is kept on a distributed network, not on the platform's servers. This means that the composition of the people does not depend on who operates the platform today, and is preserved through a change of operator, through a migration of infrastructure, and through a re-founding recognized by the Roadmap as a legitimate continuation.

---

# SECTION 10. Stages of implementation

Both how the target architecture is arranged and how it is to be reached are essential.

**Stage 1. The core - built and deployed.**
The personal account, signing the Declaration, the map of projects, Cell statuses, the voting mechanism, integration with the people's own identity-verification system. The minimum of functions sufficient to begin.

**Stage 2. Cells and projects - built and deployed.**
The cycle of work with Cells: applications, formation, delivery, recording of results. Supporting AI tools for analysing initiatives.

**Stage 3. Filling it with practice - still ahead.**
Regular substantive votes, a secret ballot with a verifiable count, delegation by area, working funds, a wider range of uses for the unit of account. Filling begins when entry opens and proceeds as the number of participants grows.

**Stage 4. External engagement - still ahead.**
Engagement with international organizations, universities, and research centres. Provision of aggregated data for the analysis of global processes. Participation of the people in discussing questions that go beyond a single country.

> **On the boundary of the fourth stage.** What is meant is the right to be heard, not power in the decision. The platform does not become and cannot become a place where decisions binding on anyone other than Earthlings themselves are taken. The powers of states are not affected (Declaration, Article 7).

The division into what is built and what is still ahead is given honestly: the infrastructure exists and has been tested in a working environment, but its evidentiary and practical value arises as participation accumulates, not at the moment of deployment.

---

## Note: the external legal interface

For engagement with traditional legal, administrative, and financial infrastructure, the Earthlings people uses registered legal instruments in various jurisdictions. Such instruments are replaceable operational means of external engagement and do not define the people.

Persons acting through these instruments carry out a mandate of the Assembly, revocable at any time by a simple majority, and form no offices. The detailed legal model is in the document [Legal Basis](https://earth-lings.org/documents/en/en04-legal-basis.html).
