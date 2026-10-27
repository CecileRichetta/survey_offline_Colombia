#!/bin/bash
# Export the oTree data and upload it to SwitchDrive (Geneva team only).
# Once SwitchDrive has a verified copy, the files with personal
# information (payoffs, recall) are deleted from the tablet.
source "$(dirname "$0")/config.sh"

STAMP=$(date +%Y-%m-%d_%H%M%S)
ENUM=$(cat "$C4P_ID_FILE" 2>/dev/null)
OUTDIR="$C4P_UPLOAD_ROOT/$STAMP"

echo "oTree Data Upload"
echo "Date: $STAMP"
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
chmod 700 "$C4P_UPLOAD_ROOT"

echo "Exporting oTree data..."
OUTFILE="$OUTDIR/otree_data_$STAMP.csv"
if ! curl -sS -f -H "otree-rest-key: $OTREE_REST_KEY" \
     -o "$OUTFILE" "$C4P_URL/api/export_wide"; then
  echo "ERROR: oTree export failed."
  rm -rf "$OUTDIR"
  exit 1
fi
echo "  $(($(wc -l < "$OUTFILE") - 1)) participant rows"

echo "Copying survey files..."
cd "$C4P_PROJECT" || exit 1
for f in data_internal/*/*.csv _static/data_external/treatment_balance.csv; do
  [ -f "$f" ] || continue
  cp "$f" "$OUTDIR/$(basename "$f" .csv)_$STAMP.csv"
done

# Also sends any earlier upload that failed (still waiting in the folder)
if c4p_send_waiting_uploads "$ENUM"; then
  echo "Removing personal information from the tablet..."
  c4p_delete_sent_personal_data "$OUTDIR" "_$STAMP"
  c4p_clear_waiting_uploads
  echo "Upload complete!"
else
  echo "UPLOAD FAILED. Check the internet connection"
  echo "and run ./upload.sh again. Nothing is lost: the files"
  echo "wait on the tablet and are sent with the next upload."
  exit 1
fi
