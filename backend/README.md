# IMG Deduplication

## How to use

```sh
git clone https://
cd
# Install packages
pip install -e
```

## How it should work

1. Get all the file path recursively
2. Convert all extensions in lower case
3. Convert all HEIC into JPG or PNG
4. Compare the images
    1. Check the file shape
        - If ratio is different -> Skip
        - If resolution is different -> Load in same resolutions (decrease)
    2. Load the both images
    3. Compare the images
        - if same in N % --> move to duplicate dir

## How to run test

```sh
cd /app
pylint .
pytest .
```
