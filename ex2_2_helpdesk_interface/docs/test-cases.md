# Helpdesk UI test cases

| # | Input / viewport | Expected result |
|---|---|---|
| 1 | Submit all fields empty | Category error; focus moves to category |
| 2 | Unsupported category changed in DevTools | Rejected by allow-list |
| 3 | Title shorter than 5 characters | Length message; title focused |
| 4 | Description shorter than 10 characters | Length message; description focused |
| 5 | Valid sample fields | Safe text-only summary displayed; no network request |
| 6 | Description includes HTML-like text | Displayed as text through `textContent`, not markup |
| 7 | Keyboard-only navigation | Labels, selects, button and visible focus usable by keyboard |
| 8 | 375px narrow mobile | Single-column form and summary; no horizontal overflow expected |
| 9 | 768px tablet | Two-column layout where space allows |
| 10 | 1280px desktop | Centered, constrained-width layout |

Open `index.html` locally. Viewport sizes are suggested for browser DevTools; no backend is configured.
