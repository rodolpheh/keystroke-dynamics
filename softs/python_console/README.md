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