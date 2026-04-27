#!/bin/bash
# set -x
shopt -s globstar
HEADER=$(cat <<EOF
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
echo "will add header to each python file not containing 'Supermodels'"
echo "header is: $HEADER
END Of HEADER"
for f in ./**/*.py; do
    if [[ -f "$f" ]]; then
        if grep -q "Supermodels" "$f"; then
            echo "File $f is fine"
        else
            echo "File $f is either not a regular file or has no proper header, replacing"
            if command -v sponge >/dev/null 2>&1; then
                echo "$HEADER" | cat - "$f" | sponge "$f"
            else
                echo "sponge not available, will use manual backup"
                cp "$f" "$f.bak"
                echo "$HEADER" | cat - "$f.bak" >"$f"
            fi
        fi
    fi
done
