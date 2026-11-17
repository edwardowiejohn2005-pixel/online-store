# Online Shopping System

Product list, basket, stock checks, and local pending-payment orders. No payment integration. Stock is in-memory and resets when the app restarts.

## Run

Open a terminal in this folder and run:

```bash
python app.py
```

On Windows you may need `py app.py` instead. Requires Python 3.10+; no third-party packages.

## Tests

```bash
python -m unittest discover -v
```

The app creates local JSON files as needed; these should not be committed.
