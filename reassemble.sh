#!/bin/bash
# Reassemble split mp3 files back to their originals
# Usage: ./reassemble.sh

set -e

for dir in Klub100/*/; do
    for part in "$dir"*.mp3.part_aa; do
        [ -f "$part" ] || continue
        base="${part%.part_aa}"
        echo "Reassembling $base ..."
        cat "$base".part_* > "$base"
        rm "$base".part_*
    done
done

echo "Done!"
