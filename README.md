# Kachna Bot

Kachna Bot plays locally configured sound files through the host's PulseAudio-compatible audio server and provides Discord and KIS notifications. It does not generate speech. Speech/TTS is handled outside this repository; a host-side library can use the same `paplay` backend.

## Requirements

- Linux host with PulseAudio, or PipeWire with its PulseAudio-compatible server enabled.
- Docker Compose plugin.
- A Discord bot token and Spotify application credentials in `config.py`.
- KIS connection settings in `config.json`.

`paplay` uses the PulseAudio protocol. Compose passes the host's `pulse/native` socket into the container and uses the host PulseAudio cookie for authentication; it does not pass `/dev/snd` through or require a privileged container. This works with PipeWire when its PulseAudio compatibility socket is available at `$XDG_RUNTIME_DIR/pulse/native`.

## Recommended: run with Docker

Docker Compose is the preferred way to run Kachna Bot: it installs the locked dependencies, runs as a non-root user, and connects `paplay` to the host's PulseAudio-compatible socket. The host-based `uv` workflow below is optional and intended for development.

Create the ignored runtime configuration files from the checked-in examples, then edit them with your credentials:

```sh
cp config.py.template config.py
cp config.json.example config.json
```

Make sure the host audio server is running and that its socket and cookie exist. The default cookie path is `~/.config/pulse/cookie`; set `PULSE_COOKIE_FILE` if the host uses another path. Set host IDs so the container's non-root user can access the user-owned socket:

```sh
export LOCAL_UID="$(id -u)"
export LOCAL_GID="$(id -g)"
docker compose build
docker compose up -d
docker compose logs -f
```

Compose reads `XDG_RUNTIME_DIR` and `HOME` from the environment. The bot configuration and sounds are mounted into the container, while the named `app-data` volume persists user-level data such as Spotify's OAuth cache. Do not put credentials in the image.

## Development (optional)

Open the repository in the Dev Container. It uses the same Docker image and host audio socket, installs dependencies from `uv.lock`, and keeps the virtual environment and user data in Docker volumes. The mounted workspace supplies the source tree and local configuration.

For development outside the container:

```sh
uv sync --locked --all-groups
uv run pre-commit install
uv run python main.py
```

The host needs `paplay` (`pulseaudio-utils` on Debian/Ubuntu) and an active PulseAudio-compatible server.

## Checks and image publication

CI runs the pinned Ruff pre-commit hook across all tracked files and the available pytest suite. Every branch push publishes a GHCR image tagged with that branch name (for example, `master` publishes `:master`) after both checks pass. Pull requests do not publish images. Run the same checks locally with:

```sh
uv run pre-commit run --all-files
uv run pytest -q
```
