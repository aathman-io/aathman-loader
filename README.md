##Aathman Loader

Aathman Loader is a trust-aware model loading gate that ensures a machine-learning model is executed only after passing all declared trust checks.

It is the final enforcement layer in the Aathman Trust Stack, sitting downstream of identity verification, policy enforcement, and intent declaration.

Aathman Loader answers one question with certainty:

“Is this model allowed to run here, right now?”

If the answer is no, the model is not loaded.

---

##What Aathman Loader Does

Aathman Loader orchestrates four sequential trust checks before loading a model:

Identity Verification
Confirms the model file matches its cryptographically signed Aathman certificate.

Policy Enforcement (PaCM)
Applies explicit organizational rules such as allowed signers and parameter limits.

Intent Enforcement (MTM)
Enforces declared usage intent and deployment constraints from a Model Trust Manifest.

Model Loading
Loads the model into memory only if all checks pass.

If any stage fails, loading is blocked and a structured error is raised.

---

##Position in the Aathman Architecture

Aathman Loader does not implement trust logic itself.
It imports and composes the other Aathman components.

Aathman Core  → verifies model identity
PaCM          → enforces policy
MTM           → enforces declared intent
Loader        → enforces execution


This separation keeps the system minimal, auditable, and extensible.

---

##What Aathman Loader Does NOT Do

Aathman Loader intentionally avoids:

Evaluating model performance

Inspecting training data

Making safety or ethics judgments

Modifying the model

Performing inference

Managing deployment infrastructure

Its scope is narrow by design: trust enforcement at load time.

---

##Repository Contents

aathman-loader/

├── loader.py      # Trust-aware model loader (core logic)

├── errors.py      # Shared trust violation exception

├── demo.py        # Optional demonstration script

├── README.md

├── LICENSE

├── CLA.md


Only loader.py and errors.py are required for functionality.

---

##How Loader Works (Execution Order)

1. Identity Verification

Uses Aathman Core to verify:

Certificate signature

Fingerprint match

Model metadata integrity

Failure at this stage stops execution immediately.

---

##2. Policy Enforcement (PaCM)

Applies a policy file defining:

Required signatures

Allowed signers

Parameter limits

Policy decisions are explicit and deterministic.

---

##3. Intent Enforcement (MTM)

Validates and enforces the model’s declared intent, such as:

Offline-only usage

No user-facing output

Mandatory human review

Declared constraints are enforced as hard gates.

---

##4. Model Loading

Only after all trust checks pass is the model loaded via torch.load.

---

##Error Handling Model

All failures raise a single exception type:

TrustViolationError

Each error contains:

stage — where the failure occurred

reason — human-readable explanation

Example output:

DENIED
Stage: policy
Reason: Signer is not in allowed_signers


This makes failures predictable and machine-readable.

---

##Demo Usage

A demonstration script is included.

Example:
python demo.py


Possible outputs:

Identity failure

Policy denial

MTM constraint violation

Successful model load

This is intended for testing and interviews, not production.

---

##Dependencies

Aathman Loader depends on the following sibling repositories:

aathman-core

aathman-pacm

aathman-mtm

During development, these are expected to exist as sibling directories.
This setup is intentional and temporary.

Future packaging may consolidate this structure.

---

##Security Model

Aathman Loader assumes:

Certificates are cryptographically signed

Policies are explicit and auditable

Intent is declared by the model owner

Enforcement is fail-closed

If trust cannot be established, execution is denied.

---

##License

Aathman Loader is licensed under the Apache License 2.0.
See LICENSE for full terms.

---

##Contributing

Contributions are welcome.

All contributors must sign the Contributor License Agreement (CLA) before code can be merged.
See CLA.md for details.

---

##Final Note

Aathman Loader is intentionally small.

Its power comes not from complexity, but from clear boundaries, deterministic behavior, and strict enforcement.

It is designed to be trusted.
