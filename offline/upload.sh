#!/bin/bash
# Export the oTree data and upload it to SwitchDrive (Geneva team only).
source "$(dirname "$0")/config.sh"

DATE=$(date +%Y-%m-%d)
ENUM=$(cat "$C4P_ID_FILE" 2>/dev/null)
OUTDIR="$HOME/storage/downloads/otree_upload_$DATE"
[ -d "$HOME/storage/downloads" ] || OUTDIR="$HOME/otree_upload_$DATE"

echo "oTree Data Upload"
echo "Date: $DATE"
echo "Enumerator: $ENUM"

if [ -z "$ENUM" ]; then
  echo "ERROR: no enumerator ID. Run the install again."
  exit 1
fi
if ! curl -s -o /dev/null "$C4P_URL"; then
  echo "ERROR: oTree is not running."
  echo "Start it in another session with ./run.sh"
  exit 1
fi

mkdir -p "$OUTDIR"

echo "Exporting oTree data..."
OUTFILE="$OUTDIR/otree_data_$DATE.csv"
if ! curl -sS -f -H "otree-rest-key: $OTREE_REST_KEY" \
     -o "$OUTFILE" "$C4P_URL/api/export_wide"; then
  echo "ERROR: oTree export failed."
  exit 1
fi
echo "  $(($(wc -l < "$OUTFILE") - 1)) participant rows"

echo "Copying survey files..."
for f in "${C4P_LOCAL_DATA[@]}"; do
  name=$(basename "$f" .csv)
  if [ -f "$C4P_PROJECT/$f" ]; then
    cp "$C4P_PROJECT/$f" "$OUTDIR/${name}_$DATE.csv"
  else
    echo "  (missing: $f)"
  fi
done

echo "Uploading all files to SwitchDrive..."
DEST="$C4P_REMOTE:$ENUM/$DATE/"
if rclone copy "$OUTDIR" "$DEST"; then
  echo "Upload complete!"
else
  echo "UPLOAD FAILED. Check the internet connection"
  echo "and run ./upload.sh again. Files are kept in:"
  echo "  $OUTDIR"
  exit 1
fi
