# Security Review Lens (OWASP-flavored)

Run this pass on any change that touches input handling, auth, data access, file/network I/O, serialization, or dependencies. Each item lists **what to ask** and **what to grep for**. A security-relevant finding is almost always 🔴 Blocking.

> Principle: untrusted input is **everything that crosses a trust boundary** — HTTP params, headers, cookies, request bodies, file uploads, env in multi-tenant contexts, message-queue payloads, and responses from third-party services.

## 1. Secrets & credentials
- Ask: any hardcoded keys, tokens, passwords, connection strings? Secrets logged or echoed?
- Grep: `api[_-]?key`, `secret`, `password`, `token`, `AKIA[0-9A-Z]{16}`, `BEGIN (RSA|EC|OPENSSH) PRIVATE KEY`, `-----BEGIN`, `Authorization:` literals.
- Check: secrets come from env / secret manager, not source. `.env` / key files not committed.

## 2. Input validation at boundaries
- Ask: is every external input validated/normalized **at the boundary** before use (type, range, length, allow-list)?
- Watch: trusting client-supplied IDs, lengths, content-types, or redirect targets.
- Prefer allow-lists over deny-lists.

## 3. Injection
- **SQL/NoSQL:** parameterized queries / ORM bindings only. 🔴 on string-concatenated SQL.
  - Grep: `execute(` / `query(` with `f"`, `% `, `+ `, `.format(`, template literals interpolating user data.
- **Command:** no shell with interpolated input. Use arg arrays, never `shell=True` with user data.
  - Grep: `os.system`, `subprocess` + `shell=True`, `exec(`, `eval(`, backticks, `child_process.exec`.
- **XSS:** output encoded/escaped; no raw HTML from user input.
  - Grep: `dangerouslySetInnerHTML`, `innerHTML`, `v-html`, `| safe`, `mark_safe`, `render_template_string`.
- **Path traversal:** user-controlled file paths normalized + confined to a base dir.
  - Grep: `open(`, `readFile`, `os.path.join(<userinput>`, `../`.
- **Template / SSTI, LDAP, XML/XXE:** disable external entities; don't feed user input into templating engines.

## 4. AuthN / AuthZ
- Ask: is **every** new endpoint/handler/mutation behind authentication?
- Ask: is **authorization** checked per-resource (does *this* user own/can-access *this* object)? IDOR is the classic miss — sequential/guessable IDs without an ownership check.
- Watch: auth check in the UI but not the API; role check missing on a new admin action; JWT signature/expiry not verified.

## 5. SSRF & outbound requests
- Ask: does the server fetch a URL derived from user input? Restrict scheme/host; block internal ranges (169.254.169.254, 10.x, 127.x, metadata endpoints).
- Grep: `requests.get(<userinput>`, `fetch(<userinput>`, `urlopen`, webhook/callback URL handling.

## 6. Deserialization & parsing
- Ask: untrusted data deserialized into objects? 🔴 on unsafe deserializers.
- Grep: `pickle.loads`, `yaml.load` (without `SafeLoader`), `marshal`, `eval`-based JSON, Java `ObjectInputStream`, PHP `unserialize`.

## 7. Sensitive-data handling & logging
- Ask: are PII / secrets / tokens kept out of logs, error messages, and analytics?
- Ask: data encrypted in transit (TLS) and at rest where required? Right hashing for passwords (bcrypt/argon2, never MD5/SHA1)?
- Watch: full request/response dumps, stack traces leaking internals to clients.

## 8. Crypto & randomness
- Ask: security-sensitive randomness uses a CSPRNG (`secrets`, `crypto.randomBytes`), not `random` / `Math.random`?
- Watch: home-rolled crypto, ECB mode, hardcoded IV/salt, weak ciphers.

## 9. Dependencies & supply chain
- Ask: new dependency — is it reputable, maintained, pinned? Any known CVEs?
- Watch: lockfile changes pulling unexpected transitive bumps; typosquat-looking package names.

## 10. Web-app extras
- **CSRF:** state-changing requests protected (token / SameSite)?
- **Open redirect:** redirect target validated against an allow-list?
- **Rate limiting / DoS:** unbounded loops, unpaginated queries, zip-bombs, regex catastrophic backtracking (ReDoS) on user input?
- **CORS:** not `*` with credentials.
- **Security headers / cookie flags:** `HttpOnly`, `Secure`, `SameSite` on session cookies.

---
### Quick grep sweep (run after reading the diff)
```bash
grep_file pattern: "(eval\(|exec\(|os\.system|shell=True|pickle\.loads|yaml\.load\(|dangerouslySetInnerHTML|innerHTML|md5|sha1|api[_-]?key|secret|password|token|AKIA[0-9A-Z]{16})"
path: /home/user/workspace   (case_insensitive: true)
```
Treat each hit as a lead, not a verdict — confirm the data flow before flagging.
