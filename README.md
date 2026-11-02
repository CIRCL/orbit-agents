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

## Requirements

Requires Docker running with privileged mode to mount volumes, also requires
cpio and obviously the docker binary
