# Sample recorder

## Using Docker

### Requirements

* `docker`
* `docker-compose` (optional)

### Build

```bash
docker build --rm -t sample_recorder:latest .
```

### Run with Docker

```bash
docker run --rm -it --device "/dev/input/by-path/platform-i8042-serio-0-event-kbd" --volume `pwd`/sequence:/root/project/sequence sample_recorder:latest
```

### Run with Docker-compose

```bash
# Much simpler isn't it ?
docker-compose run --rm sampler
```

## Manual installation

### Requirements

* `gcc`
* `make`
* `python3`

### Deployment (first launch)

```bash
source deploy.sh
```

### Usage

```bash
# Step inside the virtual env
source env/bin/activate
# Record some samples
python3 sample_recorder.py
# Step outside the virtual env
deactivate
```

### Gotcha

The software needs access to an input file in `/dev/input` path. So we need to add the user to the `input` group.

```bash
sudo usermod -aG input $USER
```

The command is in the `deploy.sh` script and should be already executed after `source deploy.sh`. But you probably need to restart your session