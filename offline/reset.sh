#!/bin/bash
# Start a new, empty oTree database on this tablet, for survey versions
# that add or change questions. EVERYTHING is first sent to SwitchDrive
# and checked; if that fails, nothing is deleted.
# (Everything is inside main() so bash reads the whole script first.)

main() {
  source "$(dirname "$0")/config.sh"
  cd "$C4P_PROJECT" || exit 1

  local ENUM STAMP SAVE ANSWER d
  ENUM=$(cat "$C4P_ID_FILE" 2>/dev/null)
  if [ -z "$ENUM" ]; then
    echo "ERROR: no enumerator ID. Run the install again."
    exit 1
  fi

  echo "This sends ALL the data of this tablet to SwitchDrive,"
  echo "then starts a new, empty oTree database."
  echo "Internet is needed. oTree will be stopped."
  read -r -p "Type RESET (capital letters) to continue: " ANSWER
  if [ "$ANSWER" != "RESET" ]; then
    echo "Cancelled. Nothing was changed."
    exit 1
  fi

  # 1. Stop oTree so the database does not change any more
  if pgrep -f "otree prodserver" >/dev/null; then
    echo "Stopping oTree..."
    pkill -f "otree prodserver"
    sleep 5
  fi

  # 2. Put a full copy in the upload folder
  STAMP=$(date +%Y-%m-%d_%H%M%S)
  SAVE="$C4P_UPLOAD_ROOT/${STAMP}_before_reset"
  mkdir -p "$SAVE"
  chmod 700 "$C4P_UPLOAD_ROOT"
  [ -f db.sqlite3 ] && cp db.sqlite3 "$SAVE/db_$STAMP.sqlite3"
  for f in data_internal/*/*.csv _static/data_external/treatment_balance.csv; do
    [ -f "$f" ] && cp "$f" "$SAVE/$(basename "$f" .csv)_$STAMP.csv"
  done
  # Copies left in Downloads by the old protocol (readable by other apps)
  for d in "$HOME"/storage/downloads/otree_upload_* "$HOME"/otree_upload_*; do
    [ -d "$d" ] || continue
    mkdir -p "$SAVE/old_upload_folders"
    mv "$d" "$SAVE/old_upload_folders/"
  done

  # 3. Send and verify. If it fails: stop, nothing deleted.
  if ! c4p_send_waiting_uploads "$ENUM"; then
    echo "RESET CANCELLED: the upload failed (internet?)."
    echo "Nothing was deleted. Run ./reset.sh again with internet."
    exit 1
  fi

  # 4. New empty database
  source "$C4P_VENV/bin/activate"
  export DATABASE_URL="sqlite:///db.sqlite3"
  if ! otree resetdb --noinput; then
    echo "RESET FAILED. Your data is safe on SwitchDrive."
    echo "Send a screenshot of this screen to the Geneva team."
    exit 1
  fi
  cat "$C4P_SCRIPTS/DB_VERSION" > "$C4P_DB_VERSION_FILE"

  # 5. Personal data is on SwitchDrive: remove it from the tablet
  c4p_delete_sent_personal_data "$SAVE" "_$STAMP"
  c4p_clear_waiting_uploads
  c4p_make_shortcuts

  echo
  echo "Reset complete. All data is on SwitchDrive."
  echo "Now: start oTree with ./run.sh (session 1), then create"
  echo "the session again (README, part B)."
}

main "$@"
exit
