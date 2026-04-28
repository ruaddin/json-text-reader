# History Drawer — Design Spec (Option C)

## Overview

A slide-in history panel triggered by a **History** button in the app header. Stores the last 10 input/output pairs. Does not interrupt the main layout.

---

## Trigger Button

- Placed in the **top-right corner** of the app, next to or inside the existing controls row
- Label: `History` with a small badge showing the count, e.g. `History (10)`
- Clicking toggles the drawer open/closed

---

## Drawer

- Slides in from the **right side**, overlaying the main content
- Width: `260px`
- Height: full page height
- Background: primary background color (`#f0f2f5`)
- Left border: `0.5px` separator line
- Does **not** push or resize the main layout

---

## Drawer Header

- Top section with two items side by side:
  - **Left:** label `History` in medium weight
  - **Right:** muted text showing entry count, e.g. `10 entries`
- Bottom border separating it from the search box

---

## Search Box

- Full-width text input inside the drawer, below the header
- Placeholder: `Search inputs...`
- Filters the list in real time as the user types
- Searches against the **input text** content

---

## History List

- Scrollable list of up to **10 entries**
- Newest entry at the top
- Each entry shows:
  - **Top row:** input preview (truncated with ellipsis) on the left, timestamp on the right (e.g. `now`, `2m`, `12m`)
  - **Bottom row:** output preview, truncated with ellipsis, in muted color
- Active/selected entry has a subtle highlighted background
- Clicking an entry restores it (see [Restore Behavior](#restore-behavior))

---

## Entry Data Stored Per Item

Each history entry saves:

| Field | Description |
|---|---|
| `input` | The raw input text or JSON |
| `output` | The rendered output text |
| `timestamp` | ISO string of when the entry was created |
| `settings.wrapWidth` | Wrap width slider value |
| `settings.fontSize` | Font size slider value |
| `settings.lang` | Translate-to language value |

---

## Restore Behavior

When the user clicks a history entry:

1. The **input textarea** is populated with the saved input
2. The **output block** is populated with the saved output
3. **Wrap width**, **font size**, and **translate-to language** sliders/selectors are restored to the saved settings values
4. The drawer **closes automatically**
5. The restored entry moves to or stays at the **top of the list**

---

## Adding a New Entry

A new entry is added every time output is successfully generated:

- Prepended to the **top** of the list
- If the list already has **10 entries**, the oldest one is removed
- **Duplicate inputs** (same text as the most recent entry) overwrite the existing top entry rather than creating a duplicate

---

## Closing the Drawer

- Clicking the **History button** again closes it
- Clicking **anywhere outside** the drawer closes it
- **Restoring an entry** closes it automatically

---

## Storage

- Uses `localStorage` to persist history across page refreshes
- Key: `json_reader_history`
- Value: JSON array of up to 10 entry objects

### Entry Schema

```json
{
  "input": "...",
  "output": "...",
  "timestamp": "2026-04-28T12:00:00.000Z",
  "settings": {
    "wrapWidth": 80,
    "fontSize": 13,
    "lang": ""
  }
}
```
