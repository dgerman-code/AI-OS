# Secrets and Credentials

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

No secret is created, named or stored by this document. It defines where secrets may live and what holding one does and does not mean.

## 1. Values never enter the repository or the operational database

| System | Holds | Never holds |
|---|---|---|
| **Secret manager** | The value | — |
| **Repository** | A **reference**: a name, an environment binding, a rotation policy class | A value, a private key, an access token, a connection string containing credentials |
| **Operational database** | A **reference**, and metadata about the reference | A value |
| **Object storage** | Nothing secret | A value, a key, an export containing either |

A reference resolves to nothing for anyone who cannot already resolve it. That is what makes it safe to commit, and it is the only property that makes it safe.

## 2. Reference versus value

A **secret reference** names a secret and, where relevant, its environment binding: `secret.<name>@<environment>`. It is inert: it authorises nothing, and possessing it is not possessing the secret.

Resolution happens at runtime, by an identity the secret manager already authorises, and is **audited by the manager**. Nothing in Phases 1–10 resolves a reference; Phase 10 defines only that references are what is stored.

## 3. Environment-specific by construction

Every environment has its own secrets. A reference in the repository is environment-agnostic; the binding resolves per environment. **No secret is shared across environments**, because a shared secret makes environment separation a naming convention (`storage/migration-and-environment-governance.md` §3.3).

## 4. Service accounts

| Property | Rule |
|---|---|
| Least privilege | Grants are the minimum for the identity's declared purpose, evaluated over the seven access dimensions |
| Separation | A service account that writes governed records is not the account that administers schema, and neither can alter backups |
| Governance meaning | **None.** A service account may write the row that records a human decision. It is never recorded as the decider (`storage/access-control-and-rls-boundary.md` §5) |
| Attribution | Every governed record names the human or governed act **and**, separately, the system identity. Two fields, always |

## 5. Rotation and revocation

Two different acts:

- **Rotation** replaces a value on a schedule or on suspicion. The reference is unchanged; everything holding the reference continues to work; the rotation is audited.
- **Revocation** ends an identity's ability to use a secret, immediately, on compromise. **It does not change the identity's governance meaning**, because the identity never had one — and every write made under the credential during the exposure window is treated as unverified pending review (`storage/failure-modes.md` mode 13).

Rotation without revocation leaves a compromised value usable until it expires. Revocation without rotation leaves it valid for anyone else who holds it. Compromise requires both.

## 6. Auditable without exposure

What is auditable: which reference exists, which identity may resolve it, when it was created, rotated, revoked and resolved, and by whom. What is never recorded anywhere: the value.

**Metadata about a secret is not a secret** (standard §14). Treating it as one is how rotation history becomes unauditable and how nobody can answer which credentials were live during an exposure window.

## 7. Runtime credential versus governance identity

> **A credential is a capability to operate. A governance identity is a party to the architecture. Neither implies the other, in either direction.**

A human with a Decision Right may hold no credential at all. A service account with every credential holds no Right, exercises none, and gains none by being able to write the row that records one. An AI model, provider or deployment gains no authority by possessing credentials — Phase 9 denies that capability confers authority; Phase 10 denies that access does.

## 8. Vendor abstraction

The secret-management interface is one of the five adapter boundaries (`architecture/storage-persistence-architecture.md` §8). What is portable is **reference-by-name resolution, rotation, revocation and audit**. Which manager provides it is an implementation choice, and **no specific vendor is mandated here** — naming one would put a governance semantic behind a product decision.

## 9. What this document does not do

It creates no secret, no service account, no credential and no binding. It connects to nothing. Any secret this architecture eventually requires is created under the authorisation that governs it, in the manager, and never by committing it.
