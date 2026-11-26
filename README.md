# redborder-seaweedfs

Redborder RPM for [SeaweedFS](https://github.com/seaweedfs/seaweedfs) (Apache 2.0), the S3
object storage that replaces MinIO. `weed` is built from the source of a pinned release:
`packaging/rpm/Makefile` downloads the tarball and checks its sha256 before the build, and the
spec checks it again in `%prep`.

| | |
| --- | --- |
| Binary | `/usr/bin/weed` |
| Units | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer` (filer + S3 gateway) |
| Unit options | `/etc/default/seaweedfs-{master,volume,filer}` (`OPTIONS=...`) |
| Config | `/etc/seaweedfs` (`filer.toml`, `security.toml`, S3 identities) |
| Data | `/var/lib/seaweedfs/{master,volume,filer}` |
| System user | `seaweedfs` |

The package only installs the binary and the units. The cookbook `seaweedfs` writes the options
and the configuration files: a unit does not start until its `/etc/default/seaweedfs-*` exists.

## Upgrading SeaweedFS

1. Download the new release tarball and get its sha256:
   `curl -fsSL https://github.com/seaweedfs/seaweedfs/archive/refs/tags/<version>.tar.gz | sha256sum`
2. Change `WEED_VERSION`/`WEED_SHA256` in `packaging/rpm/Makefile` and `weed_version`/`weed_sha256`
   in `packaging/rpm/redborder-seaweedfs.spec`.
3. Check the `go` version in the release `go.mod` against `BuildRequires: golang`.
4. Bump `VERSION` and add a changelog entry.

Follow the SeaweedFS security advisories: https://github.com/seaweedfs/seaweedfs/security/advisories
