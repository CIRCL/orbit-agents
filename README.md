# orbit-agents for Osquery build pipeline

[![orbit-agents](https://github.com/CIRCL/orbit-agents/actions/workflows/agents.yml/badge.svg)](https://github.com/CIRCL/orbit-agents/actions/workflows/agents.yml)

Will use fleetdm orbit to build:

- Linux Debian package .deb
- Windows installer files .msi
- MacOS package .pkg

## Requirements

Requires Docker running with privileged mode to mount volumes, also requires
cpio and obviously the docker binary
