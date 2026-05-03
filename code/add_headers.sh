#!/bin/bash
set -euo pipefail

HEADER=$(cat <<'EOF'
#!/usr/bin/env python3
# created by Group Supermodels in VT2026
# for the course Modelling of Complex Systems at Uppsala University
# Group Members:
# Juan Rodriguez
# Björk Lucas
# Vootele Mets
# Marco Malosti
# Sofia Fernandes
# David Weingut

EOF
)

while IFS= read -r -d '' f; do
    if grep -q "Supermodels" "$f"; then
        echo "Skipping $f"
        continue
    fi

    echo "Adding header to $f"
    tmp="$(mktemp)"
    {
        printf '%s\n\n' "$HEADER"
        cat "$f"
    } > "$tmp"
    mv "$tmp" "$f"
done < <(find . -type f -name '*.py' -not -path '*/__pycache__/*' -print0)