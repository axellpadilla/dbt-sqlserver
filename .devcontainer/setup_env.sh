set -euo pipefail

cp test.env.sample test.env

if [ ! -f test.env ]; then
	cp test.env.sample test.env
fi

# Install uv in the container user environment.
pip install uv

# Use a workspace-local virtualenv so package installs do not fail on user permissions.
uv pip install -r dev_requirements.txt
source .venv/bin/activate
pre-commit install
