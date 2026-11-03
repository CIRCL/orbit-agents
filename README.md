# orbit-agents for Osquery build pipeline

[![orbit-agents](https://github.com/CIRCL/orbit-agents/actions/workflows/agents.yml/badge.svg)](https://github.com/CIRCL/orbit-agents/actions/workflows/agents.yml)

Will use fleetdm orbit to build:

- Linux Debian package .deb
- Windows installer files .msi
- MacOS package .pkg

## Builds and releases

The `VERSION` and `ARCH` variables in `.github/workflows/agents.yml` pin the
Fleet CLI used to build all three installers, with Fleet Desktop and scripts
enabled. This CLI pin is separate from the Orbit, osquery and Desktop component
versions selected through Fleet's update channels.

Pushes to `test` build and list the installers. Pushes to `main` also deploy them
to the package web host using `rsync --delete`. Only `main` loads the deployment
SSH key; test builds still require the enrollment secret.
Runs are serialized per branch so deployments cannot overlap. An active run
finishes before the next starts; only the newest pending run is retained.
Deployment trusts the Ed25519 host key pinned in the workflow. Verify replacement
keys independently before rotating that pin.

## Download website

`site/index.html` is the editable download-page template. Its navy, teal and mint
palette, typography and cards match nc3-infra's `deploy/mon01-pano/index.html`.
The page uses no external assets or libraries; downloads and checksum details
work without JavaScript.

After packaging, `scripts/build-download-site.py` discovers exactly one installer
per platform, then generates `packages/index.html` and `packages/SHA256SUMS` from
the actual filenames, sizes and SHA-256 hashes. A missing or ambiguous installer
fails the build before deployment. Test builds prepare the same website without
loading the deployment key or publishing it.

To preview using existing authorized installers in a private `packages/` folder:

```sh
python3 scripts/build-download-site.py packages/
python3 -m http.server 8000 --bind 127.0.0.1 --directory packages/
```

Open `http://127.0.0.1:8000/`. Keep installers and generated output out of Git.
Check desktop/mobile layout, keyboard navigation, all three download targets
and `SHA256SUMS` before publishing. This changes the download page; enrollment
still needs verification in Fleet after installation.

## Requirements

Local installer builds require Docker with privileged mount support, `cpio` and
`fleetctl` on `PATH`. Website generation uses Python 3.11 or newer and its
standard library; CI's Ubuntu 24.04 runner supplies Python.
