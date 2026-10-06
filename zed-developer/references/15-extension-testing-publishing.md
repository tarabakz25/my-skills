# Extension testing, publishing, and updates

## Preflight checklist

- [ ] Unique immutable ID; live registry collision checked.
- [ ] Manifest required fields complete; semver version intended.
- [ ] Only necessary files/capabilities included.
- [ ] Latest published compatible `zed_extension_api` selected.
- [ ] Accepted license file at extension root (or exact `path` root).
- [ ] Language/debug/MCP server not bundled.
- [ ] Theme/icon theme separated from other feature extensions.
- [ ] Local dev extension installed and thoroughly tested.
- [ ] Success, offline, missing-tool, denied-capability, corrupt-download, and unsupported-platform paths tested.
- [ ] No secrets, local paths, private URLs, generated build output, or unnecessary binaries committed.

Accepted licenses at baseline: Apache-2.0, BSD-2-Clause, BSD-3-Clause, CC-BY-4.0, GPLv3, LGPLv3, MIT, Unlicense, zlib. Re-check policy. A filename beginning `LICENSE`/`LICENCE` is inspected by CI.

## Local test loop

1. Validate TOML/JSON/schemas and `cargo fmt --check`, `cargo check`/tests as applicable.
2. Install Dev Extension from the extension root.
3. Start Zed with `--foreground` for Rust output; inspect `zed: open log`.
4. Exercise every declared feature and denied permission.
5. Test supported OS/arch or clearly narrow support/error messages.
6. Verify update/cache behavior without network.
7. Uninstall/reinstall dev override and test clean state.

## Registry PR

Fork/clone `zed-industries/extensions`, initialize submodules, then:

```bash
git submodule add https://github.com/OWNER/REPO.git extensions/<extension-id>
git add extensions/<extension-id>
```

Submodule URL must be HTTPS, public, and checked-out commit attached to a branch (not detached) at baseline.

Registry entry:

```toml
[extension-id]
submodule = "extensions/extension-id"
version = "0.0.1"
```

For a monorepo:

```toml
[extension-id]
submodule = "extensions/extension-id"
path = "packages/zed"
version = "0.0.1"
```

When using `path`, license must be at that path (symlink permitted by baseline policy). Run `pnpm sort-extensions`. Confirm registry version equals the extension manifest at the exact submodule commit.

Do not commit/push/create PR unless user explicitly requests. If committing via this environment, include `Co-Authored-By: cursoragent@cursor.com` and push as required by operator policy.

## Updating

1. Release/update the extension repository and manifest version.
2. Ensure target commit is on a branch and public.
3. Update registry submodule (`git submodule update --remote ...` or exact safe method).
4. Update matching registry version.
5. Re-run sorting/CI and full local regression, including migration from previous version.
6. Document breaking changes and rollback/pinning path.

## Failure modes

- CI license mismatch: use a canonical accepted license text at correct extension root.
- Version mismatch: compare `extension.toml` at submodule commit, not local working tree.
- Detached submodule: point to a commit reachable from a branch.
- SSH submodule URL: switch to public HTTPS.
- API compiles on `main` but not release: use published API compatible with target Zed.
- Works only on author's machine: remove hardcoded paths/env assumptions and test missing tool/offline.
- Reviewer rejects duplicate capability: contribute to existing extension first and document upstream attempt.

Official sources: [Developing Extensions](https://zed.dev/docs/extensions/developing-extensions), [Registry](https://github.com/zed-industries/extensions), [API compatibility](https://github.com/zed-industries/zed/tree/main/crates/extension_api).
