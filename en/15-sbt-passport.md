# The earthling SBT passport

**A digital certificate of belonging to the Earthlings people**

> This document describes the design and legal significance of the passport. Where they diverge, the [Charter](https://earth-lings.org/documents/en/en05-charter.html) prevails; where the Charter diverges from the [Declaration](https://earth-lings.org/documents/en/en01-declaration.html), the Declaration prevails. The procedure for entering is described in the document [The Earthling Path](https://earth-lings.org/documents/en/en14-the-earthling-path.html). During the founding period - from 22 October 2026 until the Declaration is adopted - signing the Declaration and entering the people are suspended: a people defined by an adopted text does not yet exist. During this period identity verification is carried out free of charge, and on its completion a temporary document of a participant in the founding is issued, rather than a passport (the document "The Founding Period", Part 2, section 5). The temporary document is issued in the same contract as the passport (the document "Where We Are Now"), but it does not document the signing of the Declaration. What follows describes the main regime, which will begin after the Declaration is adopted.

---

## What it is

The earthling SBT passport is a non-transferable digital token (a Soulbound Token) issued to every participant after they confirm their identity, sign the Declaration, and make the contribution. It cryptographically confirms belonging to the people and is held in a distributed ledger as a unique record that cannot be altered without detection.

Unlike state passports, which are tied to a territory and confirm citizenship, this passport confirms belonging to a people united by shared values. It cannot be transferred to another person, sold, or alienated.

**Non-transferability.** The passport is tied to your wallet, and transfer is blocked in the contract itself, not by a rule that can be worked around. Your uniqueness is confirmed at issuance.

**Cryptographic protection.** The record is held on a distributed network, and it cannot be altered without detection.

**Equality.** Everyone receives the same passport with the same rights. There are no privileged classes and no tiers of belonging. One person, one passport, one vote; the vote arises by signing the Declaration, and the passport confirms it.

---

## What the passport gives you

### Participation in governance

- confirmation of the right to vote in the DAO Assembly;
- the submission of proposals and initiatives;
- participation in decisions on every matter.

> **The vote is inalienable** and cannot be taken away or suspended for a person's views, for how they voted, for disagreement with decisions, or as a general measure of liability (Declaration, Article 4; [Charter, Articles 17 and 37](https://earth-lings.org/documents/en/en05-charter.html)). The vote is the substance of belonging: by taking it away on such grounds, the people would expel a person while leaving them the name.

The single exception is proven acts aimed at undermining the integrity of the voting itself: collusion, buying or selling a vote, coercing others, circumventing the rule of "one person, one passport" (Charter, Article 22 bis). Views, how a person voted, and disagreement with decisions are not a ground on any construction whatever.

### Digital identification

- publicly verifiable confirmation of participant status;
- access to the services of the ecosystem;
- the possibility of using the passport in decentralized applications that support this standard.

### Access to the ecosystem

- the people's digital platform;
- participation in Cells and joint projects;
- educational resources;
- interaction with other participants.

### Marks of participation

The history of a person's participation and of the work they have contributed is visible to participants on the platform: completed projects, work in Cells. Whether a particular person took part in a vote is not published: a personal vote is secret (Charter, Article 6).

> **These marks affect nothing** and are purely informational: [Charter, Article 8](https://earth-lings.org/documents/en/en05-charter.html).

---

## How to obtain it

**1. Identity verification.** Confirmation that you are a living human being and that there is only one of you. It secures the principle of "one person, one vote". Original images and scans of documents are not retained.

**2. Signing the Declaration.** Reading the documents, understanding the principles, confirming agreement with a digital signature. It is this act that creates belonging.

**3. Making the contribution.** The equivalent of 79 USD, in cryptocurrency (ETH, USDT, USDC). The purpose of the contribution and the procedure for spending it are set out in the document [Treasury](https://earth-lings.org/documents/en/en09-treasury.html).

> A person who cannot make the contribution themselves will be able, once entry requires payment, to join an open queue, and the contribution for them could then be made by another person or by the Treasury; there is no guarantee that it will be. The passport is in no way different from any other: the registry does not record by whom the contribution was made. The contribution does not buy belonging: belonging arises by signing the Declaration.

**4. Issuance of the passport.** The token is created automatically and tied to your wallet.

---

## Technical basis

### Infrastructure

- network: Polygon Mainnet, EVM-compatible;
- standard: ERC-721, non-transferable (soulbound);
- passport contract address: `0x20e7962878429B803E35F83ba34eD291afEC2Be4`;
- transactions are public and verifiable on a block explorer without our involvement;
- the contract source code is open (MIT licence).

### Contract security

- basis: the proven OpenZeppelin libraries;
- rule: one passport per wallet; transfer is blocked in the contract itself;
- an independent audit is planned before operations are expanded.

### Data storage

- **in the ledger:** the wallet address, the passport record number, the participant identifier through which the entry is linked to the data of the identity-verification system, and the time of issue; on issue, the pseudonym field is filled with the single word "Earthling", and the verification hash field with a random value unrelated to the verification data. Names, document data, biometrics, and verification hashes are not written to the ledger;
- **outside the ledger:** the personal data of the account, kept to a minimum;
- **biometrics:** not retained. Verification leaves behind the verification status, the document type and issuing country, the numeric verification scores, the reasons for rejection, and irreversible hashes of the document number and of the first name, last name, and date of birth from the document, computed with the server's secret key. The hashes are computed from the document data, not from biometrics, and are retained only so that one person cannot hold two valid passports;
- data storage is being designed in accordance with the principles of the GDPR.

### Cryptography

- signatures: ECDSA secp256k1;
- hashing: Keccak-256.

A single passport standard for all participants makes it possible to concentrate resources on the reliability of one system and gives everyone equal protection.

---

## Legal significance

The passport is a digital certificate of belonging to the Earthlings people.

### What the passport does not give you

This is important to understand before entering, not after.

- **it gives no citizenship or residence** in any country;
- **it provides no visa privileges** and no rights of entry;
- **it has no legal force** in the state institutions of any country;
- **it does not replace identity documents**;
- **it does not exempt anyone** from complying with the laws of their country of residence;
- **it creates no rights under international law.**

The passport documents what it documents, and that is no small thing: a particular person has been confirmed as living and unique, and has signed the Declaration. Inside the people, everything follows from this - an equal vote, participation in decisions, inalienable belonging. What this combination means for international law is examined separately in the documents [Legal Basis](https://earth-lings.org/documents/en/en04-legal-basis.html) and [Objections and Answers](https://earth-lings.org/documents/en/en26-objections-and-answers.html), which also set out the arguments against.

### Data protection

- a right to correction and deletion of the data processed by the platform;
- entries in a distributed ledger are by technical definition not deletable - and that is precisely why names, document data, biometrics, and verification hashes are not written to them on issue. On issue, the ledger records the wallet address, the passport record number, the participant identifier through which the entry is linked to the data of the identity-verification system, and the time of issue; issuing and burning leave marks in the ledger. These are pseudonymous data that we link to your account;
- minimization of processing; encryption in transit;
- photographs and scans are not retained.

### Liability and disputes

- the Earthlings DAO is not a registered legal entity;
- participants bear individual responsibility for complying with the laws of their countries;
- internal disputes are resolved under the procedure set out in the document "Earthlings Ethics": direct dialogue, mediation with the consent of both parties, and, if mediation has not helped or the other party has not consented to it, consideration by the Assembly; in the case of a threat to life and safety, a manifest breach of the Declaration or a crime, a person turns for help at once, bypassing dialogue and mediation. The people does not supplant courts and state legal mechanisms and provides no arbitration outside its own ecosystem.

---

## Termination of the passport

**As a general rule you alone burn your passport**, with your own key, from your own wallet (the `burnByHolder` function). The platform does not store your keys and cannot prevent the burning; no one is entitled to burn the passport for you, but until the contract owner's rights are transferred to a multisignature, issuing and burning a passport are technically available to a single key (the document "Where We Are Now").

The Charter (Article 21) establishes **two and only two** exceptions, and this list cannot be extended.

> **On the death of the holder.** Belonging ends on a person's death, but the passport is not burned. The people has no access to death records worldwide, so such a ground would rest on unverifiable information and would become the cheapest way to remove a participant. The passport remains in the registry; participation that no longer exists is handled by the inactivity mechanism (Charter, Article 20). The passport is not inherited and is not transferred under any circumstances.

### 1. Annulment of an invalid issuance

It applies where it is established that a passport was issued in breach of the conditions of issuance: more than one valid passport has been issued to one person, or verification was passed using falsified data or another person's identity, or the passport was issued to a person below the age set by the Charter.

**This is not a measure of liability and not expulsion from the people.** What is established is only that the issuance never lawfully took place. No automatic reissue follows: if the obstacle to lawful issuance is removed, a person is entitled to undergo verification again on general terms.

**The procedure** is a decision of the Assembly, not an act of the operator:

- a substantiated submission with evidence;
- notice to the holder and **no fewer than 21 days** for objections; the holder is entitled to enlist other participants in their support;
- an opinion of the Independent Council;
- a vote of the Assembly: **75 per cent with a quorum of 25, secret, without delegation**;
- **appeal within 30 days**, and a simple majority suffices to overturn the decision.

The operator's powers are limited to executing a decision already taken by the Assembly. The operator is not entitled to annul the issuance of a passport on its own.

### 2. Technical reissue

At **the holder's own request** on loss of access to a wallet or on migration of the contract. The passport is burned and immediately issued anew to the same or a new address. **Belonging is not interrupted**, and no vote is required.

### The principle of inalienability

No one can be compulsorily deprived of belonging to the people. No procedure of expulsion exists.

Where measures are applied for gross breaches of common rules, the passport is retained and **the right to vote is retained in full**. There is one measure addressed to a person - a warning, and it takes nothing away: neither the vote, nor the right to submit proposals, nor the right to create Cells and to join them, nor access to services, nothing at all. The other measures are addressed to a project or a Cell and do not concern the rights of a person - under the procedure of Article 22 of the Charter, with a right of defence, a secret ballot, and appeal.

### What happens technically

- on exit, the holder burns the passport with the `burnByHolder` function, while on annulment and technical reissue the burning is performed by the contract owner with the `burn` function;
- the passport data are deleted from the contract's active registry;
- a pseudonymous mark that the passport existed and was burned remains in the unalterable history: this is a fact of the past, not a continuing belonging;
- names, document data, biometrics, and verification hashes are not written to the ledger on issue;
- to re-enter, a person goes through the full procedure and is issued a new passport.

---

## On funding

Up to now the project has been funded from the personal funds of the author of the Declaration (the document "About Us"): no external funding has been raised.

The Charter and the document [Treasury](https://earth-lings.org/documents/en/en09-treasury.html) provide for the possibility of accepting grants and donations from external organizations - with publication of the source (or, if the donor has chosen to remain anonymous, of the fact of receipt and the amount), the absence of conditions contrary to the people's principles, and an express prohibition: a donor receives neither a vote nor influence over decisions. The size of a donation gives nothing.

After the Declaration is adopted, decisions on spending are taken by a vote of the DAO Assembly and published, and while there is no multisignature on the treasury wallet, its only key is with the author of the Declaration (the document "Treasury"); the categories of expenditure and their shares are set out in Article 9 of the document [Treasury](https://earth-lings.org/documents/en/en09-treasury.html).
