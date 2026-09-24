PY := .venv/bin/python

.PHONY: parts check archive setup

# Regenerate the current parts: rhino/max1100-*.3dm and stl/*.stl
parts:
	$(PY) cad/card_adapter.py
	$(PY) cad/comb.py

# card_adapter.V1 still reproduces Katie's Rhino model
check:
	$(PY) cad/check_v1.py

# Superseded parts, into stl/archive/
archive:
	$(PY) cad/archive/duct_card.py
	$(PY) cad/archive/box_fit_test.py
	$(PY) cad/archive/testprints_v1.py

setup:
	uv venv .venv
	uv pip install --python $(PY) -r requirements.txt
