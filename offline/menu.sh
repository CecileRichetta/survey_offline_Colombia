#!/bin/bash
# The menu that opens with Termux. Enumerators only type a number.
# (Everything is inside main() so that "Actualizar" can replace this file.)

ayuda() {
  clear 2>/dev/null
  echo "AYUDA"
  echo
  echo "El navegador no abre la encuesta:"
  echo "  Vuelva a este menú y escriba 1."
  echo
  echo "Una encuesta se cortó:"
  echo "  Escriba 1 e ingrese el mismo identificador."
  echo "  La encuesta sigue donde se quedó."
  echo
  echo "Enviar datos no funciona:"
  echo "  Busque internet y escriba 2 otra vez. No se pierde nada."
  echo
  echo "Otro problema:"
  echo "  Tome una foto de la pantalla y envíela a su supervisor."
  echo "  No borre nada."
}

main() {
  source "$(dirname "$(readlink -f "$0")")/config.sh"
  local OPTION LAST
  while true; do
    clear 2>/dev/null
    echo "=============================="
    echo "      ENCUESTA C4P"
    echo "=============================="
    echo
    echo "  1  Iniciar encuesta"
    echo "  2  Enviar datos"
    echo "  3  Actualizar"
    echo "  4  Ayuda"
    echo
    LAST=$(cat "$C4P_LAST_UPLOAD_FILE" 2>/dev/null)
    echo "Último envío de datos: ${LAST:-ninguno todavía}"
    echo
    read -r -p "Escriba un número y presione Enter: " OPTION || exit 0
    echo
    case "$OPTION" in
      1) bash "$C4P_SCRIPTS/iniciar.sh" ;;
      2) bash "$C4P_SCRIPTS/enviar_datos.sh" ;;
      3) bash "$C4P_SCRIPTS/actualizar.sh"
         read -r -p "Presione Enter para volver al menú " _ || exit 0
         exec bash "$C4P_SCRIPTS/menu.sh" ;;   # the menu may have changed
      4) ayuda ;;
      0) echo "Saliendo del menú. Para volver, escriba:  ./menu.sh"; exit 0 ;;
      *) echo "Escriba solo 1, 2, 3 o 4." ;;
    esac
    echo
    read -r -p "Presione Enter para volver al menú " _ || exit 0
  done
}

main "$@"
exit
