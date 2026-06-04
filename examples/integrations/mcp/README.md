# MCP client integration

Browser Use can run as a local Model Context Protocol (MCP) server for AI clients that support MCP tools.
Use this mode when an external model or coding agent should make the decisions while Browser Use provides browser I/O.

```bash
uvx --from 'browser-use[cli]' browser-use --mcp
```

## Client configuration

For clients that accept MCP JSON configuration:

```json
{
  "mcpServers": {
    "browser-use": {
      "command": "uvx",
      "args": ["--from", "browser-use[cli]", "browser-use", "--mcp"]
    }
  }
}
```

For local development from a checkout, point the client at the repository:

```json
{
  "mcpServers": {
    "browser-use-local": {
      "command": "uv",
      "args": ["--directory", "/path/to/browser-use", "run", "browser-use", "--mcp"]
    }
  }
}
```

The direct browser-control tools do not require an LLM API key.
Configure an LLM API key only if you plan to use `retry_with_browser_use_agent` or AI-powered extraction.

## Tool workflow

1. Navigate with `browser_navigate`.
2. Inspect with `browser_get_state`.
3. Interact with indices from the state output using `browser_click` and `browser_type`.
4. Use screenshots when custom controls or visual layout matter.
5. Clean up with `browser_close_all`.

For custom dropdowns or controls that do not open by element index, coordinate clicks may be necessary.
Use screenshot dimensions from `browser_get_state(include_screenshot=true)` to choose coordinates.

## Validation checklist

Use harmless test pages and fake values first.

- Open a static page and confirm `browser_get_state` returns URL, title, viewport, and interactive elements.
- Fill a simple text input with fake data and verify it appears visually.
- Open a custom dropdown and verify its options become visible in state output.
- Select a non-sensitive placeholder option and verify it sticks.
- Take a screenshot before and after interaction when testing a new site.
- Do not click save, submit, purchase, send, or next-step buttons unless that is the explicit goal.
- Close sessions with `browser_close_all` after tests.

## Safety notes

- Treat browser state, screenshots, form values, and cookies as sensitive.
- Prefer disposable profiles for unknown sites.
- Avoid using real financial, medical, legal, or account credentials during automation tests.
- Use domain restrictions in browser profile config when delegating broad tasks to an AI client.
- Keep client-specific secrets and local paths out of committed examples.
