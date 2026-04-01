## Coding norm

## Google Style Guide

| Token | Convention | Example |
|---|---|---|
| **Var** | `snake_case` | `user_name`, `max_retries` |
| **Function** | `snake_case` | `get_user()`, `calculate_score()` |
| **Class** | `PascalCase` | `UserService`, `GameManager` |
| **Const** | `UPPER_SNAKE_CASE` | `MAX_CONNECTIONS`, `DEFAULT_TIMEOUT` |
| **Private** | `_leading_underscore` | `_internal_method()` |

---

## Universal

- **Descriptive names** → `get_user_by_id()` not `get_u()`
- **No short names** unless very usual (`url`, `id`, `api`)
- **English only**

## Rules

- 5 functions max by file
- 25 lines max by functions

OR

- 1 function by file
- above 25 lines (try to limit under 60 lines)

## Filename

Try to describe as much as possible the implementation
3 words maximum separated by _

```bash
parsing_args.py
```

## Function name

Try to describe as much as possible the implementation
Use `custom` to explain our own implementation of the code.

```python
custom_is_num()
custom_parsing_args()
main()
```


