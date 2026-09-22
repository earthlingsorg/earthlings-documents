# Where We Are Now

*The Earthlings people. As of 19 September 2026*

## What this document is for

We claim that Earthlings is verifiable. Such a claim makes sense only when it is possible to say exactly what is being verified and by what means. Instead of the general statement "our code is open", we therefore publish the precise boundary: what is open, what is closed, and for what reason.

The founding period lasts from 22 October 2026 until the day the Declaration is adopted: during that time the people is still being founded, and some of the numbers below mean something different from what they will mean afterwards. The rules of that period are set out in the document [The Founding Period](https://earth-lings.org/documents/en/en20-the-founding-period.html) - we do not repeat them here.

> **The principle.** What is open is what the verifiability of the people depends on: the rules of the passport, the registry of entries, the public voting channel, and the treasury; where we have to be trusted today is named below. What is closed is what, if published, would add nothing to verifiability but would put participants at risk: the server layer and the processing of personal data.

## What is open

| Component | Where | Licence |
|---|---|---|
| The passport smart contract EarthlingPassportV2 | [github.com/earthlingsorg/earthlings-contracts](https://github.com/earthlingsorg/earthlings-contracts) | MIT |
| Architecture documentation | the `/docs` folder of the same repository: the identity model, data minimization, security, reputation, the flow of contributed work | MIT |
| The contract address and all its transactions | [0x20e7962878429B803E35F83ba34eD291afEC2Be4](https://polygonscan.com/address/0x20e7962878429B803E35F83ba34eD291afEC2Be4) | public data |
| The registry of passports and of temporary documents of participants in the founding | the Polygon blockchain, read directly from the contract | public data |
| The public DAO voting channel | [snapshot.org, the earthlings-dao.eth space](https://snapshot.org/#/s:earthlings-dao.eth) | public data |
| The on-chain treasury | [0xaEC7016218f7883bf6e47a2C932FdE6d822086C0](https://app.safe.global/home?safe=matic:0xaEC7016218f7883bf6e47a2C932FdE6d822086C0) | public data |

## What is closed and why

| Component | Reason |
|---|---|
| The server side of the platform | It contains the logic that governs access to accounts. Publishing it before an independent audit raises the risk of participants' accounts being compromised and adds nothing to the verifiability of the people. |
| The identity verification system | It works with documents and biometrics. Here, keeping it closed is part of protecting personal data, not concealment. The Biometric Verification Policy and the Privacy Policy describe how data minimization works in identity verification. |
| Deployment infrastructure | It contains server configuration. Publishing it would hand an attacker a map. |

The open smart contract does not decide who receives an entry in the registry or who votes: whom to issue an entry to is decided by the closed identity verification system, and the right to vote at the moment of voting is confirmed by our server. The contract only records issuance and burning, and each of them is visible on the network without us; exactly where we have to be trusted is set out below.

## What can be verified right now without trusting us

- **The rules of the passport.** Read the contract's source code in the repository: the passport is non-transferable, one per wallet, and the holder can burn it themselves.
- **How many entries the registry holds.** Call `totalSupply` on the contract through any node of the Polygon network: the contract is not verified on a block explorer, so there is no tab there for reading it. That number does not come from us - it comes from the blockchain. But it has to be read correctly, and we explain how. **The contract currently holds four test entries**, made while debugging the system before launch, and there are no real participants among them; they remain in this number. **From 22 October 2026 until the day the text is adopted**, this number minus the four test entries counts people who have confirmed their identity and are taking part in the founding: if the Declaration is adopted, those of them who sign it will become earthlings. **After adoption**, the number of earthlings is the number of those who have signed the Declaration; it cannot be read from the contract today: the record of signing is kept by our server, not by the registry. How to verify this number will be published before the day of the vote.
- **Whether a particular address holds an entry in the registry.** Call `balanceOf` in the same way. It returns 1 or 0; from 22 October 2026 until the Declaration is adopted, a 1 means a temporary document of a participant in the founding, not a passport.
- **DAO votes.** Open the Snapshot space to see the proposals, the votes, and the signatures. Every vote is signed by the voter's wallet - we cannot forge someone else's vote. A voter can be added by issuing an entry in the registry: the contract owner key can issue one to any wallet that does not yet hold an entry, and every issuance is visible on the network. Votes in this channel are open; for what this changes, see the section "What is not there yet".
- **The right to vote.** Snapshot asks our server whether an address holds an entry in the registry. This step has to be trusted at the moment of voting - but not afterwards: the addresses of everyone who voted are public, and anyone can check each of them for themselves in the contract on Polygon. A discrepancy would be visible.

We describe the last point plainly because it is one of the places where we have to be trusted. We prefer to name such places ourselves rather than leave them to be found by whoever checks. There are several of them: the right to vote at the moment of voting; the contract owner key, with which registry entries are issued and burned; the decision of the closed identity verification system on whom to issue an entry to; the record of signing the Declaration, which is kept by our server, not by the registry; votes in Cells and delegation, which are recorded in the platform's database; the treasury wallet with a signature threshold of one. Every issuance, every burn, and every movement of funds is visible on the network, but the grounds for an issuance cannot be checked from outside.

The second of them is the contract owner key. In the deployed version of the contract, the functions for issuing and burning a passport are available to the owner, and the owner key is stored on the server of the issuance service, which is managed by the founder. After the adoption of the Declaration, with which the Charter enters into force (Charter, Article 38), Article 21 of the Charter permits burning against the holder's will on one ground only - annulment of an invalid issuance - and only through a procedure: notice, a period for objections, an opinion of the Council, a secret ballot with a higher majority, appeal. These guarantees are not in the code - they are procedural; until the Declaration is adopted, there is no Independent Council and no Assembly, and against the holder's will, the temporary document of a participant in the founding is burned under the procedure set out in the document "The Founding Period" (Part 2, section 5), and that too is procedural. That means they now rest on our word rather than on the technology, and we acknowledge it. What is being done about it: separating the rights of issuance and burning into distinct roles, adding a delay on executing a burn, and transferring ownership to a multisignature of elected structures or to the control of the Assembly. When this happens is governed by the conditions for moving between phases in the [Roadmap](https://earth-lings.org/documents/en/en19-roadmap.html).

## What is not there yet

An honest list of what is declared as a principle but not yet done:

- The contract source code is published in the repository, but **it is not verified on a block explorer**. This means that anyone who wants to confirm that the published source matches the deployed bytecode has to check it themselves: build the source from the repository and compare the result with the bytecode on the network.
- **No independent security audit has been carried out.** One is planned before operations are expanded.
- **The Treasury smart contracts have not been deployed.** Only the passport contract is deployed; the internal economy of participation is for now kept in the platform's own ledger.
- The public voting channel is **deployed and technically working, but no substantive votes have yet been held in it**. Votes in it are open: each vote and the voter's address are visible to all. The Declaration (Article 9) requires a secret personal vote; we do not yet have a tool for secret voting - one is being chosen, and the vote of 17 February 2027 on the adoption of the Declaration will be held by secret ballot. After the transition, verification will no longer mean looking through a list of votes: the outcome will be checked using the proof of the count and an open recount program. And even then there is one thing secrecy will not provide. Remote voting does not protect against someone standing over the voter in the final minute before voting closes: voting again before the close undoes coercion applied before that minute, but not coercion applied during it.
- A bug bounty programme is declared as a principle but **has not yet been launched**.
- **The contract owner's rights have not been split or transferred.** Issuing and burning a passport are available to a single key, there is no delay on execution, and the owner key is stored on the server of the issuance service, which is managed by the founder. The restrictions of Article 21 of the Charter are procedural, not technical; until the Declaration is adopted, there is no Independent Council and no Assembly (Charter, Article 38), and against the holder's will, the temporary document of a participant in the founding is burned under the procedure set out in the document "The Founding Period" (Part 2, section 5).
- **There is still no multisignature on the treasury wallet.** The signature threshold is one; this can be checked at the wallet address. Transferring the treasury keys to a multisignature of elected Core Nodes or to the control of the Assembly is a criterion for moving between phases of the Roadmap.

## The right of reproduction

The registry of passports lives on the blockchain, not on our servers, and the contract code is open. This has a practical consequence: if, after the Declaration is adopted, its implementation becomes impossible as a result of a seizure of governance, the shutdown of infrastructure, or other circumstances, confirmed earthlings will be able to continue the people in existence on a different technical or organizational basis against the same registry (Declaration, Article 11). The registry entries carry over; the server layer is replaceable.

Reproduction rests on two supports, and the second is no less important than the first. The registry gives continuity of the records of confirmed people (the record of signing the Declaration is kept by our server, not by the registry), and **the published specification** gives the ability to build the instrument again: the rules, thresholds, quorums, periods, and procedures are set out in the Charter, in the Treasury document, and in the other documents of the corpus. What is reproduced is therefore not our code but the system as described. Copying the closed server side is not needed; a new platform will have to build its own identity verification.

Keeping the server side closed therefore does not negate the right of the people, once it has been founded, to continue without the founders. The signs of a lawful continuation - a preserved unamendable core, the will of confirmed individuals, and continuity of procedures - are described in the document [Roadmap of the Transitional Period](https://earth-lings.org/documents/en/en19-roadmap.html).
