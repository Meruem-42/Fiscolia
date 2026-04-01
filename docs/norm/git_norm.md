# Git commit norm

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

---

## First line

- **50 - 70 char**
- **Imperative verb** : `Add`, `Fix`, `Remove`, `Update`, `Refactor`…
- **No capital letter** right after the `:`
- **No dot at the end**

```
feat(agent scrapper): agent creation

- Step 1
- Step 2
- Step 3
- ...

[Optionnal]
New agent callable @agent_scrapper
BREAKING CHANGE: Use agent scrapper instead of the previous database content.
```

---

## Types

| Type | Usage |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fix |
| `docs` | Markdown doc |
| `style` | Formatage |
| `refactor` | Refactoring (no fix, no feat ) |
| `test` | Add/modify tests |
| `perf` | Improvement of the performances |

---

## Body

- Need **newline** between subject and footer
- Explain **what** and **why** (not how)
- **72 chars maximum**
- Bullet-point **list** possible

---

## Footer

To reference issues or warn for **breaking changes** :

```
Fix authentication timeout issue

Closes #142
BREAKING CHANGE: The token format has changed. Clients must
update to the new JWT format.
```

---

## Règles clés à retenir

1. **1 commit = only one logical thing**
2. **Write in english**
3. **Explain why**, not how.
4. **Avoid incomplete commit** as `fix stuff` or `WIP`
