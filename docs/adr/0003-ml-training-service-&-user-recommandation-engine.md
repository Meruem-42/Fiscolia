# ADR-0003: ML TRAINING SERVICE & USER RECOMMANDATION ENGINE

**Date:** 2026-05-04

## STATUS

Accepted

## CONTEXT/PROBLEM

We would like to improve the Fiscolia service by suggesting more relevant fiscal choices to users based on their personal profile. We also want to introduce machine learning into the project for both practical and academic purposes.

Currently, users receive no personalized recommendations — all users see the same options regardless of their situation. By leveraging profile data (income, family status, etc.), we could meaningfully guide users toward the fiscal choices most relevant to them.

## DECISION

We decide to implement a two-phase ML pipeline, clearly separated between training and inference:

**Phase 1 — Training service (`make training`)**
Use a dataset of fictive user profiles (e.g. yearly income, number of children, family status) to train a clustering model that assigns users to a fiscal profile. For academic purposes, this training pipeline is exposed as a standalone `make training` command in the Makefile, which produces a serialized model artifact consumable by the other Fiscolia services.

We decide to use :
- `pandas` : to load data from CSV dataset
- `numpy` : transform these data to matrices
- `pytorch` : transform matrices to tensors to train the model

Specificaly, `pytorch` makes this possible for our project :
- define and train the autoencodeur (`nn.Module`, `Linear`, `ReLU`, `MSELoss`, `Adam`)

**Phase 2 — Inference integration (`backend-recommandation`)**
A new backend feature reads the authenticated user's stored profile data and runs it through the trained model to determine a cluster assignment (e.g. *"You belong to fiscal profile X"*). This recommendation can later be enriched to highlight specific fiscal boxes the user is most likely to need, based on their profile probability scores.

**New fields to add to the `users` table (PostgreSQL):**
- `etat_civil` — Marital status
- `quotient_familial` — Family quotient
- `situation_specifique` — Specific situation (disability, caregiver, etc.)
- `rni` — Net taxable income (Revenu Net Imposable)
- `csp` — Socio-professional category

#### Advantages:
- Adds immediate user value: personalized fiscal profile from the first recommendation
- Clean separation: training and inference are fully decoupled and independently maintainable
- Academically sound: `make training` provides a reproducible, demonstrable pipeline
- Extensible: the cluster label output today can evolve into weighted recommendations tomorrow
- Non-intrusive: the backend only depends on the serialized model artifact, not on training code

#### Disadvantages:
- Model staleness: the artifact must be manually retrained when data distributions shift
- No automated retraining loop at this stage — `make training` must be run explicitly
- Initial output is minimal (cluster label only) — may feel limited to end users at first
- Requires agreement on artifact storage and versioning across services

## Alternatives

### Option A: Pure Scikit-learn (KMeans or DBSCAN directly on raw features)

Skip the autoencoder entirely and apply KMeans (or another clustering algorithm) directly on the scaled feature matrix, without any intermediate neural dimensionality reduction.

#### Advantages:
- Much simpler pipeline — no neural network, no training loop, no epochs
- Directly interpretable: the clustering operates on the actual feature space
- Faster to run and easier to debug
- `joblib` serialization is trivial for the resulting KMeans artifact

#### Disadvantages:
- KMeans struggles with high-dimensional or non-linearly distributed data — the autoencoder's latent space addresses exactly this
- No learned feature compression: all input features are treated equally regardless of their actual relevance
- Less academically interesting as a showcase of ML techniques

### Option B: TensorFlow / Keras Autoencoder + KMeans

Same architecture as the current solution (autoencoder for feature extraction, KMeans for clustering), but implemented with TensorFlow/Keras instead of PyTorch.

#### Advantages:
- Keras's `Model.fit()` loop is more concise than a manual PyTorch training loop
- TensorFlow Serving makes model deployment more straightforward in production
- Slightly more beginner-friendly API for building sequential neural networks

#### Disadvantages:
- TensorFlow is heavier to install and configure locally than PyTorch
- PyTorch is now the dominant framework in academic research — TensorFlow has lost significant ground since 2022
- The manual training loop in the current PyTorch code is actually a pedagogical asset for academic presentation
- Mixing TF with scikit-learn's KMeans raises the same integration questions as with PyTorch

## CONSEQUENCES

### ✅ Positive

- Users receive a first personalized experience: a fiscal profile assignment based on their real data
- The training pipeline is reproducible and demonstrable via `make training` — valuable for academic presentation
- The architecture is cleanly extensible: richer recommendations (probability scores, highlighted boxes) can be layered on top without restructuring
- New `users` table fields lay the groundwork for future fiscal features beyond ML
- The team gains hands-on experience with an end-to-end ML integration in a real product

### ❌ Negative

- The model must be manually retrained and redeployed when user data evolves — no automation at this stage
- The recommendation output is intentionally limited to a cluster label in v1, which may underwhelm users without proper UX framing
- The team must agree on artifact storage conventions (local path, shared Docker volume, or object storage) before implementation
- New database fields require a schema migration and corresponding backend validation