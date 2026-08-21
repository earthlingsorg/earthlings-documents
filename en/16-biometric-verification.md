# Earthlings Biometric Verification Policy

**In force from the moment of publication**

> Where this Policy diverges from the [Charter](https://earth-lings.org/documents/en/en05-charter.html), the Charter applies; where the Charter diverges from the [Declaration](https://earth-lings.org/documents/en/en01-declaration.html), the Declaration applies. The general rules on processing personal data are in the [Privacy Policy](https://earth-lings.org/documents/en/en28-privacy-policy.html).

## In brief

- biometrics are processed at the moment of verification and are not retained;
- so that one person cannot hold two valid passports, only irreversible cryptographic hashes are retained;
- you can return at any time after leaving;
- a pseudonym instead of your real name is your choice;
- biometrics serve trust, not control;
- the people's own verification system, separated stores, data minimization.

---

# SECTION 01. Principles

## Why biometrics

They serve one purpose: to confirm that behind every vote stands one living, unique human being. This is the foundation of trust between strangers - and nothing more. The system is designed so that it cannot be used for surveillance.

## The person, not the documents

The human being matters more than documents. Your belonging to the people is determined by your free choice, not by a passport or citizenship. The task of verification is not recognition from outside but the confirmation of a simple fact: you are you, and there is only one of you.

## Four principles

**1. Confirmation of uniqueness, not control.** Verification protects the people from multiple registrations but creates no database for surveillance.

**2. Belonging is confirmed personally.** State documents remain where they are: verification only checks identity and replaces nothing.

**3. Trust through verification.** In a community without a central authority, confirmed uniqueness creates a basic layer of trust. This does not guarantee good faith in any particular dealing, but it removes anonymous multiplicity of accounts as a source of manipulation.

**4. Protection against abuse.** The separation of stores, encryption, and the practical impossibility of reconstructing an image from the data retained are designed so that the system cannot be used for mass surveillance.

---

# SECTION 02. Scope and consent

This Policy governs the processing of biometric data when signing the Declaration, obtaining earthling status, and taking part in the people's infrastructure.

## Legal basis

Biometric data belong to a special category of personal data under Article 9 of the GDPR and are processed **solely on the basis of your explicit consent** (Articles 6(1)(a) and 9(2)(a) of the GDPR).

This is the only basis: neither performance of a contract nor legitimate interest legalizes a special category of data by itself.

## Your consent and its withdrawal

Verification is voluntary. You are entitled to withdraw your consent at any time by writing to privacy@earth-lings.org.

**What happens on withdrawal:**

- the processing of biometric data ceases, and the results of the check and the account data are deleted;
- **the irreversible uniqueness hash is retained, and this is the only limit on withdrawal.** It is computed from the data of the document, not from biometrics, and therefore does not fall under consent within the meaning of Article 9 GDPR and is retained on another basis. Without it one person could obtain a second passport, and no one has that possibility - including that person themselves;
- since confirmed uniqueness is a condition of the right to vote, further participation in votes becomes impossible;
- **you burn the passport yourself**, with your own key, as in an ordinary voluntary exit.

> **We cannot burn your passport for you.** The Charter (Article 21) permits a passport to be burned by someone other than the holder in two cases only - annulment of an invalid issuance by decision of the Assembly, and technical reissue at your own request; against your will a passport may be burned only in the first of them. Withdrawal of consent is not among these cases, and the platform does not store your keys. If you withdraw your consent and do not burn the passport, we will delete the data on our side, but the entry in the registry will remain until you burn it.

---

# SECTION 03. Conditions for obtaining status

- **age** - 18 years or over;
- **consent** - voluntary acceptance of the Declaration;
- **identity verification** - confirmation of uniqueness;
- **the passport** - issuance of a non-transferable token to your address.

## What data are needed

The full list and the legal bases are in the Privacy Policy. Verification requires:

- **a pseudonym** - of your choosing, used in the passport and for logging in to the platform;
- **an email address** - for contact;
- **verification of a document and of the face**.

**Your real first and last names are not retained.** The document data are used only at the moment of verification - to match the face against the document and confirm uniqueness - and are deleted once it is complete. Your pseudonym remains your public name.

## What the status gives

- **a passport** - confirmation of belonging to the people;
- **the right to vote** in the DAO Assembly: one person, one vote;
- **access to the infrastructure** - participation in projects, services, coordination;
- **the right to submit proposals** and to take part in decisions on every question.

> **What the status does not give.** The passport gives no citizenship or residence, no visa rights, no force in state institutions, and does not replace the documents of your country. The Earthlings people does not possess international legal personality and cannot represent anyone's interests in courts or before state authorities. The full list is in the documents [The Earthling Path](https://earth-lings.org/documents/en/en14-the-earthling-path.html) and [SBT passport](https://earth-lings.org/documents/en/en15-sbt-passport.html).

---

# SECTION 04. How verification works

**Document → face → liveness check → matching document and face → result → protected storage of the result**

## What is checked

- **the document** - matching the data against an official identity document;
- **facial geometry** - key points and proportions;
- **liveness** - protection against photographs, video recordings, and masks. The check is built on the presentation attack detection model described in the ISO/IEC 30107 standard; the stated level of resistance and the results of independent testing are published when the system enters production use.

## Procedure

1. **Receiving** the image of the document and of the face over a secure connection.
2. **Liveness check.**
3. **Extraction of features** - the document data and the key points of the face.
4. **Construction of a mathematical template** - a set of numbers describing the characteristics. The template exists only in memory for the duration of the check.
5. **Matching** the biometrics against the document and checking uniqueness.
6. **Storing the result** - in encrypted form.

> **What remains after verification.** Photographs, scans of documents, and biometric templates **are not retained**. What remains: the verification status (passed or not) and irreversible cryptographic hashes computed from the document number and from the pairing of the name with the country.
>
> The hashes do not prevent anyone from returning. They only prevent one person from holding two valid passports at the same time: on re-entry the system finds a match, satisfies itself that the previous passport has been burned, and issues a new one.

> **Precisely on the status of the hashes.** A hash is irreversible: a name or a document number cannot be read out of it. But it does allow **a particular person to be singled out** among others - otherwise it would not do its job. Under the GDPR these are therefore **pseudonymized, not anonymous** data, and the protection of personal data applies to them in full. We do not call them anonymized, because that would be inaccurate.

---

# SECTION 05. Data protection

The general measures are described in the Privacy Policy; below are those specific to biometrics.

**Secure transmission.** All data are transmitted over secure channels with end-to-end encryption between your device and the servers of the verification system.

**Encryption at rest.** The hashes are stored encrypted (AES-256). The decryption keys are stored separately from the data.

**Separation of stores.** The hashes and verification results are stored separately from account data.

**Immediate deletion of source material.** Photographs and scans are deleted immediately after the check is complete.

**Access control.** Multi-level authentication and logging: every access to verification data is recorded and can be audited.

> **The security philosophy:** the best protection is when there is nothing to steal. We do not store what could be used against you.

---

# SECTION 06. Your rights

The general rights of a participant are in the Privacy Policy and the Terms of Use. Below are those specific to biometrics.

**Withdraw consent** - at any time; the procedure and consequences are described in section 02.

**Undergo verification again.** If your appearance has changed significantly and verification does not recognize you, you go through it again. The template is not "updated" in the process: it is stored nowhere, and the matching is performed from scratch every time.

**Demand review by a human being.** An automated refusal is not final (Article 22 of the GDPR). You are entitled to state your position and to contest the result. After two unsuccessful automated attempts the case passes to a human being **without a separate request**. The number of repeat applications is not limited.

**Lodge a complaint** with the data protection supervisory authority of your country; the procedure is in the Privacy Policy.

## What happens when you leave

- the link between the verification data and your identity is broken;
- pseudonymized hashes are retained solely so that one person cannot hold two valid passports;
- **the right to return is retained**: on re-entry the system satisfies itself that the previous passport has been burned and issues a new one;
- reconstructing an image or establishing an identity from the hashes is practically impossible.

---

# SECTION 07. What verification is used for

The list is exhaustive: no processing for other purposes takes place.

- confirming uniqueness on registration;
- issuing the passport;
- confirming participant status;
- securing the principle of "one person, one vote" in votes;
- access to services requiring confirmed status.

> **What we do not do.** We do not track location. We do not analyse behaviour. We do not sell data to third parties. We do not build profiles for advertising. We do not use the system for observation. We do not transfer data to state authorities other than under a court decision in force or an equivalent lawful requirement, whose legitimacy is checked in every case.
>
> A participant is notified of requirements that have been complied with, unless the decision itself prohibits it. A summary of such cases is published in the transparency report.

---

# SECTION 08. Transparency and oversight

## What is open and what is closed

The code of the passport smart contract is open under the MIT licence and verifiable in a network explorer.

**The code of the identity verification system is closed** - precisely because it works with personal data and publishing it would make it easier to circumvent the protections. This is a deliberate choice, not a silence; the list with the reasons is in the document [Where We Are Now](https://earth-lings.org/documents/en/en32-where-we-are-now.html).

In exchange for keeping it closed we take on the following:

- **an independent security audit** is planned before operations are expanded; the report is published;
- **technical documentation** is available for study;
- **security reports** are published regularly;
- **access logging** for verification data is maintained and subject to audit.

## Independent oversight

Questions of ethics in the processing of biometric data are put to the [Independent Council](https://earth-lings.org/documents/en/en11-independent-council.html) - a body not subordinate to those who operate the platform. Until the Council is formed, such questions are considered by the DAO Assembly, and the periods of public discussion are doubled (Charter, Article 39).

Proposals to amend this Policy are put to a vote of the Assembly.

---

# SECTION 09. Division of responsibility

## The identity verification system

- receiving and processing the data of the document and of the face;
- recognizing the document and extracting the data from the machine-readable zone;
- the liveness check;
- matching the photograph against the document;
- confirming uniqueness.

## The people's registry

**What is not stored:** real first and last names; passport and document numbers; exact dates of birth; residential addresses; photographs and biometric templates; telephone numbers, except for two-factor authentication.

**What is stored:** the pseudonym; the email address; confirmation of being 18+; the country of residence (for statistics); the identity verification status; the link to the passport; the date the status was obtained.

## Minimization

The registry follows the principle of data minimization in accordance with the GDPR. Only what is necessary is stored: confirmed uniqueness, the link to the passport for taking part in decisions, and an internal identifier for distributing rewards.

Photographs and scans are deleted immediately after verification, but its result remains valid and verifiable - much as a state does not permanently store biometric samples when issuing a passport, although the fact of issuance remains valid.

> **The link between the real person and the pseudonym is not retained.** The document data are processed only at the moment of verification. What remains in the registry are the pseudonym, the verification status, and cryptographic confirmation of uniqueness. This architecture rules out disclosure of a participant's identity - to other participants, to administrators, and to third parties - because there is nothing to disclose.

---

# SECTION 10. Frequently asked questions

**Can you reconstruct my face from what you store?**
No. The biometric template is not retained at all: the comparison is performed at the moment of verification, after which the source data are deleted. What remains are irreversible hashes from which neither an image nor document data can be obtained.

**What happens if I lose my phone?**
The verification data are safe. To restore access it is enough to install the application on a new device and undergo verification again.

**Can my biometrics be stolen?**
Only encrypted irreversible hashes can be stolen, and they are useless without the decryption keys. Reconstructing a facial image from them is practically impossible.

**Do I have to give my real name?**
No. Your real first and last names are not retained. The document data are checked only at the moment of verification and are deleted afterwards. In everyday interaction you are known by your pseudonym.

**What happens to the data when I leave?**
The link between the verification data and your identity is broken. Pseudonymized hashes are retained solely so that one person cannot hold two valid passports. This does not prevent you from returning.

**What if my appearance has changed significantly?**
Undergo verification again. There is no stored template that would need updating.

**What if verification is refused?**
You will receive notice of the reasons. You can try again once they are addressed - for example, with better-quality images or a different document. If you disagree, you are entitled to demand review by a human being, and after two unsuccessful automated attempts such review happens automatically.

**Who has access to my real first and last names?**
No one: they are not stored. The people is technically unable to disclose data it does not hold.

**Do you pass data to states?**
Only under a court decision in force or an equivalent lawful requirement - the procedure and the notice given to the participant are described in the [Privacy Policy](https://earth-lings.org/documents/en/en28-privacy-policy.html).

---

# SECTION 11. Amendments to this Policy

The Policy is updated as technology and legislation develop. Amendments are published with the date of entry into force.

The procedure for amendment - notice by email no fewer than 30 days in advance, notice on the platform at the next login, publication of the list of changes, and the right to object - is laid down by the Privacy Policy.

---

**For questions about identity verification:** privacy@earth-lings.org
