# Sample recorder

## Requirements

* `gcc`
* `make`
* `python3`

## Deployment (first launch)

```bash
source deploy.sh
```

## Usage

```bash
# Step inside the virtual env
source env/bin/activate
# Record some samples
python3 sample_recorder.py
# Step outside the virtual env
deactivate
```

## Gotcha

The software needs access to an input file in `/dev/input` path. So we need to add the user to the `input` group.

```bash
sudo usermod -aG input $USER
```

The command is in the `deploy.sh` script and should be already executed after `source deploy.sh`. But you probably need to restart your session