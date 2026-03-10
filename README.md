# Super-Flash-Cards CLI

A command-line flashcard app using JSON-based card sets.
See what typical workflows would look like at the bottom of this file.

## Usage

```
python main.py [command]
```

## Commands

### `newset`
Create a new flashcard set. You will be prompted for a name. The new set is automatically selected.
```
python main.py newset
```

### `select`
Choose an existing set to study from. Lists all available sets and prompts for a selection.
```
python main.py select
```

### `create`
Add a new flashcard to the currently selected set. You will be prompted for a front and back.
The back supports multiple lines — finish input with **two blank lines**.
```
python main.py create
```

### `show`
Display a random flashcard (front side) from the selected set.
```
python main.py show
```

### `flip`
Reveal the back of the last card shown with `show`.
```
python main.py flip
```

### `delete`
Delete the currently selected set. Prompts for confirmation before removing.
```
python main.py delete
```

---

### `scrape`
Extract plain text from `web/page.html` and save it to `web/page.txt`, stripping all tags, scripts, and styles.
```
python main.py scrape
```
Requires: `pip install beautifulsoup4`

---

### `autogenerate`
Automatically generate a flashcard set from `web/page.txt` using the Claude API.
The generated set is saved to `sets/` and automatically selected.

```
python main.py autogenerate <output_name> [--model <model_id>]
```

#### Setup

1. Create an account and get an API key at [console.anthropic.com](https://console.anthropic.com)
2. Install the SDK:
   ```
   pip install anthropic
   ```
3. Set the `ANTHROPIC_API_KEY` environment variable:

   **Windows — Command Prompt (current session):**
   ```
   set ANTHROPIC_API_KEY=your_key
   ```
   **Windows — PowerShell (current session):**
   ```
   $env:ANTHROPIC_API_KEY="your_key"
   ```
   **Windows — permanent (restart terminal after):**
   ```
   setx ANTHROPIC_API_KEY "your_key"
   ```
   **Mac/Linux (current session):**
   ```
   export ANTHROPIC_API_KEY=your_key
   ```
   **Mac/Linux — permanent (add to `~/.bashrc` or `~/.zshrc`):**
   ```
   echo 'export ANTHROPIC_API_KEY=your_key' >> ~/.bashrc
   ```

4. Run:
   ```
   python main.py autogenerate my_set
   ```

---

#### No API key? Use ChatGPT manually

1. Run `python main.py scrape` to generate `web/page.txt`
2. Go to [chatgpt.com](https://chatgpt.com) and start a new chat
3. Attach `web/page.txt` using the paperclip icon
4. Send this prompt:
   > Extract all key educational concepts from the attached file and return ONLY a JSON array of flashcards, no explanation or markdown. Format: `[{"front": "Term", "back": ["Definition", "Detail", "Example"]}]`
5. Copy the JSON response and paste it into a new file in `sets/my_set.json`
6. Run `python main.py select` and choose your new set

---

## Typical Workflow

**Study an existing set:**
```
python main.py select       # Pick a set
python main.py show         # Show a random card
python main.py flip         # Reveal the answer
python main.py show         # Next card
```

**Generate a set from a webpage:**

First, save the page HTML from your browser:
1. Open the page in your browser and wait for it to fully load
2. Press `F12` to open DevTools
3. In the Elements tab, right-click the `<html>` tag at the top
4. Select **Copy → Copy outerHTML**
5. Paste into `web/page.html` and save

Then run:
```
python main.py scrape                              # Extract plain text
python main.py autogenerate my_set                 # Generate flashcards via Claude API
python main.py show                                # Start studying
```

**Generate a set from copy/pasted info**

Skip the scrape command, and paste info into web/page.txt

Then run:
```
python main.py autogenerate my_set                 # Generate flashcards via Claude API
python main.py show                                # Start studying
```

## PowerShell Aliases (Windows)

To avoid typing `python main.py` every time, load the session aliases with:

```powershell
. .\activate_aliases.ps1
```

The `. ` (dot-space) is required — it runs the script in your current session so the aliases persist. After loading, you can use shorthand commands:

| Alias | Command |
|---|---|
| `newset` | `python main.py newset` |
| `select-set` | `python main.py select` |
| `create` | `python main.py create` |
| `show` | `python main.py show` |
| `flip` | `python main.py flip` |
| `scrape` | `python main.py scrape` |
| `autogen <name> [--model x]` | `python main.py autogenerate ...` |
| `delete-set` | `python main.py delete` |

Aliases are temporary and only last for the current terminal session.

---

## Card Sets

Sets are stored as `.json` files in the `sets/` folder. Each card has a `front` (string) and a `back` (list of strings).

```json
[
  {
    "front": "STP",
    "back": [
      "Spanning Tree Protocol",
      "Eliminates layer 2 loops in a network."
    ]
  }
]
```
