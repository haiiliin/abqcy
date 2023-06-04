set -ex
cd "$(dirname "$0")"
cd ..

# Generate the baseline images
pytest --mpl-generate-path=baseline
