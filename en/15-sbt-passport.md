# The earthling SBT passport

**A digital certificate of belonging to the Earthlings people**

> This document describes the design and legal significance of the passport. Where they diverge, the [Charter](https://earth-lings.org/documents/en/en05-charter.html) applies; where the Charter diverges from the [Declaration](https://earth-lings.org/documents/en/en01-declaration.html), the Declaration applies. The procedure for entering is described in the document [The Earthling Path](https://earth-lings.org/documents/en/en14-the-earthling-path.html).

---

## What it is

The earthling SBT passport is a non-transferable digital token (a Soulbound Token) issued to every participant after they sign the Declaration, confirm their identity, and make the contribution. It cryptographically confirms belonging to the people and is held in a distributed ledger as a unique record protected against forgery.

Unlike state passports, which are tied to a territory and confirm citizenship, this passport confirms belonging to a people united by shared values. It cannot be transferred to another person, sold, or alienated.

**Non-transferability.** The passport is tied to your wallet, and transfer is blocked in the contract itself, not by a rule that can be worked around. The uniqueness of the person is confirmed at issuance.

**Cryptographic protection.** The record is held on a distributed network and cannot be forged or altered unnoticed.

**Equality.** Everyone receives the same passport with the same rights. There are no privileged classes and no tiers of membership. One person, one passport, one vote.

---

## What the passport gives

### Participation in governance

- the right to vote in the DAO Assembly;
- the submission of proposals and initiatives;
- participation in decisions on every question.

> **The vote is inalienable** and cannot be taken away or suspended for a person's views, for how they voted, for disagreement with decisions, or as a general measure of liability (Declaration, Article 10; [Charter, Articles 17 and 37](https://earth-lings.org/documents/en/en05-charter.html)). The vote is the substance of belonging: by taking it away on such grounds, the people would expel a person while leaving them the name.

The single exception is proven acts aimed at undermining the integrity of the voting itself: collusion, buying or selling a vote, coercing others, circumventing the rule of "one person, one passport" (Charter, Article 22 bis). Views, how a person voted, and disagreement with decisions are not a ground on any construction whatever.

### Digital identification

- publicly verifiable confirmation of participant status;
- access to the services of the ecosystem;
- the possibility of use in decentralized applications supporting this standard.

### Access to the ecosystem

- the people's digital platform;
- participation in Cells and joint projects;
- educational resources;
- interaction with other participants.

### Marks of participation

The history of participation and contribution is recorded publicly: votes, completed projects, work in Cells.

> **These marks affect nothing** and are purely informational: [Charter, Article 8](https://earth-lings.org/documents/en/en05-charter.html).

---

## How to obtain it

**1. Signing the Declaration.** Reading the documents, understanding the principles, confirming agreement with a digital signature. It is this act that creates belonging.

**2. Identity verification.** Confirmation that you are a living human being and that there is only one of you. It secures the principle of "one person, one vote". Original images and scans of documents are not retained.

**3. Making the contribution.** The equivalent of 79 USD, in cryptocurrency (ETH, USDT, USDC). It covers the cost of identity verification and passport issuance, goes into the common treasury, and is allocated in published shares.

> A person who cannot make the contribution themselves joins an open queue, and the contribution for them is made by another person or by the Treasury. The passport is in no way different from any other: the registry does not record by whom the contribution was made. The contribution does not buy belonging: belonging arises by signing the Declaration.

**4. Issuance of the passport.** The token is created automatically and tied to your wallet.

---

## Technical basis

### Infrastructure

- network: Polygon Mainnet, EVM-compatible;
- standard: ERC-721, non-transferable (soulbound);
- passport contract address: `0x20e7962878429B803E35F83ba34eD291afEC2Be4`;
- transactions are public and verifiable in a network explorer without our involvement;
- the contract source code is open (MIT licence).

### Contract security

- basis: the audited OpenZeppelin libraries;
- rule: one passport per wallet; transfer is blocked in the contract itself;
- an independent audit is planned before operations are expanded.

### Data storage

- **in the ledger:** an identifier, a pseudonym, a verification hash. Personal data are not written to the ledger;
- **outside the ledger:** the personal data of the account, encrypted and kept to a minimum;
- **biometrics:** not retained. Only irreversible cryptographic hashes are retained, and only so that one person cannot hold two valid passports;
- designed in accordance with the principles of the GDPR.

### Cryptography

- signatures: ECDSA secp256k1;
- hashing: Keccak-256.

A single passport standard for all participants makes it possible to concentrate resources on the reliability of one system and gives everyone equal protection.

---

## Legal significance

The passport is a digital certificate of belonging to the Earthlings people.

### What the passport does not give

This is important to understand before entering, not after.

- **it gives no citizenship or residence** of any country;
- **it provides no visa privileges** and no rights of entry;
- **it has no legal force** in the state institutions of any country;
- **it does not replace identity documents**;
- **it does not exempt anyone** from complying with the laws of their country of residence;
- **it creates no rights in international law.**

The passport documents what it documents, and that is no small thing: a particular person has been confirmed as living and unique, and has signed the Declaration. Inside the people everything follows from this - an equal vote, participation in decisions, inalienable belonging. What this combination means for international law is the subject of separate examination in the documents [Legal Basis](https://earth-lings.org/documents/en/en04-legal-basis.html) and [Objections and Answers](https://earth-lings.org/documents/en/en26-objections-and-answers.html), where the arguments against are also set out.

### Data protection

- a right to correction and deletion of the data processed by the platform;
- entries in a distributed ledger are by technical definition not deletable - and that is precisely why there are no personal data in them: they hold pseudonymous addresses and marks of actions;
- minimization of processing; encryption of personal data;
- photographs and scans are not retained.

### Liability and disputes

- the Earthlings DAO is not a registered legal entity;
- participants bear individual responsibility for complying with the laws of their countries;
- internal disputes are resolved by the procedures of the Charter: dialogue, mediation, and for serious breaches recourse to the Independent Council. The people does not supplant courts and state legal mechanisms and provides no arbitration outside its own ecosystem.

---

## Termination of the passport

**As a general rule you alone burn your passport**, with your own key, from your own wallet (the `burnByHolder` function). The platform does not store your keys and can neither perform the burning for you nor prevent it.

The Charter (Article 21) establishes **two and only two** exceptions, and this list cannot be extended.

> **On the death of the holder.** Belonging ends as a consequence of a person's death, but the passport is not burned. The people has no access to death records worldwide, so such a ground would rest on unverifiable information and would become the cheapest way to remove a participant. The passport remains in the registry; participation that no longer exists is handled by the inactivity mechanism (Charter, Article 20). The passport is not inherited and is not transferred under any circumstances.

### 1. Annulment of an invalid issuance

It applies where it is established that a passport was issued in breach of the conditions of issuance: more than one valid passport has been issued to one person, or verification was passed using falsified data or another person's identity.

**This is not a measure of liability and not expulsion from the people.** What is established is only that the issuance never lawfully took place. No automatic reissue follows: if the obstacle to lawful issuance is removed, the person is entitled to undergo verification again on general terms.

**The procedure** is a decision of the Assembly, not an act of the operator:

- a substantiated submission with evidence;
- notice to the holder and **no fewer than 21 days** for objections; the holder is entitled to enlist other participants in their support;
- an opinion of the Independent Council;
- a vote of the Assembly: **75 per cent with a quorum of 25, secret, without delegation**;
- **appeal within 30 days**, and a simple majority suffices to overturn the decision.

The operator's technical powers are limited to executing a decision already taken by the Assembly. The operator cannot annul a passport on its own.

### 2. Technical reissue

At **the holder's own request** on loss of access to a wallet or on migration of the contract. The passport is burned and immediately issued anew to the same or a new address. **Membership is not interrupted**, and no vote is required.

### The principle of inalienability

No one can be deprived of belonging to the people by compulsion. No procedure of expulsion exists.

Where restrictive measures are applied for gross breaches of common rules, the passport is retained, **the right to vote is retained in full**, and the restrictions affect only participation in Cells, the right to submit proposals, and access to particular services - under the procedure of Article 22 of the Charter, with a right of defence, a secret ballot, and appeal.

### What happens technically

- burning is performed by the `burn` function of the smart contract;
- the passport data are deleted from the contract's active registry;
- a pseudonymous mark remains in the unalterable history that the passport existed and was burned: this is a fact of the past, not a continuing membership;
- there are no real personal data in the ledger;
- to re-enter, the full procedure is gone through and a new passport is issued.

---

## On funding

As of today the people develops on participants' funds: no external funding has been raised.

The Charter and the document [Treasury](https://earth-lings.org/documents/en/en09-treasury.html) provide for the possibility of accepting grants and donations from external organizations - with mandatory publication of the source, the absence of conditions contrary to the people's principles, and an express prohibition: a donor receives neither a vote nor influence over decisions. The size of a donation gives nothing.

Participants' contributions cover the cost of identity verification and passport issuance, the development of infrastructure, legal support, and the running of the ecosystem. All decisions on spending are taken by a vote of the DAO Assembly and published.
