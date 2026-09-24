# Earthlings Biometric Verification Policy

**In force from the moment of publication**

> Where this Policy diverges from the [Charter](https://earth-lings.org/documents/en/en05-charter.html), the Charter prevails; where the Charter diverges from the [Declaration](https://earth-lings.org/documents/en/en01-declaration.html), the Declaration prevails. The general rules on processing personal data are in the [Privacy Policy](https://earth-lings.org/documents/en/en28-privacy-policy.html). During the founding period - from 22 October 2026 until the Declaration is adopted - signing the Declaration and entering the people are suspended: a people defined by an adopted text does not yet exist. During this period identity verification is carried out free of charge, and on its completion a temporary document of a participant in the founding is issued, rather than a passport (the document "The Founding Period", Part 2, section 5). The temporary document is issued in the same contract as the passport (the document "Where We Are Now"). This Policy also applies to such verification; what it says about signing and the passport refers to the main regime after the Declaration is adopted.

## In brief

- biometrics are processed at the moment of verification and are not retained;
- irreversible cryptographic hashes are retained, so that one person cannot hold two valid passports;
- you can return at any time after leaving;
- your first and last names as they appear in the document are needed to check against it; other participants see you under the pseudonym you choose;
- biometrics serve trust, not control;
- an in-house verification system, data minimization.

---

# SECTION 01. Principles

## Why biometrics

They serve one purpose: to confirm that behind every vote stands one living, unique human being. This is the foundation of trust between strangers - and nothing more. The system is designed to store as little as possible.

## The individual, not the documents

The human being matters more than documents. Whether you belong to the people is determined by your free choice, not by a passport or citizenship. The task of verification is not recognition from outside but the confirmation of a simple fact: you are you, and there is only one of you.

## Four principles

**1. Confirmation of uniqueness, not control.** Verification protects the people from multiple registrations and is not used for surveillance.

**2. Belonging is confirmed personally.** State documents keep their place: verification only checks identity and replaces nothing.

**3. Trust through verification.** In a community without a central authority, confirmed uniqueness creates a basic layer of trust. This does not guarantee good faith in any particular dealing, but it removes anonymous multi-accounting as a source of manipulation.

**4. Protection against abuse.** Not storing images or templates, hashes computed with the server's secret key, and the practical impossibility of reconstructing an image from the data retained are designed so that the system cannot be used for mass surveillance.

---

# SECTION 02. Scope and consent

This Policy governs the processing of biometric data when you sign the Declaration, obtain earthling status, and take part in the people's infrastructure, and, during the founding period, when your identity is verified for a temporary document of a participant in the founding.

## Legal basis

Biometric data belong to a special category of personal data under Article 9 of the GDPR and are processed **solely on the basis of your explicit consent** (Articles 6(1)(a) and 9(2)(a) of the GDPR).

This is the only basis: neither performance of a contract nor legitimate interest legalizes a special category of data by itself.

## Your consent and its withdrawal

Verification is voluntary. You are entitled to withdraw your consent at any time by writing to privacy@earth-lings.org.

**What happens on withdrawal:**

- the processing of biometric data ceases (after verification they are not stored in any case); the result of the check (section 04) is retained: it is not biometric data;
- **the irreversible uniqueness hash is also retained.** It is computed from the data of the document, not from biometrics, and therefore does not fall under consent within the meaning of Article 9 GDPR and is retained on another basis. Without it one person could obtain a second passport on the same document data: the hash makes it possible to detect such an attempt, including one made by that person themselves, and a passport issued by circumventing verification is annulled (Declaration, Article 8);
- withdrawal of consent does not affect belonging or the right to vote, and the account is not deleted because of it; for a person who belongs to the people, the account is deleted only upon exit;
- **you burn the passport yourself**, with your own key, if you decide to leave: withdrawal of consent does not burn the passport.

> **We are not entitled to burn your passport for you.** The Charter (Article 21) permits a passport to be burned by someone other than the holder in two cases only - annulment of an invalid issuance by decision of the Assembly, and technical reissue at your own request; against your will a passport may be burned only in the first of them. Withdrawal of consent is not among these cases, and the platform does not store your keys; but until the contract owner's rights are transferred to a multisignature, issuing and burning a passport are technically available to a single key (the document "Where We Are Now"). The entry in the registry remains after consent is withdrawn. Until the Declaration is adopted, there is no Assembly (Charter, Article 38), and against the holder's will, the temporary document of a participant in the founding is burned under the procedure set out in the document "The Founding Period" (Part 2, section 5).

---

# SECTION 03. Conditions for obtaining status

- **age** - 18 years or over;
- **consent** - voluntary signing of the Declaration;
- **identity verification** - confirmation of uniqueness;
- **the passport** - issuance of a non-transferable token to your wallet address; the passport confirms the status that arises by signing the Declaration.

## What data are needed

The full list and the legal bases are in the Privacy Policy. Verification requires:

- **a pseudonym** - of your choosing, used in the passport and for logging in to the platform;
- **an email address** - for contact;
- **verification of a document and of your face** - together with your first and last names in Latin script as they appear in the document; in addition, you give your country of residence and confirm that you are aged 18 or over.

**Your real first and last names are not retained.** The document data are used only at the moment of verification, to match the face against the document and confirm uniqueness; once it is complete, nothing remains of them but the document type, the issuing country, and irreversible hashes. Your pseudonym remains the name under which other participants see you.

## What the status gives you

- **a passport** - confirmation of belonging to the people;
- **the right to vote** in the DAO Assembly: one person, one vote;
- **access to the infrastructure** - participation in projects, services, coordination;
- **the right to submit proposals** and to take part in decisions on every matter.

> **What the status does not give you.** The passport gives no citizenship or residence, no visa rights, no force in state institutions, and does not replace the documents of your country. The Earthlings people does not possess international legal personality and cannot represent anyone's interests in courts or before state authorities. The full list is in the documents [The Earthling Path](https://earth-lings.org/documents/en/en14-the-earthling-path.html) and [SBT passport](https://earth-lings.org/documents/en/en15-sbt-passport.html).

---

# SECTION 04. How verification works

**Document → face → liveness check → matching document and face → result → storage of the result**

## What is checked

- **the document** - matching the data against an official identity document;
- **facial geometry** - key points and proportions;
- **liveness** - at present this is a basic passive check on a single image of the face: it is designed for simple fakes - a shot of a photograph or of a screen - and does not protect against video recordings or masks, while the image itself can be uploaded as a file. A check built on the presentation attack detection model described in the ISO/IEC 30107 standard has not yet been introduced; the stated level of resistance and the results of independent testing will be published when it is introduced.

## Procedure

1. **Receiving** the image of the document and of the face over a secure connection.
2. **Liveness check.**
3. **Extraction of features** - the document data and the key points of the face.
4. **Construction of a mathematical template** - a set of numbers describing the characteristics. The template exists only in memory for the duration of the check.
5. **Matching** the biometrics against the document and checking uniqueness.
6. **Storing the result** - without images or templates.

> **What remains after verification.** Photographs, scans of documents, and biometric templates **are not retained**. What remains: the verification status, the document type and issuing country, the numeric verification scores, the reasons for rejection, and irreversible hashes computed with the server's secret key - a hash of the document number and a single combined hash of the first name, last name, and date of birth from the document; the document number, first name, last name, and date of birth themselves are not retained.
>
> The hashes do not prevent anyone from returning. They only prevent one person from holding two valid passports at the same time: on re-entry the system finds a match, satisfies itself that the previous passport has been burned, and issues a new one.

> **Precisely on the status of the hashes.** A hash is irreversible and is computed with the server's secret key: a name or a document number cannot be read out of it, and without the key they cannot be guessed by brute force either. But it does allow **a particular person to be singled out** among others - otherwise it would not do its job. Under the GDPR these are therefore **pseudonymized, not anonymous** data, and the protection of personal data applies to them in full. We do not call them anonymized, because that would be inaccurate.

---

# SECTION 05. Data protection

The general measures are described in the Privacy Policy; below are those specific to biometrics.

**Secure transmission.** All data are transmitted over secure channels with end-to-end encryption between your device and the servers of the verification system.

**The hash key.** The hashes are computed with the server's secret key (HMAC-SHA256); the key is stored outside the database. There is no application-level encryption of stored data.

**A single data store.** The hashes and verification results are stored in the same database as account data; platform data are in a separate database.

**Immediate deletion of source material.** Photographs and scans are deleted immediately after the check is complete.

**Access control.** Only administrators have access to verification data, using an administrator key; there is no multi-level authentication yet, and not every access is logged.

> **The security philosophy:** the less that is stored, the less there is to steal. We do not store images, biometric templates, your name, or the document number; what is stored is listed in section 09 and in the Privacy Policy.

---

# SECTION 06. Your rights

The general rights of a participant are in the Privacy Policy and the Terms of Use. Below are those specific to biometrics.

**Withdraw consent** - at any time; the procedure and consequences are described in section 02.

**Undergo verification again.** If your appearance has changed significantly and verification does not recognize you, you go through it again. The template is not "updated" in the process: it is stored nowhere, and the matching is performed from scratch every time.

**Demand review by a human being.** An automated refusal is not final (Article 22 of the GDPR). You are entitled to state your position and to contest the result. After two unsuccessful automated attempts review by a human being is carried out **without a separate request**. The number of repeat applications is not limited.

**Lodge a complaint** with the data protection supervisory authority of your country; the procedure is in the Privacy Policy.

## What happens when you leave

- burning the passport does not by itself delete data: account data are deleted at your request, and after deletion the wallet address, the passport record number, the pseudonym, the country, the verification result and scores, and the irreversible hashes remain;
- pseudonymized hashes are retained solely so that one person cannot hold two valid passports;
- **the right to return is retained**: on re-entry the system satisfies itself that the previous passport has been burned and issues a new one;
- an image cannot be reconstructed from the hashes; a name or a document number cannot be read out of them, and without the server's secret key they cannot be guessed by brute force either.

---

# SECTION 07. What verification is used for

The list is exhaustive: no processing for other purposes takes place.

- confirming uniqueness on registration;
- issuing the passport, and during the founding period a temporary document of a participant in the founding;
- confirming participant status;
- securing the principle of "one person, one vote" in voting;
- access to services requiring confirmed status.

> **What we do not do.** We do not track location. We do not analyse behaviour, except for aggregate statistics on visits, which also count the steps of the identity verification form (Privacy Policy, section 04). We do not sell data to third parties. We do not build profiles for advertising. We do not use the system for surveillance. We do not disclose data to state authorities other than under a court decision in force or an equivalent lawful requirement, whose legitimacy is checked in every case.
>
> A participant is notified of requirements that have been complied with, unless the decision itself prohibits it. A summary of such cases is published in the transparency report.

---

# SECTION 08. Transparency and oversight

## What is open and what is closed

The code of the passport smart contract is open under the MIT licence; the contract is not verified on a block explorer, and anyone who wants to confirm that the source matches the deployed contract has to check it themselves (the document "Where We Are Now").

**The code of the identity verification system is closed** - precisely because it works with personal data and publishing it would make it easier to circumvent the protections. This is a deliberate choice, not an omission; the list with the reasons is in the document [Where We Are Now](https://earth-lings.org/documents/en/en32-where-we-are-now.html).

In exchange for keeping it closed we take on the following:

- **an independent security audit** is planned before operations are expanded; the report will be published;
- **technical documentation** is available for study;
- **security reports** are published regularly;
- **access logging** for verification data is subject to audit; at present not every access is logged.

## Independent oversight

Questions of ethics in the processing of biometric data are put to the [Independent Council](https://earth-lings.org/documents/en/en11-independent-council.html) - a body not subordinate to those who operate the platform. After the Declaration is adopted, while the Council has not been formed, this stage is skipped, and the periods of public discussion of such questions are doubled (Charter, Article 39); until the Declaration is adopted, there is no Council (Charter, Article 38).

After the Declaration is adopted, proposals to amend this Policy are put to a vote of the Assembly; until then, the decision on them is taken by the author of the Declaration under the procedure set out in the document "The Founding Period" (Part 2, section 2).

---

# SECTION 09. Division of responsibility

## The identity verification system

- receiving and processing the data of the document and of the face;
- recognizing the document and extracting the data from the machine-readable zone;
- the liveness check;
- matching the photograph against the document;
- confirming uniqueness.

## The people's registry

**What is not stored:** real first and last names; passport and document numbers; exact dates of birth; residential addresses; photographs and biometric templates; telephone numbers, except those used for two-factor authentication.

**What is stored:** the pseudonym; the email address; confirmation of being aged 18 or over; the country of residence (for statistics); the identity verification status; the link to the passport; the date the status was obtained; the wallet address; the IP address and browser type at the time of verification - for no longer than 12 months.

## Minimization

The registry follows the principle of data minimization in accordance with the GDPR. Only what is necessary for confirming uniqueness and for the link to the passport for taking part in decisions is stored; what exactly is stored is set out above, in the box below, and in the Privacy Policy.

Photographs and scans are deleted immediately after verification, but its result remains valid and verifiable.

> **Real first and last names are not stored.** The document data are processed only at the moment of verification. What remains in the identity verification system are the pseudonym, the email address, the country, the wallet address, and the IP address and browser type at the time of verification, and, from verification, the verification status, the document type and issuing country, the numeric verification scores, the reasons for rejection, and irreversible hashes computed with the server's secret key - a hash of the document number and a single combined hash of the first name, last name, and date of birth from the document; the document number, first name, last name, and date of birth themselves are not retained; the pseudonym is not written to the open registry. Therefore your name or document number cannot be disclosed to other participants, to administrators, or to third parties: we do not have them.

---

# SECTION 10. Frequently asked questions

**Can you reconstruct my face from what you store?**
No. The biometric template is not retained at all: the comparison is performed at the moment of verification, after which the source data are deleted. What remains are the verification result and irreversible hashes from which no image can be obtained; a name or a document number cannot be read out of them, and without the server's secret key they cannot be guessed by brute force either.

**What happens if I lose my phone?**
The verification data are safe. There is no application: verification takes place in the browser. If your wallet was created by logging in with email, Google, or Apple, you only need to log in the same way on the new device. If access to the wallet is lost, the passport is reissued to a new wallet address at your request, and belonging is not interrupted (Charter, Article 21).

**Can my biometrics be stolen?**
Biometrics cannot be stolen: we do not store them. The hashes we store are computed with the server's secret key from the document data, not from biometrics, and they contain no facial image.

**Do I have to give my real name?**
For verification, yes: your first and last names as they appear in the document are needed to check against it. Your real first and last names are not retained. The document data are checked only at the moment of verification; afterwards nothing remains of them but the document type, the issuing country, and irreversible hashes. In everyday interaction you are known by your pseudonym.

**What happens to the data when I leave?**
Burning the passport does not by itself delete data: account data are deleted at your request, and after deletion the wallet address, the passport record number, the pseudonym, the country, the verification result and scores, and the irreversible hashes remain. Pseudonymized hashes are retained solely so that one person cannot hold two valid passports. This does not prevent you from returning.

**What if my appearance has changed significantly?**
Undergo verification again. There is no stored template that would need updating.

**What if my verification is rejected?**
The reasons for an automated rejection are shown on the verification screen, for now as service codes, and the decision following review by a human being is sent by email. You can try again once the reasons are addressed - for example, with better-quality images or a different document. If you disagree, you are entitled to demand review by a human being, and after two unsuccessful automated attempts review by a human being is carried out without a separate request.

**Who has access to my real first and last names?**
No one: they are not stored. The people is technically unable to disclose data it does not hold.

**Do you hand over data to states?**
Only under a court decision in force or an equivalent lawful requirement - the procedure and the notice given to the participant are described in the [Privacy Policy](https://earth-lings.org/documents/en/en28-privacy-policy.html).

---

# SECTION 11. Amendments to this Policy

The Policy is updated as technology and legislation develop. Amendments are published with the date of entry into force.

The procedure for amendment - notice by email no fewer than 30 days in advance, notice on the platform at the next login, publication of the list of changes, and the right to object - is set out in the Privacy Policy.

---

**For questions about identity verification:** privacy@earth-lings.org
