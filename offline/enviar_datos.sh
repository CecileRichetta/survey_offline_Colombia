#!/bin/bash
# Export the oTree data and upload it to SwitchDrive (Geneva team only).
# Once SwitchDrive has a verified copy, the files with personal
# information (payoffs, recall) are deleted from the tablet.
source "$(dirname "$(readlink -f "$0")")/config.sh"

c4p_ask_enumerator || exit 1

STAMP=$(date +%Y-%m-%d_%H%M%S)
ENUM=$(cat "$C4P_ID_FILE" 2>/dev/null)
OUTDIR="$C4P_UPLOAD_ROOT/$STAMP"

echo "ENVIAR DATOS"
echo "Código de encuestador: $ENUM"
echo

if [ -z "$ENUM" ]; then
  echo "ERROR: esta tablet no tiene código de encuestador."
  echo "Tome una foto de esta pantalla y envíela a su supervisor."
  exit 1
fi

# The export needs oTree running: start it if needed
c4p_start_otree
case $? in
  0) ;;
  2)
    echo "Esta versión necesita una base de datos nueva."
    echo "Con internet, vuelva al menú y escriba 3 (Actualizar)."
    exit 1 ;;
  *)
    echo "ERROR: la encuesta no pudo iniciar. Nada se ha perdido."
    echo "Tome una foto de esta pantalla y envíela a su supervisor."
    exit 1 ;;
esac

mkdir -p "$OUTDIR"
chmod 700 "$C4P_UPLOAD_ROOT"

echo "Preparando los datos..."
OUTFILE="$OUTDIR/otree_data_$STAMP.csv"
if ! curl -sS -f -H "otree-rest-key: $OTREE_REST_KEY" \
     -o "$OUTFILE" "$C4P_URL/api/export_wide"; then
  echo "ERROR: no se pudieron preparar los datos. Nada se ha perdido."
  echo "Tome una foto de esta pantalla y envíela a su supervisor."
  rm -rf "$OUTDIR"
  exit 1
fi

cd "$C4P_PROJECT" || exit 1
for f in data_internal/*/*.csv _static/data_external/treatment_balance.csv; do
  [ -f "$f" ] || continue
  cp "$f" "$OUTDIR/$(basename "$f" .csv)_$STAMP.csv"
done

# Also sends any earlier upload that failed (still waiting in the folder)
if c4p_send_waiting_uploads "$ENUM"; then
  c4p_delete_sent_personal_data "$OUTDIR" "_$STAMP"
  c4p_clear_waiting_uploads
  date "+%d/%m/%Y %H:%M" > "$C4P_LAST_UPLOAD_FILE"
  echo
  echo "ENVÍO COMPLETO. Los datos llegaron bien."
else
  echo
  echo "EL ENVÍO FALLÓ. Revise el internet y escriba 2 otra vez."
  echo "Nada se ha perdido: los datos esperan en la tablet."
  exit 1
fi
