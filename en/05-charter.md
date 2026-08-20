# Earthlings Charter

**The rules by which a decentralized people operates**

The Earthlings people, proceeding from the principles and values set out in the Earthlings Declaration of Self-Determination, and seeking to build a genuinely decentralized and just community, adopts this Charter as its principal organizational document.

We reject traditional hierarchical structures and build governance without hierarchy. Binding decisions are taken only by the DAO Assembly - that is, by Earthlings themselves, each with their own vote. No organ, no structure and no group holds a vote of its own. The particular technical and protective powers provided for by this Charter are exercised under an immediately revocable mandate from the Assembly and do not substitute for decisions taken on behalf of the people.

Every vote is equal, every decision is transparent, every action is verifiable.

## Fundamental Principles

**1 person = 1 vote.** Absolute equality of all Earthlings, regardless of reputation, tokens or role in the community.

**Only people vote.** Project teams and other structures hold no collective vote; only individual participants do.

**A horizontal structure.** Power does not accumulate in any organ and does not rest on a monopoly on coercion; all decisions are taken democratically.

**Smart contracts = execution.** Automation instead of bureaucracy: code executes the rules adopted by people; all operations are transparent.

**Technology = service.** Technical structures provide support without any power of decision.

**Ethics = a reference point.** The Independent Council gives recommendations but does not govern.

**Every mandate is revocable.** No power is granted in the Earthlings people that cannot be revoked immediately and by no higher a threshold than the one that granted it. No mandate constitutes an office and none confers an exclusive right to act.

---

# SECTION 01. Organizational Structure

## Levels

**The level of governance.** The sole decision-making organ. Takes all strategic, financial and organizational decisions.
The DAO Assembly - all Earthlings, 1 person = 1 vote, SBT passport.

**The level of execution (service functions).** Technical and operational structures supporting the DAO: Core Nodes and the Emergency Multisig. They take no strategic decisions; they keep the infrastructure running (Articles 2 and 3).

**The level of consultation (advisory functions).** The Independent Council: ethical oversight and expert recommendations, with no right of veto and no ability to block decisions of the DAO (Article 4).

**The economic layer.** The Treasury and Earthlings Coin: smart contracts for the transparent management of finances, all operations on-chain and public (Articles 9 and 10).

**The key principle.** The power to take binding decisions is concentrated at one level only - in the DAO Assembly. All other levels provide support, consultation and execution, and hold no power to take decisions on behalf of the people.

## Article 1. The DAO Assembly (the Sole Organ of Governance)

The DAO Assembly is the sole organ of governance of the Earthlings people. It comprises all verified Earthlings. It takes all strategic, financial and organizational decisions by direct vote.

**Participants:** natural persons only - Earthlings who have reached the age of 18.
**Voting principle:** 1 earthling = 1 vote (through the SBT passport).

### Thresholds

**Simple majority - 51%, quorum 20%**
- Operational decisions
- Project funding up to 10,000 EC
- Election and revocation of Core Nodes and the Emergency Multisig
- Grant and revocation of the protective legal mandate (Article 33)
- Procedural questions

**Significant majority - 67%, quorum 20%**
- Project funding of 10,000-100,000 EC
- Restriction of powers (levels 1-3)

**Qualified majority - 67%, quorum 25%**
- Changes to the rules of the DAO
- Strategic decisions
- Amendment of the Charter
- Project funding above 100,000 EC

**Sanction majority - 75%, quorum 25%**
- Restriction of powers at levels 4-5 (Article 22)
- Suspension of the right to vote for undermining the integrity of voting (Article 22 bis)
- Annulment of an invalid issuance of a passport (Article 21)

### Voting Mechanisms

- **Delegation by field:** a vote on a particular field may be transferred to another earthling; it is revoked at any time (Article 7)
- **Snapshot:** for off-chain votes and preliminary polls
- **On-chain execution:** automatic execution through smart contracts
- **Standard periods:** 14 days of discussion + 7 days of voting
- **Expedited procedures:** for decisions up to 1,000 EC - 3 days of discussion + 3 days of voting
- **Allocation by support:** for the order of funding among competing projects (Article 11)

## Article 2. Core Nodes (Technical Infrastructure)

Core Nodes are technical coordinators. They keep the platform and the technical infrastructure running. They take no decisions on behalf of the people. They may be revoked by a vote of the DAO at any time.

**Functions (technical only):**
- Support of the DAO platform and infrastructure
- Cybersecurity and defence against attacks
- Technical support of votes
- Audit of smart contracts
- Monitoring of system operation

**What they do not do:**
- They take no decisions on behalf of the people
- They do not manage finances (technical support only)
- They carry no special weight in votes
- They cannot block decisions of the DAO

**Formation:**
- Number: up to 6 people
- Election: vote of the DAO, simple majority (51%, quorum 20%)
- Rotation: every 6 months
- **Revocation: simple majority (51%, quorum 20%), at any time, without giving reasons**
- Reporting: monthly, public

> **Symmetry of thresholds.** Removing someone from a mandate cannot be harder than appointing them to it. The threshold for revoking Core Nodes and the Emergency Multisig equals the threshold for their election. The reverse asymmetry would protect the holder of an office from the people, rather than the people from a concentration of power.

## Article 3. The Emergency Multisig (Rapid Response)

The Emergency Multisig is a multi-signature wallet for urgent technical operations. It consists of six trusted Earthlings. A composition of fewer than six people is not permitted, and until it is elected the wallet is granted no powers.

Signature thresholds are set as a share of the composition, not as an absolute number: an emergency suspension requires not less than two thirds of the composition; administrative operations and contract upgrades require not less than five sixths; the share is rounded up. With a composition of six people, that is four and five signatures.

> **Why exactly six, and not "up to six".** A share of five sixths, with a smaller composition, rounds up to the whole composition: with five signatories it gives five out of five, with three it gives three out of three. One lost or unavailable key would then block contract upgrades and the correction of errors in them permanently. Six is the smallest composition at which the administrative threshold stays below the whole and the design survives the loss of one key. The lower bound here is not a formality: without it, the share requirement is satisfied even by one signature from one signatory - that is, by a multi-signature that does not exist.

**Independence of signatories.** The signatories are different people, each with their own key on their own device. No one person may hold two keys, dispose of another's key, or recover it. A threshold reached by keys under the control of one person is deemed not reached.

The Emergency Multisig may act quickly in emergencies, but only to protect the system. After each such action the DAO Assembly confirms it within 7 days - or annuls it.

**Powers (strictly limited):**
- Suspension of smart contracts on discovery of critical vulnerabilities
- Emergency measures during cyberattacks
- Urgent technical fixes
- Emergency funding up to 5,000 EC in cases of force majeure

**What it cannot do:**
- Take strategic decisions
- Change the rules of the DAO
- Dispose of amounts above 5,000 EC
- Block decisions of the DAO Assembly

**Control mechanisms:**
- Transparency: all transactions are visible on-chain
- Time constraints: actions require a 24-hour timelock (except during critical attacks)
- Mandatory reporting: within 48 hours of an action
- Right of annulment: the DAO may annul any action by simple majority
- Accountability: abuse leads to immediate revocation

**Formation:**
- Election: vote of the DAO, simple majority (51%, quorum 20%)
- Term: 12 months, re-election permitted
- Rotation: at least 2 new people at each rotation
- **Revocation: simple majority (51%, quorum 20%), at any time**

## Article 4. The Independent Council of Earthlings (Ethical Oversight)

The Independent Council is an advisory organ. It carries out ethical audit of decisions, publishes recommendations and expert opinions. The strength of the Council lies in reputation and expertise, not in powers.

**Functions:**
- Ethical audit of DAO decisions
- Public recommendations on difficult questions
- Annual reports on the state of the people
- Expert opinions at the request of Earthlings
- Mediation in conflicts

**Critically important:**
- Its opinions are advisory only
- It cannot block decisions of the DAO
- It holds no right of veto
- It takes no part in the management of finances

**Formation:**
- Number: 7-11 people (an odd number)
- Election: vote of the DAO, qualified majority (67%, quorum 25%)
- Term: 3 years
- Requirements: recognized expertise in ethics, law, ecology or technology; nomination is open to any earthling, including self-nomination

**Revocation of a member of the Council** is effected by a decision of the Assembly at a qualified majority (67%, quorum 25%) - the same threshold at which they were elected, and no higher.

Revocation is possible **only on one of the following grounds**, named and substantiated in the proposal for revocation:

- breach of the duty to declare a conflict of interest;
- systematic non-participation in the work of the Council;
- receiving instructions, remuneration or other benefits from a person with an interest in the content of an opinion;
- loss of the ability to take part in the work.

> **Disagreement with the content of an opinion is not a ground for revocation.** Neither a published position of a member of the Council, nor their dissenting opinion, nor criticism of decisions of the Assembly may serve as a reason for revocation, whether directly or under the guise of another ground. An organ that can be removed for what it has said stops being independent that same day.
>
> Revocation applies to an individual person. Terminating the powers of the entire composition at once is equivalent to abolishing the institution and requires an amendment to this Charter.

A member of the Council may resign by their own decision at any time, without giving reasons.

**Funding of the Council** is provided from a protected budget which cannot be cut without a qualified majority.

**Compensation for the time of Council members** is permitted on the following conditions, which apply cumulatively:

- the amount is set by a decision of the Assembly in advance and is published;
- the amount is the same for all members of the Council and cannot be differentiated;
- payment does not depend on the content of opinions and cannot be reduced, suspended or cancelled for the sitting composition: a change in the amount takes effect only for the next composition;
- a member of the Council may decline the compensation in whole or in part.

No remuneration for holding a seat on the Council is paid beyond such compensation.

> **The current state of the structures.** The Charter constitutes these structures, but they are staffed as the people grows. As of today Core Nodes and the Emergency Multisig have not been elected, the Independent Council has not been formed, and the DAO Assembly has held no substantive votes. Until they are elected, the corresponding functions are performed procedurally during the structure-formation stage, on the responsibility of the founders; the handover of those functions to elected structures is the criterion for moving between the phases of the Roadmap (Article 39).

---

# SECTION 02. Decision-Making Mechanisms

## Article 5. Types of Vote

**Simple majority - 51%, quorum 20%.** Current operational decisions, project funding up to 10,000 EC, election and revocation of Core Nodes and the Emergency Multisig, grant and revocation of the protective legal mandate, annulment of actions of the Emergency Multisig, early lifting of restrictions, appeals.

**Significant majority - 67%, quorum 20%.** Project funding of 10,000-100,000 EC, restriction of powers at levels 1-3.

**Qualified majority - 67%, quorum 25%.** Amendment of the Charter, strategic decisions, project funding above 100,000 EC.

**Sanction majority - 75%, quorum 25%.** Restriction of powers at levels 4-5 (Article 22), suspension of the right to vote for undermining the integrity of voting (Article 22 bis), annulment of an invalid issuance of a passport (Article 21).

**Allocation by support.** Applied to determine the order of funding among projects that have already passed their approval threshold, where their total request exceeds the limit for the field (Article 11).

> **Funding thresholds.** The amounts of 10,000 EC and 100,000 EC that separate the types of vote are set by a decision of the DAO Assembly and are changed without amending the Charter. The figures given here are those in force at the time the Charter is adopted; where they diverge, the decision of the DAO Assembly in force applies.

## Article 6. Voting Procedures

**Standard procedure:**
- Days 1-14: discussion of the proposal, submission of amendments
- Days 15-21: voting (on-chain or Snapshot)
- Day 22: counting of results and publication
- Day 23 onward: automatic execution through smart contracts

**Expedited procedure (for projects up to 1,000 EC):**
- Days 1-3: discussion of the proposal
- Days 4-6: voting
- Day 7: execution

**Emergency procedure (only in cases of force majeure):**
- Initiated by the Emergency Multisig
- 48 hours to vote
- A simple majority is required
- The action takes effect immediately, but may be annulled by the DAO

### Openness and Secrecy of the Ballot

As a general rule, votes within the Earthlings people are open: the fact of participation and the expression of will are available for verification by all Earthlings. Openness is the way to be sure that the count is honest.

Transparency, however, extends to the actions of institutions, not to the personal data of people. There are questions on which openness of the expression of will does not protect a person but exposes them to risk - including from the state of which they are a citizen. In such cases a secret ballot is used while the verifiability of the count is preserved: the result is verified by all, and the link between a vote and the voter is disclosed to no one, including the administrators of the platform.

**A secret ballot is mandatory:**
- when a restriction of powers is under consideration (Article 22)
- when a suspension of the right to vote is under consideration (Article 22 bis)
- when an invalid issuance of a passport is annulled (Article 21)

**A secret ballot may be ordered by a decision of the DAO Assembly** for a particular question or category of questions - in particular, for votes concerning the position of the people on the actions of states and on international matters.

In every case the following are published: the question itself, the outcome, the number of those who voted, and the result of the verification of the count.

## Article 7. Delegation of Votes

An earthling may delegate their vote on a particular field to another earthling. Delegation is voluntary and is revoked at any time.

> **Delegation is not representation.** It is given by field, not for a term; it is revoked immediately, without giving reasons and without the delegate's consent; it constitutes no office and gives the delegate no rights other than casting the votes transferred to them. A delegate may at any time be left without a single delegated vote, and that is the mechanism working normally, not a failure.

**Who may be a delegate.** Any earthling. Neither reputation, nor length of participation, nor merit opens or closes access to receiving delegated votes: the only selection is the delegator's own choice.

**Transparency:**
- A public on-chain history of the delegate's decisions
- All votes cast by the delegate are visible
- No special privileges: 1 delegated vote = 1 vote

**Limits on delegation:**
- **By field only.** A vote cannot be delegated across all questions at once. A field is a thematic category (ecology, technology, economics, law, education) or a particular Cell.
- **No self-delegation.** An earthling cannot delegate a vote to themselves. The limit is implemented technically and is checked at every delegation operation.
- **No chains.** A delegated vote received cannot be passed on further.
- **A ceiling on delegation.** The ceiling is 5% of Earthlings, but not fewer than 10 delegators; the 5% limit therefore begins to bind a delegate only above 200 Earthlings.
- **One active delegation per field.** Delegating the same field again is impossible without revoking the previous one.
- **Revocation at any time** - without giving reasons and without the delegate's consent.
- **Questions on which delegation does not apply.** Amendment of the Charter and of the basic rules of the Treasury, funding above 100,000 EC, formation of the Emergency Multisig, restriction of powers (Article 22), suspension of the right to vote (Article 22 bis), annulment of the issuance of a passport (Article 21), and amendment of the unamendable principles - on these an earthling votes only in person.

**The purpose of these limits:** delegation provides competence on specialized questions without giving rise to standing factions. The prohibition on delegating across all questions at once separates this mechanism from representation. The ceiling excludes the concentration of a significant share of votes in one person, the prohibition on chains excludes the formation of pyramids, and the prohibition on self-delegation excludes the artificial building up of one's own weight.

## Article 8. The Reputation System

**Critically important:** reputation has no effect on the weight of a vote and opens access to no role. The principle "1 person = 1 vote" is absolute. Reputation is informational only.

**Reputation factors (on-chain):**
- Participation in votes
- Successful delivery of projects
- Contribution to the development of the community
- Quality of proposals
- Assessments by other participants

**Use of reputation:**
- **A chronological feed by default:** all proposals are displayed in the order submitted, and the author's reputation has no effect on their place in the feed. Filtering by reputation is available as an optional viewing mode which each earthling switches on for themselves
- Reference information when choosing a delegate
- No effect on the weight of a vote
- Not a condition for receiving delegated votes, or for nomination to Core Nodes, the Emergency Multisig or the Independent Council

**Rationale:** automatic prioritization of proposals by reputation shapes a de facto agenda without formal accountability. A chronological feed provides equal access to the community's attention regardless of a history of participation. Any mechanism in which reputation opens access to accumulating votes turns it into a hidden voting weight and is therefore excluded.

---

# SECTION 03. The Economic System

## Article 9. The Earthlings Treasury

The Earthlings Treasury is managed through smart contracts. All operations are transparent and recorded on-chain. The allocation of funds is approved by a vote of the DAO.

**Sources of funds:**
- Contributions on joining (the procedure and purpose are set out in the document [Earthlings Treasury](https://earth-lings.org/documents/en/en09-treasury.html))
- Voluntary contributions from Earthlings
- Grants and donations
- Issuance of Earthlings Coin (under the established rules)
- Other sources approved by the DAO

The annual budget of the Fund is allocated across the principal fields approved by the DAO Assembly. The current proportions and a description of each category of expenditure are documented in the [Earthlings Treasury](https://earth-lings.org/documents/en/en09-treasury.html). The proportions are changed only by a qualified majority (67%) of the DAO Assembly.

## Article 10. Earthlings Coin (EC)

**Characteristics:**
- A utility token of the Earthlings ecosystem
- No effect on the weight of a vote (1 person = 1 vote regardless of the amount of EC)
- Used to pay for services within the community
- Transparent issuance under the established rules
- Cannot be exchanged for a vote, for priority of a proposal, or for any other advantage in decision-making

**Inheritance.** Earthlings Coin, as crypto-assets, is inherited in accordance with the applicable law and where the heirs have access to the wallet. The Earthlings people bears no obligation to transfer assets to heirs and has no technical ability to restore access to a wallet. A passport is not inherited under any circumstances: it is non-transferable.

The details of the economic model are described in the document [Earthlings Coin](https://earth-lings.org/documents/en/en10-earthlings-coin.html).

## Article 11. Project Funding

**The funding process:**

1. **Submission of an application** through the platform, with a description of the project, the budget and the team
2. **Discussion:** 14 days (or 3 days for projects up to 1,000 EC)
3. **Approval vote:** 51% at a quorum of 20% (up to 10,000 EC); 67% at a quorum of 20% (10,000-100,000 EC); 67% at a quorum of 25% (above 100,000 EC)
4. **Determination of order** - if the total request of approved projects exceeds the limit for the field (see below)
5. **Payment:** automatic through a smart contract, by milestones
6. **Reporting:** public and on-chain on completion of each milestone

### Allocation by Support

When several projects have passed the approval threshold but the funds of the field are not enough for all of them, the order is determined as follows:

- Each earthling marks all the projects they consider worth funding - one, or all of them. The number of marks is not limited and costs nothing.
- The number of marks for each project is counted.
- Projects are funded in descending order of the number of marks, until the annual limit for the field is exhausted.
- Projects that receive no funding in the current cycle keep their approval and take part in the next allocation without a further vote.

> **Why this way.** Every earthling has the same, inexhaustible ability to support any number of projects. There is no budget of votes here that can be spent, concentrated or bought: priority is formed from the number of people who gave support, not from who put more weight behind their support. Any mechanism that allows one person to cast more weight than another in a single decision contradicts Article 37 of this Charter and is not used within the Earthlings people.

The details of how project work is organized are described in the document [Earthlings Cells](https://earth-lings.org/documents/en/en08-cells.html).

---

# SECTION 04. Belonging and Verification

## Article 12. Principles of Participation

Participation in the Earthlings people is open to all persons who have reached the age of 18, have accepted the Earthlings Declaration and have passed identity verification.

There are no other conditions. Nationality, race, religion, sex, social position, citizenship and place of residence have no bearing on the ability to join.

## Article 12 bis. The Entry Contribution and Payment for Another

Identity verification and the issuance of a passport are covered by a one-time contribution on joining. The contribution buys no belonging and creates no advantage of any kind (Declaration, Article 8). The purpose of the contribution and the procedure for spending it are established by the Earthlings Treasury (Article 9). The amount of the contribution is set by the Assembly; it may be increased only by a decision of the Assembly.

There is no exemption from the contribution. The contribution is always paid in full; what differs is only who pays it.

**An open queue.** A person who cannot pay the contribution themselves joins an open queue by a single action. An application, evidence and an explanation of reasons are not required and cannot be required. Placement in the queue cannot be refused.

**What is published.** The queue publishes a sequence number and the date of placement. Name, country, reason and any other information about the person are not published.

**Order of payment.** The head of the queue is paid for. Choosing a particular person is not permitted. The payer is not told whom they paid for; the person paid for is not told who paid the contribution for them.

**Who may pay.** Any person, whether or not they belong to the Earthlings people. The payer's name is published at their choice.

**Equality of passports.** The registry does not record who paid a contribution. A passport paid for by another person is in no way different from any other; payment for another affects neither status, nor vote, nor the scope of participation. Creating a separate category of such participants is not permitted.

**Payment from the Treasury.** The Assembly may set a share of incoming contributions to be directed to paying the queue (Treasury, Article 3 bis).

## Article 13. The Verification System

**Protection of the principle "1 person = 1 vote":**
- **Biometric verification:** confirmation of the uniqueness of a person
- **Soulbound Token (SBT):** a non-transferable token of belonging
- **Data minimization:** only what is necessary to confirm uniqueness is processed; photographs and scans are not retained
- **Anti-Sybil protection:** prevention of the creation of multiple accounts

The personal and biometric data of participants is not public under any circumstances.

## Article 14. The Rights of Earthlings

- Participation in votes with equal voting weight
- Creation of proposals and initiatives
- Participation in community projects
- Delegation of a vote by field
- Access to all information on the platform
- Participation in debate and discussion
- Leaving the people at any time

## Article 15. The Duties of Earthlings

- Observance of the principles of the Earthlings Declaration
- Respect for other participants
- Conscientious participation in votes
- Transparency in delivering projects
- Reporting on the use of the Fund's resources

## Article 16. Declaring a Conflict of Interest

An earthling is obliged to declare a conflict of interest openly in any situation where their personal interest may affect the objectivity of a decision.

**A conflict of interest arises where an earthling:**
- has a direct or indirect material benefit from the outcome of a decision
- is connected by family, business or other significant relations with the persons or organizations that the decision concerns
- represents the interests of third parties or organizations in the matter under consideration

Declaring a conflict of interest does not in itself deprive an earthling of the right to vote. Mandatory recusal applies in votes on the allocation of funds: an earthling does not take part in such a vote if they are the applicant or a co-author of the application, are part of the project team, are closely related to the applicant (spouse, parents, children, siblings), or have contractual obligations towards them that provide for remuneration.

No other grounds for excluding a vote exist: an earthling's vote is not excluded from the count by a decision of a majority.

Deliberate concealment of a conflict of interest is treated as a breach of ethical rules and may entail a restriction of powers under Article 22.

---

# SECTION 05. Change in the Status of an Earthling

## Article 17. Fundamental Principle

Belonging to the Earthlings people is inalienable. No one can be expelled from the Earthlings people under any circumstances. Having become an earthling, a person remains one until they themselves decide to leave.

**The right to vote cannot be taken away or suspended for a person's views, for the content of their vote, for disagreement with decisions taken, or as a general measure of liability for breaking rules.** The vote is the substance of belonging: to take it away on such grounds would be to expel a person from the people while leaving them the name. The restrictive measures provided for by Article 22 do not affect the right to vote.

The only permissible exception is established by Article 22 bis and concerns acts directed at undermining the integrity of voting itself. The list of grounds is not subject to extension.

This principle follows from the Earthlings Declaration: freedom belongs to everyone, and no majority has the power to deprive a person of belonging to a people they joined voluntarily.

## Article 18. Voluntary Departure

Every earthling has the right at any time to end their participation in the Earthlings people voluntarily. This right is unconditional and requires no explanation of reasons.

**The procedure for voluntary departure:**

1. The earthling submits a statement of departure through their account on the Earthlings platform
2. The system requests a separate confirmation of the decision and warns of the consequences. By default a pause of 72 hours is kept between the statement and the burning - this is a protection against impulsive decisions, and the earthling may waive it. The Earthlings people can neither delay a departure nor cancel it: burning is always available to the earthling directly from their own wallet
3. After confirmation the earthling burns the SBT passport with their own key (the `burnByHolder` function). The Earthlings people does not hold a participant's keys and can neither perform the burning for them nor prevent it; access to votes and internal services ends
4. Departure takes effect from the moment the SBT passport is burned

**Earthlings Coin on departure.** Tokens held in the wallet of a departing earthling remain their property: they are not confiscated and not annulled. After losing the status of an earthling the holder loses the right to vote in the DAO and access to internal services; further use of the tokens depends on their technical accessibility and on the applicable law of the relevant jurisdiction.

**Rejoining.** A person who has voluntarily left the Earthlings people has the right to rejoin at any time by going through the standard procedure - verification and the one-time entry contribution covering its cost price (the contribution may also be paid under Article 12 bis) - and receiving a new SBT passport. A previously burned passport is no impediment to returning: verification data are retained only so that one person cannot hold two valid passports at once.

## Article 19. Suspension of Status

An earthling has the right to suspend their status temporarily without leaving entirely.

**Grounds for suspension:**
- personal circumstances requiring a break
- a prolonged inability to take part in the life of the community
- other reasons at the earthling's discretion

**Consequences of suspension:**
- the SBT passport is retained but marked as "suspended"
- the right to vote is suspended by the earthling's own decision
- the vote of a suspended earthling is not counted towards the quorum
- access to information resources is retained
- Earthlings Coin remains in the wallet without restriction

**Duration of suspension.** A suspension lasts until the earthling states that they are resuming participation, but no longer than 12 months. After 12 months the system sends a request as to their intentions. If no answer is received within 30 days, the status becomes "inactive".

**Resumption.** To resume active status a statement through the account is enough. Repeat verification is not required.

## Article 20. Inactive Participants

An earthling is deemed inactive if they:
- have taken part in no vote for 12 months
- have performed no action on the platform for 12 months
- have not answered a request to confirm their status

**Consequences of inactivity:**
- the SBT passport is retained but marked as "inactive"
- the vote of an inactive earthling is not counted towards the quorum
- the right to vote is retained and may be exercised at any time
- on the first action (a vote, a login to the platform) the status is restored automatically

The inactivity mechanism protects the system from an artificial inflation of quorum requirements, while preserving the right of every earthling to return to participation at any time.

## Article 21. Burning a Passport Against the Holder's Will

As a general rule an SBT passport is burned only by the holder themselves (Article 18). This Article establishes **two and only two** exceptions to that rule.

> **Why death is not on this list.** Belonging ends upon the death of a person - this is established by Article 8 of the Declaration and occurs of itself, without anyone's decision. A passport is not burned on that ground, and for the following reasons. The people has, and can have, no access to records of death across the world: such a ground would rest on information whose reliability there is no way to check, and it would become the cheapest way to remove a participant - without notice, without a period for objections and without appeal, since all of these presuppose the person's presence. Nor does burning provide protection against voting with someone else's key: it cannot outrun knowledge of the death. The practical side is covered by Article 20: whoever does not take part is deemed inactive, their vote is not counted towards the quorum, and the passport is retained. The system does not need to know why a person stopped taking part.

### 1. Annulment of an Invalid Issuance

A passport may be annulled if it is established that it was issued in breach of the conditions of issuance: more than one valid passport has been issued to one person, or verification was passed using false data or another person's identity, or the passport was issued to a person below the age established by this Charter. The list of grounds is closed and corresponds to Article 8 of the Declaration.

If more than one valid passport has been issued to one person, the issuance of all but the first is annulled. The person's belonging to the people is preserved.

**Procedure:**
- Initiation: a substantiated submission with evidence, made by any earthling or by Core Nodes following a technical check
- Notice to the holder and a period of not less than 21 days to submit objections; the holder may enlist other Earthlings in their support
- An opinion of the Independent Council (in its absence, the discussion period is doubled). The opinion is an opinion: it does not replace the decision of the participants, does not predetermine it, and does not bind them (Declaration, Article 11)
- Vote: **sanction majority of 75% at a quorum of 25%, secret, without delegation**
- Appeal within 30 days; a simple majority (51%, quorum 20%) is enough to overturn the decision

Annulment is not expulsion from the people and is not applied as a measure of liability for conduct. It establishes only that the issuance did not lawfully take place. A person whose passport has been annulled has the right to undergo verification again on general terms, once the impediment to lawful issuance has been removed.

### 2. Technical Reissue

A passport may be burned and immediately reissued to the same address or to a new address of the holder, at the holder's own request - on loss of access to the wallet or on migration of the contract. Reissue does not interrupt belonging and requires no vote.

**No other grounds for burning a passport against the holder's will exist.**

## Article 22. Restriction of Powers

Where the rules and principles of the Earthlings people are breached, restrictive measures may be applied to an earthling. A restriction of powers does not deprive a person of the status of an earthling and **does not affect their right to vote** (Article 17). What is restricted is only what involves the spending of common attention and common resources.

### Types of Restriction

**Level 1 - Warning.** A public record of the breach without restriction of rights. It remains in the history and is taken into account when subsequent breaches are considered.

**Level 2 - Restriction of participation in Cells.** A temporary prohibition on creating new Cells or joining existing ones. Duration: from 1 to 12 months.

**Level 3 - Restriction of the right of initiative.** A temporary prohibition on submitting proposals to the DAO. The right to vote on the proposals of others is fully retained. Duration: from 1 to 12 months.

**Level 4 - Restriction of access to services.** Restriction of access to particular services of the platform. Access to votes, to information and to one's account is not restricted under any circumstances. Duration: from 1 to 24 months.

**Level 5 - Combined restriction.** A combination of several restrictions at levels 2-4. Applied in cases of systematic or gross breaches. Duration: from 6 to 36 months.

> Suspension of the right to vote is not among the measures listed. None of the grounds in this Article - neither a breach of ethical rules, nor spam, nor reputational damage - affects the right to vote. The sole ground for suspending a vote is established separately, by Article 22 bis, and does not concern a participant's conduct outside the voting mechanism.

## Article 22 bis. Suspension of the Right to Vote

This Article establishes the **sole** case in which the right to vote may be suspended, and it is exhaustive.

### The Ground

Suspension is applied only for proven acts directed at undermining the integrity of voting itself:

- collusion aimed at a coordinated distortion of the result;
- buying or selling a vote, and equally offering or accepting any reward for voting in a particular way;
- compelling other participants to vote in a particular way, including blackmail and threats;
- circumventing the rule of "one person, one passport", or assisting such circumvention.

### What Is Not a Ground

None of the following may serve as a ground for suspending a vote, however it is presented:

- a participant's views, their convictions, faith and political position;
- the content of their vote and how they voted previously;
- disagreement with decisions taken, criticism of the structures of the people and of the founders;
- breach of any other rules listed in Article 22;
- an assessment of a participant's mental state, legal capacity or competence.

> **Why the line is drawn precisely here.** The vote is protected **as a vote**. Whoever attacks the voting mechanism itself attacks what gives every person's vote its meaning - and for that reason loses their own. Whoever votes "wrongly" undermines no mechanism, and their vote is inviolable.
>
> Such a ground cannot be applied to a dissenter: for it to work, a specific act against the mechanism must be proved, not an opinion about a person.

### Procedure

The procedure follows Article 22, with the following particulars:

- **duration** - up to 6 months; extension is not permitted, and repeat application is possible only for a new proven act;
- **threshold** - sanction majority, 75 percent at a quorum of 25;
- **voting** - secret, without delegation;
- **a mandatory opinion of the Independent Council**; in its absence the period of public discussion is doubled;
- **the right to a defence** - full information about the allegations, the opportunity to present one's position and to enlist other participants in one's support, not less than 21 days;
- **proof** - the burden of proving the act lies on the initiator; where doubt cannot be removed, the measure is not applied;
- **appeal** within 30 days; a simple majority is enough to overturn;
- **early lifting** at any time by a simple majority.

Suspension of the right to vote does not affect belonging to the people, which is inalienable, and does not entail expulsion under any circumstances.

### Grounds for Restrictions

- breach of the ethical rules of the Earthlings people
- deliberate concealment of a conflict of interest
- abuse of DAO mechanisms (spamming proposals, manipulation)
- acts causing reputational damage to the Earthlings people
- breach of the confidentiality of other Earthlings
- systematic failure to perform voluntarily assumed obligations

### Procedure for Application

1. **Initiation.** Any earthling or group of Earthlings (not fewer than 5 people) may initiate consideration by submitting a substantiation
2. **Preliminary consideration.** The Independent Council considers whether the initiative is well founded within 14 days and publishes a recommendation
3. **The right to a defence.** The earthling has the right to receive full information about the allegations, to present their position and to enlist other Earthlings in support
4. **Discussion.** Not less than 14 days (levels 1-3) or 21 days (levels 4-5)
5. **Vote.** Levels 1-3: 67% at a quorum of 20%. Levels 4-5: 75% at a quorum of 25%. The vote is **secret, without delegation** (Articles 6 and 7)
6. **Execution.** Restrictions take effect 48 hours after the vote closes

**Early lifting.** Restrictions may be lifted early at any time by a decision of the DAO at a simple majority (51%, quorum 20%). It may be initiated by the earthling themselves or by any other earthling.

> Raised thresholds protect against imposing restrictions, not against lifting them: lifting a restriction is always easier than imposing one.

**Appeal.** An earthling has the right to appeal a decision within 30 days. The appeal is considered by the DAO Assembly. A simple majority (51%, quorum 20%) is enough to overturn the decision.

---

# SECTION 06. Cells - the System of Cooperation

## Article 23. The Nature of Cells

Cells are autonomous small teams of Earthlings that come together to deliver particular projects, research or initiatives. Cells operate openly within the Digital Platform, and any earthling may look at their projects.

**Principles of how Cells work:**
- **Autonomy** - Cells determine their own structure, working methods and distribution of roles
- **Voluntariness** - joining a Cell and leaving it are entirely free
- **Transparency** - the activity of Cells is open to all Earthlings
- **Contribution to the common good** - 5% of a Cell's profit is directed to the Earthlings Treasury
- **Human scale** - a Cell has from 2 to 6 participants; if a task requires more people, several Cells are created rather than one large one

## Article 24. Creating and Dissolving Cells

Any earthling may initiate the creation of a Cell by joining with other Earthlings around a particular aim or project. Registration takes place on the Digital Platform, stating:
- the name and a short description of the Cell
- the aim and field of activity
- the composition of participants
- the projects planned

## Article 25. Autonomy and Limits

The DAO Assembly does not coordinate the day-to-day work of Cells. Cells act autonomously within the principles of the Earthlings Declaration and of this Charter.

**The DAO intervenes only in exceptional cases:**
- systematic breach of the ethical principles of Earthlings
- irresolvable conflicts within a Cell
- attempts to seize resources or to monopolize fields
- acts damaging the reputation of the Earthlings people

Decisions on sanctions against a Cell are taken by a qualified majority of the DAO after an independent investigation. Sanctions against a Cell do not entail any restriction of the rights of its participants as Earthlings; a restriction of an individual person's powers is possible only under Article 22.

## Article 26. The Economics of Cells

Cells may receive payment for their work both in Earthlings Coin and in fiat currency. The participants of a Cell distribute the income among themselves according to their own arrangements.

A contribution to a Cell may be labour, expertise or capital. Capital is accounted for on the same footing as other contributions and receives a fair, capped final return, but never gives a vote, control over the Cell, or a perpetual rent: governance of a Cell always remains on the principle of "one person, one vote". Governance accounting and economic accounting are kept separately. The detailed model is described in the document [Earthlings Cells](https://earth-lings.org/documents/en/en08-cells.html).

**Mandatory contribution to the Fund:**
- 5% of a Cell's profit is transferred to the Earthlings Treasury
- The deduction may be made in EC, in fiat or in stablecoin through transparent mechanisms
- These funds support the common infrastructure and the projects of the people

## Article 27. Legal Status

The participants of a Cell may, by their own decision, create a legal structure (a company, a cooperative, a partnership) for working with clients who intend to pay for the Cell's services in fiat. Such structures are created by the participants in their own name, and not on behalf of the Earthlings people.

Each participant of a Cell is individually responsible for complying with the tax law of their country of residence (for more detail see [Earthlings Cells](https://earth-lings.org/documents/en/en08-cells.html)).

The Earthlings people owns no territory and lays no claim to any. Any physical premises, equipment or other property used by a Cell or its participants, including a coworking space or a meeting place, belongs to particular participants or to the legal structures they have created and lies within their own local legal and tax responsibility, and not in the ownership or under the jurisdiction of the Earthlings people.

---

# SECTION 07. The Digital Platform and Security

## Article 28. Components of the Platform

- The identification and verification system (biometrics + SBT)
- The voting system, including the mechanism of a secret ballot with a verifiable count
- Coordination of Cells
- The smart contracts of the Fund
- The communication system
- The educational platform
- The analytics system (on-chain data)

## Article 29. Security

The security of the platform is critical for protecting the autonomy and privacy of Earthlings.

**Security measures:**
- Modern end-to-end encryption
- Multi-factor authentication
- Distributed data storage
- Decentralized infrastructure

An independent audit of the smart contracts and a vulnerability bounty program are planned before operations are expanded.

## Article 30. Openness of the Code

The code of the passport smart contract is open (MIT license). The code of the platform and of the identity verification system is closed: they work with personal data. The list, with reasons, is in the document [Where We Are Now](https://earth-lings.org/documents/en/en32-where-we-are-now.html).

---

# SECTION 08. Participation of Legal Entities

## Article 31. Principles of Interaction

Legal entities may interact with the Earthlings people but hold no right to vote. Only natural persons - Earthlings - vote.

**Forms of participation:**
- Partnership in delivering projects
- Funding of projects and grants
- Provision of expertise and resources
- Technical support of initiatives

**Limits:**
- They cannot vote in the DAO Assembly
- They cannot influence strategic decisions
- They cannot be members of Core Nodes or of the Emergency Multisig
- All interactions are transparent and approved by the DAO

---

# SECTION 09. Crisis Management

## Article 32. Types of Crisis

**Technical.** Cyberattacks, vulnerabilities in smart contracts, infrastructure failures.
**Economic.** Sharp changes in the value of EC, liquidity problems of the Fund.
**Legal.** Legal pressure, prohibitions in jurisdictions, court demands with strict deadlines for compliance.
**Social.** Loss of trust, a split in the community, conflicts.

## Article 33. Response Mechanisms

### Level 1: a technical crisis
- The Emergency Multisig acts immediately
- Suspension of vulnerable smart contracts
- Notification of the community within 1 hour
- A full report within 48 hours

### Level 2: a decision of the DAO is required
- An emergency vote (a shortened period of 48-72 hours)
- Core Nodes prepare options for decision
- The Independent Council gives recommendations
- The DAO takes the final decision

### Level 2a: a legal crisis - the protective legal mandate

The deadlines of legal demands are often shorter than any voting procedure: a court request may have to be answered within 48 hours. For such cases the Assembly grants a protective legal mandate in advance.

**This is a mandate, not an office.** It confers no exclusive right to act on behalf of the people, constitutes no organ, and creates no powers beyond those expressly listed below.

- **Grant.** The DAO Assembly, by a simple majority (51%, quorum 20%), mandates one or two Earthlings with legal training to take protective actions in the legal sphere without a prior vote.
- **Revocation.** The mandate is revoked at any time by a simple majority (51%, quorum 20%), without giving reasons. The threshold for revocation equals the threshold for the grant and cannot be raised.
- **A closed list of permitted actions.** Answers to requests from state authorities and courts; recording the legal position of the people; retaining counsel; taking procedural steps where missing a deadline entails adverse consequences. No other actions are permitted.
- **Express prohibitions.** The mandate confers no right to admit claims on the merits, to dispose of or encumber assets, to assume obligations above 5,000 EC, to change the structure of the people, to conclude agreements binding the people for the future, or to act on behalf of the people on matters unrelated to the defence in a particular legal proceeding.
- **Reporting.** A mandatory public report within 24 hours of each action.
- **Annulment of what has been done.** The DAO may annul or adjust any action by a simple majority.
- **Automatic expiry.** The mandate ends of itself 30 days after it is granted, and also at the moment the DAO takes a decision on the substance of the situation. Extension requires a new vote.
- **Non-exclusivity.** The existence of the mandate does not limit the right of the Assembly to take a decision on the same matter at any time; such a decision prevails.

### Level 3: an existential crisis
- Convening an extraordinary assembly
- The possibility of temporarily suspending operations
- Deep analysis and reform of the structures
- A qualified majority for critical changes

---

# SECTION 10. International Relations

## Article 34. Principles

- Respect for international law and the sovereignty of states
- Peaceful cooperation and the non-violent resolution of conflicts
- Priority of interests common to all humanity
- Transparency and openness
- Partnership on equal terms

The Earthlings people does not interfere in the internal affairs of states and takes no part in political struggle at the national level.

## Article 35. Legal Personality

The Earthlings people works towards legal cognizability: towards being treated as a people wherever a specific question arises. No organ that recognizes peoples exists for anyone, so cognizability accumulates through practice, time and the number of participants, and is not issued by decision. As stated in Article 7 of the Declaration, law has not yet addressed the question of the acquisition of international legal personality by a community that has never held territory.

Until legal cognizability has accumulated, the people operates for external dealings through legally registered structures - replaceable legal interfaces - in the relevant jurisdictions. The legal strategy is described in the document [Legal Basis](https://earth-lings.org/documents/en/en04-legal-basis.html).

---

# SECTION 11. Amendment of the Charter

## Article 36. Procedure for Making Amendments

**A qualified majority of 67% at a quorum of not less than 25%.**

**Stages:**
1. **Proposal.** Any earthling may propose an amendment
2. **Discussion.** A minimum of 21 days
3. **Expert review.** The Independent Council gives an advisory opinion
4. **Vote.** 14 days, qualified majority of 67%
5. **Entry into force.** 7 days after approval

An amendment that contradicts the Earthlings Declaration is not to be put to a vote, and if adopted has no force (Article 38).

## Article 37. Unamendable Principles

The following principles cannot be changed even by a qualified majority:

- **1 person = 1 vote.** Absolute equality of all Earthlings. No mechanism may allow one person to cast more weight than another in a single decision
- **The vote is inalienable.** The right to vote cannot be taken away or suspended for views, for the content of a vote, for disagreement with decisions, or as a general measure of liability, nor made conditional on money, reputation, length of participation or merit. The sole exception is undermining the integrity of voting itself (Article 22 bis); the list of its grounds is not subject to extension
- **Only people vote.** Structures hold no collective vote
- **Openness and transparency of decisions and finances.** All decisions of the DAO, the outcomes of votes, the financial transactions of the Fund and the actions of executive structures are public and verifiable. The personal and biometric data of participants is not public - it is protected by Article 13. Transparency extends to the actions of institutions, not to the personal data of people; the expression of will of a particular person is personal data and may be closed under Article 6
- **Voluntariness.** Participation and departure are free; expulsion is impossible
- **Revocability of every mandate.** A power that cannot be revoked immediately and at a threshold no higher than the threshold of its grant is not granted

> **Relation to the Declaration.** The principles listed are the operational expression of the unamendable core of the Earthlings Declaration - the life, dignity and freedom of the person, planetary solidarity, care for the planet and the refusal of concentrated power. They cannot narrow that core and are construed only in its favour.

---

# SECTION 12. Final Provisions

## Article 38. Entry into Force and the Hierarchy of Documents

This Charter enters into force upon its publication on the website of the Earthlings people, earth-lings.org.

**The hierarchy of the documents of the Earthlings people:**

1. **The Earthlings Declaration of Self-Determination** - the founding document, holding the highest force. A provision of any other document that contradicts the Declaration has no force from the moment of adoption and is not to be applied
2. **This Charter** - the principal organizational document
3. **Derivative documents** - where the Charter and a derivative document diverge, the Charter applies

A contradiction of the Charter with the Declaration, once discovered, is removed by bringing the Charter into accordance with the Declaration, and not the other way round.

**Division of subject matter.** The Declaration establishes principles, the guarantees to the person, and the limits of the people. The principles of its unamendable core are never abolished; the wording of those principles and its other provisions are changed only by the Assembly, in the manner provided by Article 13 of the Declaration and only so that no guarantee to the person becomes weaker. The Charter establishes mechanisms, thresholds, time limits and procedures; it is amended in the manner provided by Article 36. Numerical values, technical means and organizational detail are not carried over into the Declaration.

## Article 39. The Structure-Formation Stage

The structure-formation stage continues until the following conditions are satisfied at once:

- the technical infrastructure for voting and the treasury is deployed
- the first Core Nodes and Emergency Multisig have been elected
- the Independent Council has been formed
- not fewer than three substantive votes of the DAO Assembly have been held

Until that moment the functions of unelected structures are performed procedurally and on the responsibility of the founders, and the stages of procedures that provide for the participation of the Independent Council are omitted, with the periods of public discussion of the corresponding questions doubled.

> **On the use of the word "founders".** In this Charter it means only those who, before the structures are elected, perform their functions procedurally, and nothing beyond that. It creates no rights in governance, no weight in voting and no special status as a participant: there is no class of founders in the Earthlings people, and that provision forms part of the unamendable core of the Declaration. The functions named end with the completion of the structure-formation stage and do not pass by inheritance.

The founders publish a report on the state of the structure-formation stage not less than once every 90 days. The report contains a list of the conditions not yet satisfied and the reasons.

The completion of the structure-formation stage is recorded by a decision of the DAO Assembly and is the criterion for moving between the phases of the Roadmap.

---

# ANNEX. Summary Table of Decision-Making

This table systematizes the voting thresholds and the procedures. Where the table and the text of the corresponding section conflict, the text of the document prevails.

## Decisions of the DAO Assembly

**Current questions - 51%, quorum 20%**
Approval of Cell projects, allocation of grants up to 10,000 EC, election **and revocation** of Core Nodes and the Emergency Multisig, grant and revocation of the protective legal mandate, annulment of actions of the Emergency Multisig, early lifting of restrictions, appeals, procedural questions.
Timing: 14 days of discussion + 7 days of voting.

**Significant questions - 67%, quorum 20%**
Project funding of 10,000-100,000 EC, restriction of powers at levels 1-3.
Timing: 14 days of discussion + 7 days of voting.

**Critical questions - 67%, quorum 25%**
Amendment of the Charter, strategic decisions, project funding above 100,000 EC, formation of the Independent Council.
Timing: 21 days of discussion + 14 days of voting.

**Sanction questions - 75%, quorum 25%**
Restriction of powers at levels 4-5 (Article 22), annulment of an invalid issuance of a passport (Article 21). The vote is secret; delegation does not apply.
Timing: 21 days of discussion + 14 days of voting.

**Allocation by support**
The order of funding among projects already approved where the funds of a field are short. Marks of support without any limit on their number; funding in descending order of the number of supporters.

## Powers of the Executing Structures

**Core Nodes.** Technical support of the infrastructure, preparation of proposals for the DAO, coordination between Cells. They take no decisions on the allocation of resources and do not vote on behalf of the DAO. Rotation every 6 months, revocation by simple majority at any time.

**Emergency Multisig.** Emergency suspension of smart contracts where security is threatened, protective action during cyberattacks, emergency funding up to 5,000 EC. A mandatory report within 48 hours, retrospective ratification by the DAO within 7 days, revocation by simple majority at any time.

**The protective legal mandate.** Protective actions in a particular legal proceeding, on a closed list. A report within 24 hours, automatic expiry after 30 days, revocation by simple majority at any time.

**The Independent Council.** Ethical audit, recommendations, public opinions. Advisory in character, with no right of veto. An annual public report, re-election every 3 years.
