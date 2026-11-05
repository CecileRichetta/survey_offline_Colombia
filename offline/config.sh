# Shared settings for the offline tablets (sourced by the other scripts).
# This repository is public: only put values here that are safe to be
# public. The oTree server only listens on the tablet itself (127.0.0.1),
# so the admin password and REST key below cannot be used from outside.
# NEVER put the SwitchDrive link password here: instalar.sh asks for it.

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

# Room used for the interviews, and the page where the ID is entered
C4P_ROOM=C4PTHP_COL
C4P_ROOM_URL="$C4P_URL/room/$C4P_ROOM"
# Size of the session created automatically on the tablet
C4P_PARTICIPANTS=300
# Survey wave for all tablets (1 or 2). Geneva changes this file in the
# repository; tablets take it with "Actualizar".
C4P_WAVE_FILE="$C4P_SCRIPTS/OLA"
# Wave of the session that exists on this tablet
C4P_SESSION_WAVE_FILE="$HOME/.c4p_ola_sesion"

# Where the enumerator code of this tablet is stored. It is asked the
# first time the tablet is used (option 1 or 2 of the menu), not at the
# installation, because tablets are installed before being assigned.
C4P_ID_FILE="$HOME/.c4p_enumerator"
# Date of the last complete upload (shown in the menu)
C4P_LAST_UPLOAD_FILE="$HOME/.c4p_ultimo_envio"
# oTree messages, for the support team (no personal data)
C4P_LOG="$HOME/otree.log"

# SwitchDrive destination: the shared link to the C4P_Data folder
# (https://drive.switch.ch/index.php/s/<token>). The link only gives
# access to that folder. Its password is asked by instalar.sh.
C4P_REMOTE=swdrive
SWD_URL="https://drive.switch.ch/public.php/webdav/"
SWD_SHARE_TOKEN="oSnYi965MAQdHkH"

# Per-tablet secret key for oTree (created at first start, never in git)
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
# so instalar.sh tells git to leave the local copies alone on "git pull".
C4P_LOCAL_DATA=(
  data_internal/payoffs/payoffs.csv
  data_internal/payoffs/games_wave_1.csv
  data_internal/for_wave_2/recall.csv
  data_internal/for_wave_2/participant_wave_1.csv
  data_internal/tracking/interviews_per_group.csv
  data_internal/tracking/payment_ngo.csv
  _static/data_external/treatment_balance.csv
)

# ---------- Shortcuts and menu ----------

# Shortcuts in the home folder, and the menu that opens with Termux
c4p_make_shortcuts() {
  local s line rc
  for s in menu iniciar enviar_datos actualizar reiniciar_base; do
    printf '#!/bin/bash\nexec bash "%s/%s.sh" "$@"\n' "$C4P_SCRIPTS" "$s" \
      > "$HOME/$s.sh"
    chmod +x "$HOME/$s.sh"
  done
  # Tablets installed before the Spanish names: the old commands now
  # only explain what to do.
  for s in run upload update reset; do
    [ -f "$HOME/$s.sh" ] || continue
    printf '#!/bin/bash\necho "Este comando ya no se usa. Cierre Termux y vuelva a abrirlo: aparecera el menu."\n' \
      > "$HOME/$s.sh"
  done
  # Open the menu when Termux opens (only once per session)
  line='if [ -z "$C4P_MENU" ] && [ -t 0 ] && [ -f "$HOME/menu.sh" ]; then export C4P_MENU=1; bash "$HOME/menu.sh"; fi'
  for rc in "$HOME/.bashrc" "$HOME/.bash_profile"; do
    grep -qsF 'C4P_MENU=1' "$rc" || echo "$line" >> "$rc"
  done
}

# ---------- Enumerator code ----------

# Asks for the enumerator code if this tablet does not have one yet.
# Returns 1 if no code could be read.
c4p_ask_enumerator() {
  [ -s "$C4P_ID_FILE" ] && return 0
  local ENUM OK
  echo "Esta tablet todavía no tiene código de encuestador."
  while true; do
    read -r -p "Escriba su código de encuestador (4 dígitos): " ENUM || return 1
    if [[ ! "$ENUM" =~ ^[0-9]{4}$ ]]; then
      echo "Deben ser exactamente 4 dígitos."
      continue
    fi
    read -r -p "Usted escribió $ENUM. ¿Es correcto? Escriba s (sí) o n (no): " OK || return 1
    if [ "$OK" = "s" ] || [ "$OK" = "S" ]; then
      break
    fi
  done
  echo "$ENUM" > "$C4P_ID_FILE"
  echo
}

# ---------- oTree ----------

c4p_otree_running() {
  curl -s -o /dev/null --max-time 5 "$C4P_URL"
}

c4p_stop_otree() {
  pkill -f "otree prodserver" 2>/dev/null
  pkill -f "otree timeoutworker" 2>/dev/null
  local i
  for i in 1 2 3 4 5 6 7 8 9 10; do
    pgrep -f "otree prodserver" >/dev/null || return 0
    sleep 1
  done
  pkill -9 -f "otree prodserver" 2>/dev/null
  return 0
}

# True if the database on this tablet is too old for this survey version
c4p_db_outdated() {
  [ -f "$C4P_PROJECT/db.sqlite3" ] && \
    [ "$(cat "$C4P_SCRIPTS/DB_VERSION" 2>/dev/null)" != "$(cat "$C4P_DB_VERSION_FILE" 2>/dev/null)" ]
}

# Starts oTree in the background and waits until it answers.
# Returns 0 = running, 1 = did not start, 2 = needs a new database.
c4p_start_otree() {
  c4p_otree_running && return 0
  cd "$C4P_PROJECT" || return 1
  c4p_db_outdated && return 2
  [ -f db.sqlite3 ] || cat "$C4P_SCRIPTS/DB_VERSION" > "$C4P_DB_VERSION_FILE"
  # Secret key of this tablet, created once (the repository is public)
  if [ ! -s "$C4P_KEY_FILE" ]; then
    "$C4P_VENV/bin/python" -c "import secrets; print(secrets.token_urlsafe(32))" > "$C4P_KEY_FILE"
    chmod 600 "$C4P_KEY_FILE"
  fi
  # Ask Android not to put Termux to sleep (Termux only)
  command -v termux-wake-lock >/dev/null && termux-wake-lock
  echo "Iniciando la encuesta, espere un momento..."
  (
    source "$C4P_VENV/bin/activate"
    export OTREE_SECRET_KEY="$(cat "$C4P_KEY_FILE")"
    # Database file on disk: every answer is saved immediately
    export DATABASE_URL="sqlite:///db.sqlite3"
    nohup otree prodserver "127.0.0.1:$C4P_PORT" > "$C4P_LOG" 2>&1 < /dev/null &
  )
  local i
  for i in $(seq 1 90); do
    c4p_otree_running && return 0
    sleep 2
  done
  return 1
}

# Creates the session of the current wave if this tablet does not have it
# (the admin page is never needed). Existing interviews are kept.
c4p_ensure_session() {
  local WAVE CURRENT HAVE ANSWER
  WAVE=$(tr -d ' \r\n' < "$C4P_WAVE_FILE")
  case "$WAVE" in
    1|2) ;;
    *) echo "ERROR: el archivo OLA debe decir 1 o 2."; return 1 ;;
  esac
  CURRENT=$(curl -s -H "otree-rest-key: $OTREE_REST_KEY" "$C4P_URL/api/rooms" | \
    "$C4P_VENV/bin/python" -c "
import json, sys
rooms = json.load(sys.stdin)
print(next((r['session_code'] or '' for r in rooms if r['name'] == '$C4P_ROOM'), ''))") || return 1
  HAVE=$(cat "$C4P_SESSION_WAVE_FILE" 2>/dev/null)
  if [ -n "$CURRENT" ]; then
    # A session made by hand on an older tablet is kept
    [ -n "$HAVE" ] || { echo "$WAVE" > "$C4P_SESSION_WAVE_FILE"; return 0; }
    [ "$HAVE" = "$WAVE" ] && return 0
  fi
  ANSWER=$(curl -s -f -X POST -H "otree-rest-key: $OTREE_REST_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"session_config_name\":\"session_C4P_SPANISH_w$WAVE\",\"num_participants\":$C4P_PARTICIPANTS,\"room_name\":\"$C4P_ROOM\"}" \
    "$C4P_URL/api/sessions") || return 1
  echo "$ANSWER" | grep -q '"code"' || return 1
  echo "$WAVE" > "$C4P_SESSION_WAVE_FILE"
  echo "Encuesta lista (ola $WAVE)."
  return 0
}

# ---------- Sending data ----------

# Send everything waiting in $C4P_UPLOAD_ROOT to SwitchDrive
# (C4P_Data/<enumerator code>/<upload time>/) and check that SwitchDrive
# has every file. Returns 0 only if everything was sent and verified.
# The caller deletes the local copies afterwards (c4p_clear_waiting_uploads).
c4p_send_waiting_uploads() {
  local ENUM="$1"
  local DEST="$C4P_REMOTE:$ENUM/"
  [ -n "$(ls -A "$C4P_UPLOAD_ROOT" 2>/dev/null)" ] || return 0
  echo "Enviando a SwitchDrive..."
  rclone copy "$C4P_UPLOAD_ROOT" "$DEST" || return 1
  echo "Comprobando que SwitchDrive recibió todo..."
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
      fi
    done
  done
}
