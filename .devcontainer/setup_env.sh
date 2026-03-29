set -eu

cp test.env.sample test.env

sudo apt-get update
sudo apt-get install -y libltdl7 libkrb5-3 libgssapi-krb5-2

docker compose build
docker compose up -d

pip install -r dev_requirements.txt
