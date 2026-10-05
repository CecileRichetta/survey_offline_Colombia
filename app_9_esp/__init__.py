from otree.api import *
import csv
import os
import threading
from pathlib import Path

doc = """
Support for peace agreement provisions. 
"""

def treatment_other_check_g3_choices(player):
    import random
    shuffled = [(0, 'Grupos insurgentes'), (1, 'Ejército nacional')]
    fixed = [(998, "No sabe (no leer)"), (999, 'No responde (no leer)')]
    random.shuffle(shuffled)
    return shuffled + fixed

def treatment_other_check_g4_choices(player):
    import random
    shuffled = [(0, 'Grupos insurgentes'), (1, 'Ejército nacional')]
    fixed = [(998, "No sabe (no leer)"), (999, 'No responde (no leer)')]
    random.shuffle(shuffled)
    return shuffled + fixed

class C(BaseConstants):
    NAME_IN_URL = 'app_9_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PARTICIPATION_FEE = 30000
    # CHOICES
    CHOICE_PEACE_SUPPORT = [
        (0, "Para nada"), # Not at all
        (1, "Un poco"), # A little
        (2, "Algo"), # Somewhat
        (3, "Mucho"), # A lot
        (4, 'Completamente '), # Completely
        (998, "No sabe (no leer)"), # Don't know
        (999, "No responde (no leer)") # Prefer not to say
    ]
    CHOICE_NGO_NAME = [
        (0, "1. Asomujer y Trabajo Association (relacionado con el conflicto)"),
        (1, "2. Fundación Pies Descalzos (Educación y desarrollo infantil)"),
        (2, "3. TECHO Colombia (Vivienda y desarrollo comunitario)")
    ]
    NGO_CSV_NAMES = {
        0: "Asomujer y Trabajo",
        1: "Fundación Pies Descalzos",
        2: "TECHO Colombia",
    }
    HOPE_SCALE = [
        (0, "Muy desesperanzado"), # Very hopeless
        (1, "Desesperanzado"), # Hopeless
        (2, "Ni desesperanzado ni esperanzado"), # Neither hopeless nor hopeful
        (3, "Esperanzado"), # Hopeful
        (4, "Muy esperanzado"), # Very hopeful
        (998, "No sabe (no leer)"), # Don't know
        (999, "No responde (no leer)") # Prefer not to say
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    justice_provision_1 = models.IntegerField(
        label="9.1. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa?: perdón para todos los excombatientes ",
        # 9.1. Regarding the conflict, please tell me how much do you support the following initiative: Amnesty of all previous fighters.
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    military_provision_2 = models.IntegerField(
        label="9.2. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa: Un cese al fuego?",
        # 9.2. Regarding the conflict, please tell me how much do you support the following initiative: A ceasefire.
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    military_provision_3 = models.IntegerField(
        label="9.3. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa: Desarme y reintegración de los Excombatientes a la vida civil?",
        # 9.3. Regarding the conflict, please tell me how much do you support the following initiative: Disarmament and reintegration of previous fighters in civilian life.
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    military_provision_4 = models.IntegerField(
        label="9.4. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa: Desmilitarización de las regiones afectadas por el conflicto?",
        # 9.4. Regarding the conflict, please tell me how much do you support the following initiative: Demilitarization, of conflict-affected regions
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    political_provision_3 = models.IntegerField(
        label="9.5. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa: Diálogos nacionales de paz?",
        # 9.5. Regarding the conflict, please tell me how much do you support the following initiative: National peace talks.
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    political_provision_4 = models.IntegerField(
        label="9.6. Por favor, digame cuánto apoya al partido político comunes",
        # 9.7. Please tell me how much do you support the Communes political party
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    territorial_provision_2 = models.IntegerField(
        label="9.8. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa: Libertad cultural?",
        # 9.8. Regarding the conflict, please tell me how much do you support the following initiative: Cultural freedom.
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    territorial_provision_6 = models.IntegerField(
        label="9.9. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa: Autonomía regional/local?",
        # 9.9. Regarding the conflict, please tell me how much do you support the following initiative: Local regional autonomy.
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    territorial_provision_7 = models.IntegerField(
        label="9.10. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa: Distribución del poder a nivel local/regional en las regiones afectadas por el conflicto?",
        # 9.10. Regarding the conflict, please tell me how much do you support the following initiative: Local regional power-sharing in conflict-affected regions.
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    territorial_provision_9 = models.IntegerField(
        label="9.11. Con respecto al conflicto, por favor díganos, ¿qué tanto apoya la siguiente iniciativa: Desarrollo económico y social regional?",
        # 9.11. Regarding the conflict, please tell me how much do you support the following initiative: Regional economic and social development.
        choices=C.CHOICE_PEACE_SUPPORT,
        widget=widgets.RadioSelect,
        blank=False
    )
    ngo_binary = models.BooleanField(
        label="9.12. ¿Quiere dar parte de su cuota de participación?",
        # 9.10. Do you want to give part of your participation fee?
        choices=[
            (True, "Sí"),
            (False, "No")
        ],
        blank=False
    )
    ngo_amount = models.IntegerField(
        label="9.13. Si es así, ¿cuánto? (en COP)",
 #       widget=widgets.RadioSelect,
        min=0,
        max=30000,
        blank=True
    )
    ngo_name = models.IntegerField(
        label="9.14. ¿A qué ONG?",
        choices=C.CHOICE_NGO_NAME,
        widget=widgets.RadioSelect,
        blank=True
    )
    hope_check = models.IntegerField(
        label="9.15. ¿Qué tan esperanzado se siente en este momento sobre la posibilidad de un proceso de paz en Colombia "
              "entre el gobierno y los grupos armados que aún permanecen?",
        #
        choices= C.HOPE_SCALE,
        blank=False,
        widget=widgets.RadioSelect
    )
    treatment_other_check_g3 = models.IntegerField(
        label="9.16. Durante las actividades, jugaste con alguien que pertenece a grupos que comparten los objetivos perseguidos "
              "por las FARC durante el conflicto y un excombatiente, ya sea del ejército nacional o de un grupo insurgente. "
              "¿De qué bando crees que la otra persona era combatiente?",
        blank=False,
        widget=widgets.RadioSelect
    )
    treatment_other_check_g4 = models.IntegerField(
        label="9.16. Durante las actividades, jugaste con alguien que pertenece a grupos que se oponen a los objetivos perseguidos "
              "por las FARC durante el conflicto y un excombatiente, ya sea del ejército nacional o de un grupo insurgente. "
              "¿De qué bando crees que la otra persona era combatiente?",
        blank=False,
        widget=widgets.RadioSelect
    )

_ngo_lock = threading.Lock()

def update_ngo_totals(player):
    """Add the player's donation to the matching NGO's total in payment_ngo.csv."""
    # Only count real donations
    if not player.field_maybe_none('ngo_binary'):
        return
    amount = player.field_maybe_none('ngo_amount')
    ngo_id = player.field_maybe_none('ngo_name')
    if amount is None or ngo_id is None or amount <= 0 or amount == 997:
        return

    data_folder = Path("data_internal/tracking")
    csv_file_path = data_folder / "payment_ngo.csv"
    temp_file = csv_file_path.with_suffix('.tmp')
    data_folder.mkdir(parents=True, exist_ok=True)

    with _ngo_lock:
        try:
            # Start from zero for each NGO, then load existing totals
            totals = {name: 0 for name in C.NGO_CSV_NAMES.values()}
            if csv_file_path.exists():
                with open(csv_file_path, 'r', newline='', encoding='utf-8-sig') as f:
                    for row in csv.DictReader(f):
                        totals[row['ngo']] = int(float(row['total'] or 0))

            # Add this donation
            totals[C.NGO_CSV_NAMES[ngo_id]] += amount

            # Write to temp file, then replace the original
            with open(temp_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['ngo', 'total'])
                writer.writeheader()
                for name, total in totals.items():
                    writer.writerow({'ngo': name, 'total': total})
            os.replace(temp_file, csv_file_path)

        except Exception as e:
            if temp_file.exists():
                os.remove(temp_file)
            print(f"Erreur dans update_ngo_totals: {e}")

# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = [
        'justice_provision_1',
        'military_provision_2',
        'military_provision_3',
        'military_provision_4',
        'political_provision_3',
        'political_provision_4',
        'territorial_provision_2',
        'territorial_provision_6',
        'territorial_provision_7',
        'territorial_provision_9'
        ]

class Page2(Page):
    form_model = 'player'
    form_fields = [
        'ngo_binary',
        'ngo_amount',
        'ngo_name'
    ]
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.ngo_binary==True and player.ngo_amount !=997:
            participant.participation_fee = C.PARTICIPATION_FEE - player.ngo_amount
        else:
            participant.participation_fee= C.PARTICIPATION_FEE
        participant.total_compensation = participant.participation_fee + participant.payoff_games
    @staticmethod
    def error_message(player, values):
        # If they want to donate (ngo_binary == True), they must specify amount and NGO
        if values['ngo_binary'] == True:
            if values.get('ngo_amount') is None:
                return 'Por favor indique cuánto desea donar.'
            if values.get('ngo_name') is None:
                return 'Por favor seleccione una ONG.'
        raw = str(values.get('ngo_amount', '') or '').replace(',', '').replace(' ', '').replace("'",'')
        if raw == '':
            return  # let oTree's blank=False handle the empty case
        try:
            num = int(raw)
            if num % 100 != 0:
                return '9.9. Por favor, introduzca un múltiplo de 100 (p. ej., 100, 200, 300...).'
        except ValueError:
            return 'Por favor, introduzca un número entero válido.'
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.ngo_binary == True and player.ngo_amount != 997:
            participant.participation_fee = C.PARTICIPATION_FEE - player.ngo_amount
        else:
            participant.participation_fee = C.PARTICIPATION_FEE
        participant.total_compensation = participant.participation_fee + participant.payoff_games
        update_ngo_totals(player)

class Page3(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.treatment_other == 3:
            return [
                'hope_check',
                'treatment_other_check_g3'
            ]
        elif participant.treatment_other == 4:
            return [
                'hope_check',
                'treatment_other_check_g4'
            ]
        else:
            return ['hope_check']

page_sequence = [
    Page1,
    Page2,
    Page3
]
