# ADR-0001: Choice of DB Session Store

**Date:** 2026-05-01

## STATUS

Approuved

## CONTEXT / PROBLEM

Our application (FastAPI backend + React frontend) requires a mechanism to manage authenticated user sessions. We need to store session data server-side so that we can identify and authorize users across HTTP requests, which are stateless by nature.

We already operate a PostgreSQL instance as our primary database. Our server resources are partially constrained: a significant portion of available RAM is dedicated to AI/ML inference processes, making in-memory session stores costly to operate.

The solution must support:
- Secure session creation, retrieval, and revocation
- Automatic expiration of stale sessions
- No additional infrastructure beyond what we already run

## DECISION

We will use **PostgreSQL as the session store**, via a dedicated `sessions` table managed by SQLAlchemy.

Session identifiers (UUIDs) are issued at login and stored in an `HttpOnly` cookie on the client. On each authenticated request, FastAPI looks up the session record in PostgreSQL to validate the user.

**Key reasons for this choice:**
- We already have a PostgreSQL instance — no new infrastructure, no new operational burden.
- PostgreSQL is persistent (survives restarts), ACID-compliant, and supports immediate revocation by deleting a row.
- It consumes no additional RAM, unlike Redis or other in-memory stores, which is critical given our AI workloads.
- For our expected traffic levels (< 5 000 req/min because it is an academic school project), the latency overhead of a DB lookup (~5–20 ms) is perfectly acceptable.
- The implementation is straightforward and well understood by the team.

#### Advantages

- **Zero new infrastructure** — reuses the existing PostgreSQL instance.
- **Immediate revocation** — deleting a session row takes effect instantly, with no propagation delay.
- **No RAM overhead** — sessions are stored on disk, leaving memory available for AI/ML processes.
- **ACID guarantees** — sessions are durable and consistent even across restarts or failures.
- **Simple mental model** — sessions are just rows in a table; easy to inspect, debug, and audit.
- **TTL via `expires_at`** — expiration is handled by a scheduled cleanup query, no external daemon needed (we could implement a cron : */5 * * * * psql -c "DELETE FROM sessions WHERE expired_at < NOW();").

#### Disadvantages

- **Higher latency than Redis** — each session lookup hits the DB (~5–20 ms vs. ~0.5 ms for Redis).
- **DB load** — every authenticated request adds a read query; at very high scale this may become a bottleneck.
- **Manual cleanup required** — expired sessions must be purged periodically (e.g., via a background task or cron job), unlike Redis which handles TTL natively.

## Alternatives

### Option A: Redis as session store

Store sessions in Redis (in-memory key-value store) with native TTL support.

#### Advantages

- Sub-millisecond session lookups.
- Native TTL — expired sessions are deleted automatically, no cleanup needed.
- Industry-standard solution for high-throughput session management.

#### Disadvantages

- **Requires additional infrastructure** — a Redis instance must be deployed, monitored, and maintained.
- **RAM consumption** — directly competes with our AI/ML processes for memory on the same server.
- **Volatile by default** — sessions are lost on restart unless persistence (AOF/RDB) is explicitly configured.
- Adds operational complexity (connection pooling, eviction policy tuning, failover).

### Option B: JWT with Refresh Tokens (stateless access tokens)

Issue short-lived JWTs (15 min) as access tokens, paired with long-lived opaque refresh tokens stored in PostgreSQL.

#### Advantages

- Access token validation is fully stateless — no DB lookup per request during the token's lifetime.
- Scales horizontally without a shared session store.
- Compatible with OAuth2 / OpenID Connect standards.

#### Disadvantages

- **More complex to implement** — requires managing two token types, a rotation strategy, and a React interceptor for silent refresh.
- **Access tokens cannot be revoked immediately** — a stolen token remains valid until expiration (up to 15 min).
- Refresh tokens still require a DB table, meaning PostgreSQL is used anyway.
- Overkill for a monolithic application without third-party API consumers.

## CONSEQUENCES

### ✅ Positive

- No new service to deploy or operate — the team can focus on product features.
- Full control over session lifecycle: creation, extension, and revocation in a single SQL query.
- Sessions are visible and auditable directly in the database (useful for debugging and compliance).
- Memory pressure on the server is not increased.

### ❌ Negative

- A cleanup job must be implemented and scheduled to remove expired sessions.
- If traffic grows significantly beyond 5 000 req/min, the session lookup may become a DB bottleneck and the architecture will need to be revisited (e.g., adding a read replica or migrating to Redis).
- Session reads will slightly increase overall PostgreSQL query load.

## IMPLEMENTATION

- Add a `sessions` table via a SQLAlchemy model with columns: `id` (UUID, PK), `user_id` (FK), `data` (JSON), `expires_at` (DateTime), `created_at` (DateTime).
- Create a composite index on `(id, expires_at)` to make session lookups efficient.
- Implement `create_session`, `get_session`, and `delete_session` functions in a `session_store.py` module.
- Edit (or create if missing) `POST /auth/login`, `POST /auth/logout` routes in FastAPI; issue and clear the `session_id` cookie (`HttpOnly`, `Secure`, `SameSite=Lax`).
- Inject a `get_current_user` dependency (reads the cookie → queries PostgreSQL) into all protected routes.
- Schedule a `cleanup_expired_sessions` background task (APScheduler or FastAPI lifespan) to delete rows where `expires_at < now()`, running once per hour (for example).
- Set `withCredentials: true` on the Axios/fetch instance in React so cookies are sent on every cross-origin request.

## NOTES

> This decision should be revisited if the application scales beyond ~5 000 authenticated requests per minute, or if multiple backend instances are deployed and session latency becomes measurable in user-facing response times. At that point, introducing Redis (or a read replica for the sessions table) would be the natural next step.

> JWT + Refresh Tokens remains a valid future migration path if the API is ever exposed to third-party consumers or a mobile app that cannot use cookies reliably.