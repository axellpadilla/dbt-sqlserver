#!/bin/bash
set -euo pipefail

if [ ! -f test.env ]; then
	cp test.env.sample test.env
fi

sudo apt-get update
sudo apt-get install -y libltdl7 libkrb5-3 libgssapi-krb5-2

docker compose build
docker compose up -d

export UV_VENV_CLEAR=1
uv venv .venv
uv pip install --python .venv/bin/python -r dev_requirements.txt
.venv/bin/pre-commit install
