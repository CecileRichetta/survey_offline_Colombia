# C4P offline survey on an Android tablet

Enumerators follow the Spanish guide (PDF). They only use the menu that
opens with Termux and type a number. This page is for the support team.

## Installation (once per tablet, with internet, about 30 minutes)

1. Install **Termux from F-Droid** (not the Play Store):
   https://f-droid.org/en/packages/com.termux/
2. Open Termux, paste these four lines together and press **Enter**:

```
yes "" | pkg update -y; pkg install -y git &&
mkdir -p ~/otree-experiments && cd ~/otree-experiments &&
git clone https://github.com/CecileRichetta/survey_offline_Colombia &&
bash survey_offline_Colombia/offline/instalar.sh
```

3. When asked, paste the **SwitchDrive link password** given by the Geneva team
   (nothing is shown while pasting, this is normal).
4. Android settings → Apps → Termux → Battery → **Unrestricted**.

The installation can be run again safely: steps already done are skipped.

**Enumerator code:** it is not asked at installation, so tablets can be installed
before they are assigned. The enumerator types it the first time they use option
1 or 2 of the menu. After that the menu shows it. If you tried option 1 or 2 while
preparing a tablet, or a tablet changes hands, clear the code: type `0` in the menu, then
`rm ~/.c4p_enumerator`. Send the data first when a tablet changes hands, because the next upload
goes to the new code's folder.

## Final clean-up (once per tablet, after training, before fieldwork)

Needs internet. It is not in the menu, so enumerators cannot start it by accident.
Type `0` in the menu, then paste:

```
cd ~/otree-experiments/survey_offline_Colombia && git fetch && git checkout origin/HEAD -- offline/limpiar_tablet.sh && bash offline/limpiar_tablet.sh
```

Type `BORRAR` when asked. It does three things:

1. **Erases all data:** the database and every file written by the survey. A copy first
   goes to `C4P_Data/capacitacion/<code>/` on SwitchDrive, apart from the real data. If the
   copy can't be sent, nothing is deleted.
2. **Gets the latest version** from GitHub, including the clean data files.
3. **Erases the enumerator code.**

It must end with `LIMPIEZA COMPLETA`. Never run it once a tablet holds real interviews.

## Tablet data files in the repository

Keep these files clean in the repository: header only, with counts and totals at 0.
Once a tablet is in the field, **never change them again**: `git pull` (option 3) refuses
to update a tablet when they change, because the tablet's copies hold its data.
A tablet installed before a change to these files needs the final clean-up line above,
because option 3 will fail on it.

## Daily use: the menu

| Number | Script | What it does |
|---|---|---|
| 1 Iniciar encuesta | `iniciar.sh` | Starts oTree in the background if needed, creates the session if needed, opens the ID page in the browser. |
| 2 Enviar datos | `enviar_datos.sh` | Exports and sends the data to SwitchDrive, checks it, then deletes personal data from the tablet. Needs internet. |
| 3 Actualizar | `actualizar.sh` | Gets the latest survey version and restarts oTree. If a new database is needed, it runs `reiniciar_base.sh`. Needs internet. |
| 4 Ayuda | | Short help in Spanish. |
| 0 (not shown) | | Leaves the menu, for support. `./menu.sh` opens it again. |

`config.sh` holds the shared settings and is not launched by hand.

Nobody needs the oTree admin page on a tablet any more: the session is
created automatically (300 participants) through the local REST API.

## For Geneva: changing things on all tablets

Commit and push to GitHub, then ask the teams to use **3 Actualizar**.

- **Wave:** write `1` or `2` in `offline/OLA`. The tablet creates a new session
  of that wave at the next start. Earlier interviews stay in the database.
- **New or changed questions in the database:** add 1 to `offline/DB_VERSION`.
  "Actualizar" then asks for `SI`, sends and checks everything including the
  database file, and only then creates the empty database.
- **Never modify the tablet data files tracked in git** (list in `config.sh`):
  `git pull` would fail on the tablets. New files written by tablets must be
  listed in `.gitignore`.

## Names are not shown offline

The wave 2 name check exists only in the online version (`pid_check.csv`).
Tablets show the ID only, and never hold a list of names for wave 2: a lost
tablet must not expose participants. Do not copy `pid_check.csv` to a tablet.

If someone interviewed on a tablet in wave 1 will be interviewed online in
wave 2, add their ID and name to the server's `pid_check.csv` from the
`recall` files on SwitchDrive. Otherwise the online pop-up will not find them.

## What goes where

All data goes to SwitchDrive in
`C4P_Data/<enumerator code>/<date_time>/` (Geneva team only), one folder per
upload:

- `otree_data_<date_time>.csv`: anonymised oTree export (all interviews of the
  tablet so far).
- `payoffs_<date_time>.csv` and `recall_<date_time>.csv`: personal information,
  **only the interviews since the previous upload** (they are deleted from the
  tablet after each upload). Combine the files of all uploads; drop duplicate
  rows (same participant and date) that a failed upload can create.
- tracking (`interviews`, `interviews_per_group`, `payment_ngo`) and wave 2 files.
- `<date_time>_before_reset/`: full copy made before a new database
  (database file `db_<date_time>.sqlite3` and all CSV files).

Files waiting for upload are in the Termux-private folder `~/otree_uploads`.
oTree messages for troubleshooting are in `~/otree.log`.
