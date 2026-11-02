# Repository Guidelines

## Project Structure & Module Organization

This repository builds Fleet Orbit/osquery installers for Linux (`.deb`), macOS (`.pkg`), and Windows (`.msi`).

- `.github/workflows/agents.yml` defines downloads, packaging, and deployment.
- `README.md` describes the purpose and local prerequisites.
- `.gitignore` excludes common Node.js dependencies and temporary files.

There are no tracked application sources, tests, or assets. Do not incidentally commit local Fleet binaries, archives, or npm manifests. CI downloads its own CLI.

## Build, Test, and Development Commands

Run from the repository root. Use the workflow's `VERSION` and `ARCH`; update existing pins rather than adding duplicate versions. Local packaging requires Docker with privileged container support, `cpio`, and `fleetctl` on `PATH`. CI uses Ubuntu 24.04.

```sh
fleetctl --version
fleetctl package --type deb --fleet-url="$OSQUERY_URL" \
  --fleet-desktop --enable-scripts --enroll-secret="$OSQUERY_SECRET" \
  --fleet-certificate /etc/ssl/certs/ca-certificates.crt
```

These check the CLI version and build a Debian installer. Substitute `pkg` or `msi` for other targets. Set variables securely; adapt the CA bundle path outside Ubuntu.

## Coding Style & Naming Conventions

Read `README.md` and the workflow before editing. Preserve two-space YAML nesting, step-list alignment, uppercase environment variables, and multiline shell commands. Keep shared settings in `env`. No formatter or linter is configured. Keep changes focused and update documentation with behavior.

## Testing Guidelines

No test framework or coverage threshold exists. Run `git diff --check`, review YAML/shell syntax, and verify all three packaging steps for workflow changes. Pushes to `test` build and list installers without deploying; secrets and SSH setup are still required. Report commands, results, and skipped checks. Distinguish configuration, successful builds, deployment, and verified enrollment; date live observations.

## Commit & Pull Request Guidelines

Use `type: [scope] Summary` for new commit subjects:

- `new`: added capability or file.
- `chg`: changed configuration, versions, dependencies, or documentation.
- `fix`: corrected faulty behavior.

Use short scopes such as `yml`, `arch`, `ver`, `cfg`, `dep`, `gi`, or `chk`. Match the history's usual past-tense wording, e.g. `chg: [yml] Updated fleet version to 4.79.1`. Name the actual change; avoid vague subjects such as `Bump` or `Typo`. Keep each commit focused.

PRs should explain why, affected platforms, related issues, validation evidence, and recovery considerations. Review deployment impact before merging to `main`.

## Security & Deployment

Keep `OSQUERY_SECRET` and `SHARED_WEB_PRIV_KEY` in GitHub Actions secrets; exclude credentials from files and logs. Never commit credential-bearing installers. Pushes to `main` deploy with `rsync --delete`, removing destination-only files. Local validation does not authorize publishing or deployment.
