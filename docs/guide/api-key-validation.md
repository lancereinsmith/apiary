# API Key Validation

Learn about API key validation and troubleshooting configuration issues.

## Overview

Apiary includes comprehensive validation for API key configurations to catch common mistakes like:

- Misspelled file paths
- Non-existent files  
- Empty or invalid key files
- Weak API keys (too short)
- Configuration errors

## Automatic Validation

Validation runs automatically:

1. **On startup** - Validates all API key configurations when the server starts
2. **On file load** - Validates when loading keys from files
3. **On demand** - Via the CLI validation command

## Validation CLI Command

Validate your configuration before starting the server:

```bash
uv run apiary validate-config
```

This checks:

- Global API keys in `config/settings.json`
- Endpoint-specific keys in `config/endpoints.json`
- All referenced key files exist, are readable, and contain valid keys
- Warns about weak or suspicious keys

See [API Key Examples](api-key-examples.md) for detailed validation output examples.

## Validation Rules

### File Path Detection

A string is treated as a file path if it:

- Contains a forward slash (`/`)
- Ends with `.txt` or `.keys`

Examples:

```json
// Treated as FILE paths:
"api_keys": "config/api_keys.txt"       ✅ File
"api_keys": "/etc/apiary/keys.txt"      ✅ File  
"api_keys": "keys/production.keys"      ✅ File

// Treated as STRING (comma-separated keys):
"api_keys": "key1,key2,key3"            ✅ String (multiple keys)
"api_keys": "abc123"                    ✅ String (single key)
```

### Errors vs Warnings

**Errors** (prevent loading):

- File path specified but file doesn't exist
- File exists but cannot be read
- Path exists but is a directory (not a file)
- Empty key source (no valid keys)

**Warnings** (allowed but flagged):

- API keys shorter than 8 characters (weak)
- API keys longer than 200 characters (suspicious)
- Empty key files (no valid keys found)

## Troubleshooting

### Issue: "File does not exist"

```text
ERROR: settings.api_keys: File 'config/api_keys.txt' does not exist.
```

**Solution:**

1. Check the file path spelling
2. Verify the file exists: `ls config/api_keys.txt`
3. Create the file if missing

### Issue: "Path exists but is not a file"

```text
ERROR: api_keys: Path 'config/' exists but is not a file
```

**Solution:**

- Specify the full file path: `config/api_keys.txt`, not `config/`

### Issue: "File contains no valid API keys"

```text
WARNING: settings.api_keys: File 'config/api_keys.txt' contains no valid API keys
```

**Solution:**

Check file contents. Each key should be on its own line:

```text
# Valid format
key1
key2
key3

# Invalid - all on one line
key1,key2,key3
```

### Issue: "Looks like a file path"

```text
ERROR: api_keys: File 'config/api_keys.tx' does not exist. 
If this is meant to be an API key, it looks like a file path.
```

**Solution:**

You misspelled the filename. The validator detected this looks like a file path (contains `/` or ends with extension) but the file doesn't exist.

Fix: `config/api_keys.tx` → `config/api_keys.txt`

### Issue: "Key is very short"

```text
WARNING: api_keys: Key 'test123' is very short (less than 8 characters).
```

**Solution:**

Use stronger API keys. See [API Key Examples](api-key-examples.md#generating-secure-keys) for secure key generation methods.

## File Format

Key files should follow this format:

```text
# Comments start with #
# One key per line
# Empty lines are ignored

key1-actual-value-here
key2-another-value
key3-third-value

# More comments
key4-fourth-value
```

**Don't use:**

```text
# ❌ Wrong - comma-separated (this is for JSON, not files)
key1,key2,key3

# ❌ Wrong - JSON format
{"keys": ["key1", "key2"]}
```

## Testing Your Configuration

### 1. Validate Configuration

```bash
uv run apiary validate-config
```

### 2. Start Server in Debug Mode

The server logs validation results on startup:

```bash
uv run apiary serve --reload
```

Watch for:

```text
INFO: Application starting up...
INFO: Validating API key configurations...
INFO: settings.api_keys: File 'config/api_keys.txt' contains 3 key(s)
WARNING: endpoints[/api/test].api_keys: Key 'test' is very short...
INFO: ✅ All API key configurations are valid
```

### 3. Test Authentication

Try accessing a protected endpoint:

```bash
# Should succeed with valid key
curl -H "X-API-Key: your-key-here" http://localhost:8000/auth/status

# Should fail with invalid key
curl -H "X-API-Key: wrong-key" http://localhost:8000/auth/status
```

## Best Practices

### 1. Use Absolute Paths in Production

```json
{
  "api_keys": "/etc/apiary/production_keys.txt"
}
```

### 2. Set Proper File Permissions

```bash
chmod 600 config/api_keys.txt
```

### 3. Monitor Validation Logs

Check logs after file updates:

```text
INFO: API key file modified: config/api_keys.txt
INFO: Reloaded 5 API key(s) from config/api_keys.txt
```

## Next Steps

- [API Key Examples](api-key-examples.md) - API key configuration examples
- [Authentication Guide](authentication.md) - Learn about API key authentication
- [Configuration Guide](../getting-started/configuration.md) - Complete configuration reference
- [CLI Reference](../reference/cli.md) - All CLI commands
