from otree.api import *
import csv
import re
from datetime import datetime

doc = """
Consent form for Pilot Study

Elements
- app_1 form -> end of the study if participant does not app_1 

"""


class C(BaseConstants):
    NAME_IN_URL = 'app_1_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # PAYMENT INFO VARIABLES
    TEMPLATE_CONSENT_FORM_W1 = '_static/texts_SPANISH/consent_form_w1.html'
    DATA_TREATMENT_W1_LOC = 'data_internal/for_wave_2/'
    TEMPLATE_CONSENT_FORM_W2 = '_static/texts_SPANISH/consent_form_w2.html'
    # CONSTANTS
    TOKEN_ENDOWMENT = 4
    SURVEY_ORIGIN = [
        (1, "Muestra cartográfica"),
        (2, "Referidos")
    ]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    enumerator_id = models.StringField(
        label="Ingrese su identificador de encuestador", # enter your enumerator identifier
        blank=False
    )
    enumerator_name = models.StringField(
        label="Ingrese su nombre de encuestador",
        blank=False
    )
    supervisor_id = models.StringField(
        label="Ingrese su nombre de supervisor",
        blank=False
    )
    city = models.StringField(
        label="Ingrese su ciudad donde se esta realizando la encuesta:",
        blank=False
    )
    survey_origin = models.IntegerField(
        label="¿La encuesta proviene de la muestra cartográfica o de referidos?",
        choices=C.SURVEY_ORIGIN,
        blank=False
    )
    sector = models.StringField(
        label="Sector:",
        blank=True
    )
    seccion = models.StringField(
        label="Sección:",
        blank=True
    )
    manzana = models.StringField(
        label="Manzana:",
        blank=True
    )
    timestamp = models.StringField()
    consent = models.BooleanField(choices=[[True, 'Estoy dispuesto a participar en este estudio.'],
                                           [False, 'No estoy dispuesto a participar en este estudio.']],
                                  label='Confirmo que he entendido la información anterior y...',
                                  widget=widgets.RadioSelect)
    p_label = models.StringField()



# FUNCTIONS
def extract_participant_w1(p):
    participant = p.participant
    with open("data_internal/for_wave_2/participant_wave_1.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Participant_label'] == participant.label:
                participant.group = int(row['Participant_group'])
                participant.etv = int(row['Participant_etv'])
                participant.treatment_hope = int(row['Participant_treatment_hope'])
                participant.side_ultimatum = int(row['Participant_side_ultimatum'])
                participant.treatment_other = int(row['Participant_treatment_other'])
                break


def enumerator_id_error_message(player, value):
    if not re.fullmatch(r'[0-9]{4}', value.strip()):
        return 'Por favor ingrese 4 dígitos'


def supervisor_id_error_message(player, value):
    if not re.fullmatch(r'[0-9]{2}', value.strip()):
        return 'Por favor ingrese 2 dígitos'


# PAGES
class Page0(Page):
    pass

class Page1(Page):
    form_model = 'player'
    form_fields = [
        'enumerator_id',
        'enumerator_name',
        'supervisor_id',
        'city',
        'survey_origin',
        'sector',
        'seccion',
        'manzana'
    ]
    @staticmethod
    def error_message(player, values):
        if values['survey_origin'] == 1:
            errors = {}
            for f in ['sector', 'seccion', 'manzana']:
                if values[f] in (None, ''):
                    errors[f] = 'Este campo es obligatorio'
            if errors:
                return errors
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.participation_fee = 30000
        participant.supervisor = player.supervisor_id
        participant.enumerator = player.enumerator_id
        # For the monitoring dashboard (app_13). No personal data here.
        participant.vars['city'] = player.city.strip()
        participant.vars['sector'] = (player.field_maybe_none('sector') or '').strip()
        participant.vars['survey_origin'] = player.survey_origin


class Page2(Page):
    form_model = 'player'
    form_fields = ['consent']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        current_datetime = datetime.now()
        player.timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        participant = player.participant
        participant.vars['consent'] = player.consent
        participant.dropout = not player.consent
        player.p_label = participant.label
        if player.session.config['name']=="session_C4P_SPANISH_w2":
            participant.military_binary = 997
            extract_participant_w1(player)
        else:
            pass

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if not player.consent:
            participant = player.participant
            participant.dropout = True  # custom field in Player model
            participant.treatment_hope = 999
            participant.participation_fee = 0
            return upcoming_apps[-1]

page_sequence = [
    Page0, # welcome
    Page1, # enumerator identifier
    Page2 # consent form
]
