# C4P offline survey on an Android tablet

Copy each grey box with its **copy button** (top-right of the box),
paste it into Termux and press **Enter**. Do not retype the commands.

## A. Installation (support team, once per tablet, with internet)

1. Install **Termux from F-Droid** (not the Play Store):
   https://f-droid.org/en/packages/com.termux/
   (allow "Install unknown apps" for your browser if Android asks).
2. Open Termux and run, one box at a time:

```
pkg update -y && pkg install -y git
```

```
mkdir -p ~/otree-experiments && cd ~/otree-experiments
```

```
git clone https://github.com/CecileRichetta/survey_offline_Colombia
```

```
bash survey_offline_Colombia/offline/install.sh
```

During the installation:

- If a question appears during the package update, press **Enter**.
- Tap **Allow** when Android asks for storage access.
- Type the **enumerator ID** of this tablet (e.g. `enumerator_01`).
- Paste the **SwitchDrive link password** given by the Geneva team
  (nothing is shown while you paste, this is normal).

The last lines should say `SwitchDrive connection OK` and
`Installation finished`.

3. Android settings → Apps → Termux → Battery → **Unrestricted**.

## B. Open the session (support team)

Start oTree (see C), then open `http://localhost:8000/` in the browser
and log in with user `admin`, password `C4P_colombia`.
Go to **Rooms → C4PTHP_COL**, choose wave 1 or wave 2, set the number of
participants (expected interviews + 10%) and click **Create**.
This is done once: the session survives restarts.

## C. Daily use

Termux has two sessions (swipe from the left edge to see them):

| Session | Command | What it does |
|---|---|---|
| [1] | `./run.sh` | Starts oTree. Leave it open. |
| [2] (NEW SESSION) | `./upload.sh` | Sends the data to Geneva (needs internet). |

**Is oTree running?** Open an offline link. If it fails, type
`./run.sh` in session [1].

**End of each day with offline interviews:** check oTree is running,
then in session [2] type `./upload.sh`. It must end with
`Upload complete!`. If it says `UPLOAD FAILED`, try again later with
internet: nothing is lost.

## D. Updating the survey (when Geneva asks)

```
./update.sh
```

Then stop oTree in session [1] (**Ctrl+C**) and start it again with
`./run.sh`. If the update says `UPDATE FAILED`, do not delete anything:
send a screenshot to the Geneva team.

## E. Tablets installed with the old protocol (once)

```
cd ~/otree-experiments/survey_offline_Colombia
```

```
git fetch && git checkout origin/master -- offline
```

```
bash offline/install.sh
```

```
cd ~ && ./update.sh
```

## What goes where

All data goes to SwitchDrive in
`C4P_Data/<enumerator ID>/<date>/` (Geneva team only):
`otree_data_<date>.csv` (anonymised oTree export), `payoffs_<date>.csv`
and `recall_<date>.csv` (personal information), plus the tracking and
wave 2 files. A copy stays on the tablet in
`Downloads/otree_upload_<date>`.
