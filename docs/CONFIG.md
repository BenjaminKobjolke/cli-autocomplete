# Configuration (`config.json`)

The tool reads its configuration from `config.json` in the project root (next to
`clicomplete.py`). The file is **gitignored** because its contents are machine-specific;
a committed template lives at `config.json.example`.

## First-time setup

Copy the template and adjust it, or let the tool manage it for you:

```bash
copy config.json.example config.json
```

You normally never edit the file by hand — the CLI manages it:

```bash
auto --add "C:\Your\Scripts"   # add a directory
auto --add .                   # add the current directory
auto --list                    # show configured directories
auto --delete 1                # remove by list index
auto --delete "C:\Your\Scripts"  # remove by path
```

If `config.json` does not exist, the tool creates an empty one on first run.

## Keys

| Key     | Type       | Required | Description |
|---------|------------|----------|-------------|
| `paths` | `string[]` | yes      | Absolute directories searched for executable scripts/commands in the first interactive prompt. Searched in order; all entries are offered for completion. |

### `paths`

- Each entry must be an **absolute path** to a directory. Entries are normalized
  (resolved) when added via `--add`; duplicates are rejected.
- In JSON, backslashes must be escaped: `"C:\\Your\\Scripts"`.
- Directories that no longer exist are silently skipped during completion — they stay
  in the config until removed with `--delete`.
- Only the directory's direct children are offered for completion (no recursion).

## Example

```json
{
  "paths": [
    "C:\\Your\\Scripts",
    "D:\\Another\\ScriptFolder"
  ]
}
```

## Related behavior

- A corrupt `config.json` (invalid JSON) is treated as empty; the error is logged to
  `logs/cli_complete.log`.
- With no paths configured, the tool prints quick-start instructions and exits.
