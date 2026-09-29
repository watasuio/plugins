# Sandbox MCP and Code Interpreter

These are higher-level runtimes built on the same sandbox lifecycle.

## MCP gateway inside a sandbox

Create a sandbox with an `mcp` map describing allowed stdio MCP servers. Watasu
starts them inside the isolated machine and returns a gateway URL/token for the
session.

```text
mcp server definition -> sandbox stdio process -> authenticated gateway URL
```

Pass server credentials through the documented server `env` field, sourced from
secret storage at runtime, not literal command arguments or committed MCP maps.
Treat the whole request and returned gateway token/URL as secret-bearing.
Expose only the servers and tools required by the agent's task.

This sandbox MCP gateway is different from the plugin's read-only customer-state
[Watasu MCP server](mcp.md).

## Code Interpreter

Official Python and TypeScript Code Interpreter packages default to the current
`code-interpreter` template and manage persistent language contexts. Contexts
can be created, listed, restarted, and removed.

For execution, supply either a language or an existing `context_id`, not both.
Read structured `results`, `logs`, and `error` independently. A successful HTTP
call can contain a language exception. Use stdout callbacks for progressive
feedback without treating a partial stream as final success.

## Safety

- Pass untrusted data through files or supported values, not source-string
  concatenation.
- Bound execution time and output.
- Apply explicit network policy.
- Retain context IDs only as long as stateful execution is needed.
- Destroy/pause the underlying sandbox according to lifecycle intent.
- Never return session, MCP, or signed-URL credentials in model-visible output.

[Handbook](index.md) · [SDK recipes](sdk-recipes.md) · [Lifecycle](sandbox-lifecycle.md)
