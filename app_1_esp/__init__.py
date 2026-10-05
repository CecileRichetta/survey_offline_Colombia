from otree.api import *
import csv
import random
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
    sector = models.StringField(
        label="Sector:",
        blank=True
    )
    seccion = models.StringField(
        label="Sección",
        blank=True
    )
    manzana = models.StringField(
        label="Manzana",
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
        'sector',
        'seccion',
        'manzana'
    ]
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.participation_fee = 30000
        participant.supervisor = player.supervisor_id
        participant.enumerator = player.enumerator_id
#        if player.session.config['name'] == "session_C4P_SPANISH_w1":
#            participant.age = player.module_0_age
#    def error_message(player, values):
#        if player.session.config['name'] == "session_C4P_SPANISH_w1":
#            # For actividad_otra (StringField)
#            if values['module_0_actividad'] == 6:
#                if not values.get('module_0_actividad_otra') or values['module_0_actividad_otra'].strip() == '':
#                    return 'Por favor indique la actividad otra.'
#            if len(values['appleid']) != 6:
#                return "Apple ID debe tener 6 caracteres."
#            if not values['appleid'].isdigit():
#                return "Apple ID debe contener solo números."



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
