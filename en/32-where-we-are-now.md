# Where We Are Now

*The Earthlings people*

## What this document is for

We claim that Earthlings is verifiable. Such a claim makes sense only when it is possible to say exactly what is being verified and by what means. Instead of the general formula "our code is open", we therefore publish the precise boundary: what is open, what is closed, and for what reason.

The founding period is now under way: until the day the Declaration is adopted the people is still being founded, and some of the numbers below read differently from how they will read afterwards. Its rules and dates are set out in the document [The Founding Period](https://earth-lings.org/documents/en/en20-the-founding-period.html) - we do not repeat them here, so that the dates keep a single source.

> **The principle.** What is open is everything on which the verifiability of the people depends: who is a participant, how they became one, how many of us there are, and how a vote is counted. What is closed is what publishing would add nothing to verifiability but would create risk for participants: the server layer and the processing of personal data.

## What is open

| Component | Where | Licence |
|---|---|---|
| The passport smart contract EarthlingPassportV2 | [github.com/earthlingsorg/earthlings-contracts](https://github.com/earthlingsorg/earthlings-contracts) | MIT |
| Architectural documentation | the `/docs` folder of the same repository: the identity model, data minimization, security, reputation, the flow of contributions | MIT |
| The contract address and all its transactions | [0x20e7962878429B803E35F83ba34eD291afEC2Be4](https://polygonscan.com/address/0x20e7962878429B803E35F83ba34eD291afEC2Be4) | public data |
| The registry of passports | the Polygon blockchain, read directly from the contract | public data |
| The public channel of DAO votes | [snapshot.org, the earthlings-dao.eth space](https://snapshot.org/#/s:earthlings-dao.eth) | public data |
| The on-chain treasury | [0xaEC7016218f7883bf6e47a2C932FdE6d822086C0](https://app.safe.global/home?safe=matic:0xaEC7016218f7883bf6e47a2C932FdE6d822086C0) | public data |

## What is closed and why

| Component | Reason |
|---|---|
| The server side of the platform | It contains the logic of access to accounts. Publishing it before an independent audit raises the risk of participants' accounts being broken into and adds nothing to the verifiability of the people. |
| The identity verification system | It works with documents and biometrics. Here closedness is part of the protection of personal data, not concealment. How data minimization is arranged is described in the open documentation. |
| Deployment infrastructure | It contains server configuration. Publishing it would be a map for an attacker. |

None of the closed components determines who is an earthling and how a vote is counted. That is determined by the open smart contract.

## What can be verified right now without trusting us

- **The rules of the passport.** Read the contract's source code in the repository: the passport is non-transferable, one per wallet, and the holder can burn it themselves.
- **How many passports have been issued.** Call the contract's `totalSupply`. That number is named not by us - it is named by the blockchain. But it has to be read correctly, and we explain how. **There are four test entries there at present**, made while debugging the system before launch, and none of them is a real participant. **From 7 September 2026 until the day the text is adopted**, this number means people who have confirmed their identity and are taking part in the founding: they become earthlings only after the Declaration is adopted. **After adoption**, the number of passports issued is the number of earthlings.
- **Whether a particular address holds a passport.** Call `balanceOf`. The answer: 1 or 0.
- **DAO votes.** Open the space on Snapshot and see the proposals, the votes, and the signatures. Every vote is signed by the voter's wallet - we can neither add a vote nor forge someone else's.
- **The right to vote.** Snapshot asks our server whether an address holds a passport. This step has to be trusted at the moment of voting - but not afterwards: the addresses of everyone who voted are public, and any person can check each of them in the contract on Polygon themselves. A discrepancy would be visible.

We describe the last point plainly, because it is one of the two places where we have to be trusted. We prefer to name them ourselves rather than leave them as a find for someone checking.

The second place is the contract owner's keys. In the deployed version of the contract the functions for issuing and burning a passport are available to the owner, and the owner key is currently with the founder. The Charter, Article 21, permits burning against the holder's will on two grounds only and only with a procedure: notice, a period for objection, an opinion of the Council, a secret ballot with a raised majority, appeal. These guarantees are not in the code - they are procedural. That means they now rest on our word rather than on the technology, and we acknowledge it. What is being done about it: separating the rights of issuance and burning into distinct roles, a delay on executing a burn, and transferring ownership to a multisignature of six elected signatories. The timing is in the [Roadmap](https://earth-lings.org/documents/en/en19-roadmap.html).

## What is not there yet

An honest list of what is declared as a principle but not yet done:

- The contract source code is published in the repository, but **it is not yet verified in a blockchain explorer**. This means that the correspondence between the published source and the deployed bytecode has for now to be checked independently. Verification is in progress.
- **No independent security audit has been carried out.** It is planned before operations are expanded.
- **The Treasury smart contracts are not deployed.** Only the passport contract is deployed; the internal economy of participation is for now kept in the platform's accounts.
- The public voting channel is **deployed and technically working, but no substantive votes have yet been held in it**.
- A vulnerability search programme (bug bounty) is declared as a principle but **has not yet been opened**.
- **The contract owner's rights have not been split or transferred.** Issuing and burning a passport are available to a single key, there is no delay on execution, and the key is with the founder. The restrictions of Article 21 of the Charter operate procedurally.
- **There is still no multisignature on the treasury wallet.** The signature threshold is one; this can be checked at the wallet address. The move to a composition of six signatories is a criterion for moving between phases.

## The right of reproduction

The registry of passports lives on the blockchain, not on our servers, and the contract code is open. From this follows something practical: if the infrastructure is stopped or its operation is captured, the community can build a new platform against the same registry. What carries over is people and their passports; the server layer is replaceable.

Reproduction has two supports, and the second is no less important than the first. The registry gives continuity of people, and **the published specification** gives the ability to assemble the instrument anew: the rules, thresholds, quorums, periods, and procedures are set out in full in the Charter, in the Treasury, and in these documents. What is reproduced is therefore not our code but the system as described. Copying the closed server side is not needed and will not be needed.

The closedness of the server side therefore does not cancel the people's right to continue without the founders. The marks of a lawful continuation - a preserved unamendable core, the will of verified people, and continuity of procedures - are described in the document [Roadmap of the Transitional Period](https://earth-lings.org/documents/en/en19-roadmap.html).
