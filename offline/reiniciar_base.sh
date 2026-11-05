#!/bin/bash
# Start a new, empty oTree database on this tablet, for survey versions
# that add or change questions. EVERYTHING is first sent to SwitchDrive
# and checked; if that fails, nothing is deleted.
# Normally started by actualizar.sh, not by hand.
# (Everything is inside main() so bash reads the whole script first.)

main() {
  source "$(dirname "$(readlink -f "$0")")/config.sh"
  cd "$C4P_PROJECT" || exit 1

  local ENUM STAMP SAVE ANSWER d
  ENUM=$(cat "$C4P_ID_FILE" 2>/dev/null)
  if [ -z "$ENUM" ]; then
    echo "ERROR: esta tablet no tiene código de encuestador."
    echo "Tome una foto de esta pantalla y envíela a su supervisor."
    exit 1
  fi

  echo "Se enviarán TODOS los datos de esta tablet a SwitchDrive y"
  echo "después se creará una base de datos vacía."
  echo "Termine primero cualquier encuesta abierta: no podrá continuarla."
  read -r -p "Escriba SI (en mayúsculas) para continuar: " ANSWER
  if [ "$ANSWER" != "SI" ]; then
    echo "Cancelado. No se cambió nada."
    exit 1
  fi

  # 1. Stop oTree so the database does not change any more
  c4p_stop_otree

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
    echo
    echo "CANCELADO: el envío falló (¿internet?). No se borró nada."
    echo "Con internet, vuelva al menú y escriba 3 otra vez."
    exit 1
  fi

  # 4. New empty database
  source "$C4P_VENV/bin/activate"
  export DATABASE_URL="sqlite:///db.sqlite3"
  if ! otree resetdb --noinput; then
    echo
    echo "ERROR al crear la base de datos. Sus datos están en SwitchDrive."
    echo "Tome una foto de esta pantalla y envíela a su supervisor."
    exit 1
  fi
  cat "$C4P_SCRIPTS/DB_VERSION" > "$C4P_DB_VERSION_FILE"
  rm -f "$C4P_SESSION_WAVE_FILE"
  date "+%d/%m/%Y %H:%M" > "$C4P_LAST_UPLOAD_FILE"

  # 5. Personal data is on SwitchDrive: remove it from the tablet
  c4p_delete_sent_personal_data "$SAVE" "_$STAMP"
  c4p_clear_waiting_uploads
  c4p_make_shortcuts

  echo
  echo "Base de datos nueva lista. Todos los datos están en SwitchDrive."
}

main "$@"
exit
