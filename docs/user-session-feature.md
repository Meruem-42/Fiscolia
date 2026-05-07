# Feature: Session Utilisateur (UserSession)

**Projet:** Fiscolia  
**Périmètre:** Frontend React + Backend FastAPI + PostgreSQL (session store)

## 1) Pourquoi cette feature existe

HTTP est stateless: chaque requête est indépendante.  
Pour éviter de demander email/mot de passe à chaque action, on crée une **session serveur** après un login réussi.

Le principe implémenté dans Fiscolia est:
- Le serveur valide les identifiants.
- Le serveur crée une session en base (table `sessions`) avec une expiration.
- Le serveur renvoie un cookie `session_id` au navigateur.
- Le navigateur renvoie ce cookie automatiquement sur les appels suivants.
- Le backend revalide la session à chaque endpoint protégé (`/api/me`, etc.).

## 2) Vue architecture

```text
[React Frontend]
    |
    | fetch('/api/...', credentials: include)
    v
[Proxy]
    |
    v
[FastAPI backend-auth]
    |
    | SQLAlchemy
    v
[PostgreSQL: users + sessions]
```

Composants principaux:
- Frontend:
  - `srcs/frontend/srcs/pages/Login/Login.jsx`
  - `srcs/frontend/srcs/pages/UserSession/UserSession.jsx`
- Backend auth:
  - `srcs/backend-auth-login/config/main.py`
  - `srcs/backend-auth-login/config/session_store.py`
  - `srcs/backend-auth-login/config/connect_db.py`
- Orchestration:
  - `srcs/docker-compose.yml`

## 3) Modèle de données session côté serveur

Dans `connect_db.py`, le modèle SQLAlchemy `SessionDB` représente les sessions:
- `id`: identifiant de session (UUID string)
- `user_id`: FK (Foreigner Key) vers `users.id` (ça veut dire que `user_id` doit forcément correspondre à un `id` qui existe déjà dans la table "users")
- `data`: JSONB (payload complémentaire, pour le moment peu utile)
- `expires_at`: date d'expiration
- `created_at`: date de création

Cette approche correspond à une session **stateful côté serveur**: l'état des sessions est dans la DB serveur, pas dans le cookie client.

Pour résumer :
- on a un vestiaire (notre serveur) qui possède le manteau de chaque client (en gros la table `sessions`)
- on a un client qui possède un ticket de vestiaire unique (un `cookie`)

Processus imagé :
- L'utilisateur présente son ticket (abc-123).
- Le serveur va chercher dans sa base de données : "À qui appartient ce ticket ?".
- Il trouve la ligne dans la table `sessions` construite via l'objet SessionDB, vérifie si `expires_at` est encore bon, et récupère le `user_id`.

## 4) Cycle complet d'une session

## 4.1 Login (création de session)

### Côté front
Dans `Login.jsx`, `handleSubmit` envoie:
- `POST /api/auth-login`
- body JSON `{ email, password }`
- `credentials: 'include'` pour autoriser le transport des cookies

### Côté backend
Dans `main.py`, route `@auth.post('/api/auth-login')`:
1. Récupère l'utilisateur par email.
2. Vérifie le mot de passe (`verify_password`).
3. Crée une session DB via `create_session(...)` avec TTL 7 jours.
4. Retourne un cookie avec `response.set_cookie(...)`:
   - `key='session_id'`
   - `value=<uuid session>`
   - `httponly=True`
   - `samesite='lax'` (on pourrait passer en samesite=strict si besoin pour ce genre de service)
   - `max_age=7 * 24 * 3600`
   - `secure=True`

Conséquence: le JS frontend ne peut pas lire le cookie (HttpOnly), mais le navigateur l'envoie automatiquement sur les prochains appels HTTP vers le même domaine/route matching.

## 4.2 Utilisation de session (accès aux routes protégées)

Le backend utilise `get_current_user(...)`:
- Lit `session_id` depuis le cookie (`Cookie(None)`).
- Charge la session via `get_session(db, session_id)`.
- Vérifie qu'elle existe et n'est pas expirée.
- Charge l'utilisateur lié.
- Sinon renvoie `401`.

Cette `dependency` est injecté sur `/api/me`. (dependency injection)

On parle de "dependency" pour exprimer que la fonction `get_current_user()` se comporte comme un vigile garant du bon déroulement du backend /api/me, en l'occurence ici il vérifie le "badge" (`session_id`) dans le cookie.

Dans `session_store.py`, `get_session(...)`:
- Retourne `None` si session absente.
- Supprime automatiquement la session si expirée puis retourne `None`.

## 4.3 Frontend UserSession

Dans `UserSession.jsx`, au démarrage:
- `GET /api/me` avec `credentials: 'include'`.
- Si réponse OK: hydrate l'état `user` (en gros on change l'état du User) et affiche l'espace UserSession.
- Sinon: redirection vers `/login`.

Cela fait de `/api/me` la source de vérité d'authentification côté front.

## 4.4 Vérification automatique dès la page Login

Dans `Login.jsx`, un `useEffect` a été ajouté:
- Appel `GET /api/me` dès l'ouverture de la page.
- Si cookie valide: redirection immédiate vers `/session`.
- Sinon: on affiche le formulaire de login.

Résultat UX: l'utilisateur déjà authentifié n'a plus besoin de retaper ses identifiants.

## 4.5 Logout

`POST /api/auth-logout`:
- Supprime la session en base via `delete_session(...)`.
- Demande au navigateur de supprimer `session_id` (`response.delete_cookie`).
- Le front redirige ensuite vers `/`.

## 5) Nettoyage et expiration des sessions

Deux niveaux de nettoyage existent:
- **Lazy cleanup** à la lecture (`get_session`) si la session est expirée.
- **Background cleanup** dans `connect_db.py` (lifespan FastAPI):
  - tâche asynchrone chaque 3600 secondes,
  - supprime les sessions `expires_at < now()`.

Cela évite l'accumulation de sessions obsolètes en base.

## 6) Contrat des endpoints liés à la session

- `POST /api/auth-login`
  - Entrée: `{ email, password }`
  - Succès: `200` + JSON de bienvenue + `Set-Cookie: session_id=...`
  - Erreur: `400` si credentials invalides

- `GET /api/me`
  - Entrée: cookie `session_id`
  - Succès: `200` + user `{ id, email, firstname, lastname }`
  - Erreur: `401` si non authentifié, session invalide/expirée

- `POST /api/auth-logout`
  - Entrée: cookie `session_id` (optionnel)
  - Succès: `200` + suppression session côté serveur + suppression cookie côté client

## 7) Sécurité: ce qui est bien couvert

- Mot de passe hashé (`bcrypt` via passlib) avant stockage.
- Cookie `HttpOnly`: réduit le risque d'exfiltration via JS.
- Cookie `SameSite=Lax`: limite une partie des scénarios CSRF. (l'exemple du cookie qui est utilisé par un nouveau lien sur un site pirate, protégé)
- Session stockée côté serveur: révocation immédiate possible (delete row).
- Expiration TTL explicite + purge périodique.

## 8) Points d'attention / limites actuelles

- `secure=True` sur cookie exige HTTPS:
  - en environnement non TLS, le cookie peut ne pas être stocké/envoyé par le navigateur. (mais en soit rarement un pb en localhost)


## 9) Résumé pédagogique pour l'équipe

La feature UserSession suit un pattern classique et robuste:
1. **Login** crée une session en base.
2. Le backend envoie un **identifiant de session opaque** dans un cookie sécurisé.
3. Le navigateur renvoie ce cookie automatiquement.
4. Le backend valide ce cookie à chaque requête protégée via lookup DB.
5. Le frontend décide de l'UI en fonction de `/api/me`.
6. Logout = suppression DB + suppression cookie.

En pratique, la session n'est donc jamais "stockée dans le front" :
- le front ne connaît que l'état renvoyé par `/api/me`,
- la vérité d'authentification reste sur le serveur (table `sessions`).