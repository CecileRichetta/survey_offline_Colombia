# Shared settings for the offline tablets (sourced by the other scripts).
# This repository is public: only put values here that are safe to be
# public. The oTree server only listens on the tablet itself (127.0.0.1),
# so the admin password and REST key below cannot be used from outside.
# NEVER put the SwitchDrive link password here: install.sh asks for it.

export OTREE_PRODUCTION=1
export OTREE_AUTH_LEVEL=STUDY
export OTREE_ADMIN_PASSWORD=C4P_colombia
export OTREE_REST_KEY=otree_rest_colombia

C4P_ROOT="$HOME/otree-experiments"
C4P_PROJECT="$C4P_ROOT/survey_offline_Colombia"
C4P_VENV="$C4P_ROOT/venv"
# Folder of these scripts inside the repository
C4P_SCRIPTS="$C4P_PROJECT/offline"
C4P_PORT=8000
C4P_URL="http://127.0.0.1:$C4P_PORT"

# Where the enumerator ID of this tablet is stored (set by install.sh)
C4P_ID_FILE="$HOME/.c4p_enumerator"

# SwitchDrive destination: the shared link to the C4P_Data folder
# (https://drive.switch.ch/index.php/s/<token>). The link only gives
# access to that folder. Its password is asked by install.sh.
C4P_REMOTE=swdrive
SWD_URL="https://drive.switch.ch/public.php/webdav/"
SWD_SHARE_TOKEN="oSnYi965MAQdHkH"

# Per-tablet secret key for oTree (created by run.sh, never in git)
C4P_KEY_FILE="$HOME/.c4p_secret_key"
# Database structure version installed on this tablet (see DB_VERSION)
C4P_DB_VERSION_FILE="$HOME/.c4p_db_version"

# Files waiting to be sent to SwitchDrive. This folder is private to
# Termux (other Android apps cannot read it, unlike Downloads).
# Each upload is a sub-folder; it is deleted once SwitchDrive has it.
C4P_UPLOAD_ROOT="$HOME/otree_uploads"

# Files with personal information (name, cedula, address, phone, email).
# They are deleted from the tablet once SwitchDrive has a verified copy;
# the survey creates them again (with their header) at the next interview.
C4P_PERSONAL_DATA_GLOBS=(
  "data_internal/payoffs/payoffs*.csv"
  "data_internal/for_wave_2/recall*.csv"
)

# Files written by the survey on the tablet. They are tracked in git,
# so install.sh tells git to leave the local copies alone on "git pull".
C4P_LOCAL_DATA=(
  data_internal/payoffs/payoffs.csv
  data_internal/payoffs/games_wave_1.csv
  data_internal/for_wave_2/recall.csv
  data_internal/for_wave_2/participant_wave_1.csv
  data_internal/tracking/interviews_per_group.csv
  data_internal/tracking/payment_ngo.csv
  _static/data_external/treatment_balance.csv
)

# Shortcuts in the home folder: ./run.sh ./upload.sh ./update.sh ./reset.sh
c4p_make_shortcuts() {
  local s
  for s in run upload update reset; do
    printf '#!/bin/bash\nexec bash "%s/%s.sh" "$@"\n' "$C4P_SCRIPTS" "$s" \
      > "$HOME/$s.sh"
    chmod +x "$HOME/$s.sh"
  done
}

# Send everything waiting in $C4P_UPLOAD_ROOT to SwitchDrive
# (C4P_Data/<enumerator ID>/<upload time>/) and check that SwitchDrive
# has every file. Returns 0 only if everything was sent and verified.
# The caller deletes the local copies afterwards (c4p_clear_waiting_uploads).
c4p_send_waiting_uploads() {
  local ENUM="$1"
  local DEST="$C4P_REMOTE:$ENUM/"
  [ -n "$(ls -A "$C4P_UPLOAD_ROOT" 2>/dev/null)" ] || return 0
  echo "Uploading to SwitchDrive..."
  rclone copy "$C4P_UPLOAD_ROOT" "$DEST" || return 1
  echo "Checking that SwitchDrive received every file..."
  rclone check "$C4P_UPLOAD_ROOT" "$DEST" --one-way || return 1
  return 0
}

c4p_clear_waiting_uploads() {
  rm -rf "${C4P_UPLOAD_ROOT:?}"/*
}

# Delete the personal-data files from the tablet, but only those that are
# identical to the copy just sent (a file that changed meanwhile, e.g. an
# interview finishing during the upload, is kept and sent next time).
# $1 = folder holding the sent copies, $2 = suffix added to the copies
c4p_delete_sent_personal_data() {
  local SENT="$1" SUFFIX="$2" pattern f name
  for pattern in "${C4P_PERSONAL_DATA_GLOBS[@]}"; do
    for f in $C4P_PROJECT/$pattern; do
      [ -f "$f" ] || continue
      name=$(basename "$f" .csv)
      if cmp -s "$f" "$SENT/${name}${SUFFIX}.csv"; then
        rm -f "$f"
      else
        echo "  (kept $(basename "$f"): it changed during the upload, it will be sent next time)"
      fi
    done
  done
}
