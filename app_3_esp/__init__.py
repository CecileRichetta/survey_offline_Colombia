from otree.api import *
import random
import csv

doc = """
Questions military service and exposure to violence"""


class C(BaseConstants):
    NAME_IN_URL = 'app_3_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # EXTERNAL DATA
    DATA_TREATMENT_LOC = '_static/data_external/treatment_balance.csv'
    # CHOICES IN VARIABLES
    UNIT_TIME = [
        (1, ""),
        (2, ""),
        (3, ""),
        (4, ""),
        (999, "")
    ]
    BINARY_ANSWER = [
        (1, "Sí"),  # Yes
        (0, "No"), # No
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    BINARY_SKIP = [
        (1, "Sí"),
        (0, "No"),
        (999, "No responde (no leer)")
    ]
    BINARY_ANSWER_NA = [
        (1, "Sí"),  # Yes
        (0, "No"), # No
        (997, "No aplica (no leer)"), # Not applicable
        (999, "No responde (no leer)") # Prefer not to say
    ]
    CONSCRIPTION = [
        (0, "Fui voluntariamente"), # Join voluntarily
        (1, "Pasé el sorteo del servicio militar"), # Draft lottery
        (999, "No responde (no leer)") # Prefer not to say
    ]
    SUBREGION_COLOMBIA = [
        (1, "Antioquia"),  #
        (2, "Atlántico"),  #
        (3, "Bogotá D.C."),  #
        (4, "Bolívar"),  #
        (5, "Boyacá"),  #
        (6, "Caldas"),
        (7, "Caquetá"),  #
        (8, "Cauca"),  #
        (9, "Cesar"),  #
        (10, "Córdoba"),
        (11, "Cundinamarca"),
        (12, "Chocó"),
        (13, "Huila"),
        (14, "Guajira"),
        (15, "Magdalena"),
        (16, "Meta"),
        (17, "Nariño"),
        (18, "Norte de Santander"),
        (19, "Quindío"),
        (20, "Risaralda"),
        (21, "Santander"),
        (22, "Sucre"),
        (23, "Tolima"),
        (24, "Valle del Cauca"),
        (25, "Arauca"),
        (26, "Casanare"),
        (27, "Putumayo"),
        (28, "San Andrés y Providencia"),
        (29, "Amazonas"),
        (30, "Guainía"),
        (31, "Guaviare"),
        (32, "Vaupés"),
        (33, "Vichada"),
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    MONTH = [
        (1, "Enero"),
        (2, "Febrero"),
        (3, "Marzo"),
        (4, "Abril"),
        (5, "Mayo"),
        (6, "Junio"),
        (7, "Julio"),
        (8, "Agosto"),
        (9, "Septiembre"),
        (10, "Octubre"),
        (11, "Noviembre"),
        (12, "Diciembre"),
        (998, "No sabe (no leer)"),  # Don't know
        (999, "No responde (no leer)") # Prefer not to say
    ]
    MILITARY_DUTY = [
        (0,'Tareas de seguridad nacional (puestos de control y controles de carretera; unidades de patrullaje; operaciones de rodeamiento y registro; seguridad a docentes y monjes; aplicación de la Ley Marcial y el Decreto de Emergencia)'),
        # National security duties (checkpoints and roadblocks; patrol units; surround-and-search operations; security for teachers and monks; enforcing Martial Law and the Emergency Decree)
        (1, 'Tareas de asuntos cívicos (ayuda en desastres; reparaciones de viviendas; proyectos de voluntariado)'),
        # Civic affairs duties (disaster relief; home repairs; royal volunteer projects)
        (2,'Servicios internos en las tareas de las unidades militares (limpieza; jardinería; cocina; mantenimiento de vehículos; conducción; trabajo administrativo y papeleo; tareas de guardia dentro de recintos; asistentes de oficiales militares)'),
        # Internal services in military units duties (cleaning; gardening; cooking; vehicule maintenance; driving; clerical work and paperwork; guard duties within compounds; military officers' aides)
        (999, 'No responde (no leer)')  # Prefer not to say
    ]
    SCALE_EMPHASIS = [
        (0, "Nada"), # None
        (1, "Algo"), # Some
        (2, "Mucho"), # A lot
        (998, "No sabe (no leer)"),  # Don't know
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    SCALE_ETV = [
        (0, "Raramente"), # Rarely
        (1, "Frecuentemente"), # Often
        (999, "No responde (no leer)")  # Prefer not to say
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # MILITARY SERVICE
    military_binary = models.IntegerField(
        label="3.1. ¿Usted prestó el servicio militar?",
        # 3.1. Did you do your military service?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelect,
        blank=False
    )
    # QUESTIONS MILITARY
    conscription_binary = models.IntegerField(
        label="3.1.2. Si es así, ¿cómo ingresó?",
        # How did you get involved?
        choices=C.CONSCRIPTION,
        widget=widgets.RadioSelect,
        blank=False
    )
    military_tasks = models.IntegerField(
        label="3.1.3. ¿Cuáles fueron sus principales funciones durante su periodo de servicio militar?",
        # Main military tasks
        choices=C.MILITARY_DUTY,
        widget=widgets.RadioSelect,
        blank=False
    )
    military_province_main = models.IntegerField(
        label="3.1.4. ¿En qué departamento estuvo principalmente asignado?",
        # 3.1.4. In which subregion were you primarily located during your time in the LRA?
        choices=C.SUBREGION_COLOMBIA,
        blank=False
    )
    maindeployment_start_year = models.IntegerField(
        label="3.1.5. ¿En qué año estuvo asignado en ese departamento?",
        # 3.1.5. In which year did you start to be in that subregion?
        choices=[
            [999, "No responde (no leer)"],
            *[[y, str(y)] for y in range(1989,1996)]
        ],
        blank=False
    )
    maindeployment_start_month = models.IntegerField(
        label="3.1.6. Mes de inicio:",
        #in which starting month?
        choices=C.MONTH,
        blank=False
    )
    maindeployment_length = models.IntegerField(
        label="3.1.7. ¿Cuánto tiempo estuvo asignado en ese departamento (número de meses)?",
        min=1,
        max=24,
        # How long were you in that region with the LRA (number of months)?
        blank=False
    )
    deployment_second = models.IntegerField(
        label="3.1.8. ¿Alguna vez estuvo asignado en otro departamento?",
        # Were you deployed in any other province?
        choices=C.BINARY_SKIP,
        widget=widgets.RadioSelect,
        blank=False
    )
    military_province_second = models.IntegerField(
        label="3.1.9. Si es así, ¿en qué departamento estuvo asignado?",
        # If yes, in which province were you deployed?
        choices=C.SUBREGION_COLOMBIA,
        blank=False
    )
    seconddeployment_start_year = models.IntegerField(
        label="3.1.10. ¿Desde qué año estuvo asignado en ese departamento?",
        # In which YEAR were you deployed in this province?
        choices=[
            [999, "No responde (no leer)"],
            *[[y, str(y)] for y in range(1989,1996)]
        ],
        blank=False
    )
    seconddeployment_start_month = models.IntegerField(
        label="3.1.11. Mes de inicio :",
        # 3.1.11. In which starting month:
        choices=C.MONTH,
        blank=False
    )
    seconddeployment_length = models.IntegerField(
        label="3.1.12. ¿Cuánto tiempo estuvo asignado en ese departamento (número de meses)?",
        # How long were you been stationed in that subregion (number of months)?
        min=0,
        max=24,
        blank=False
    )
    military_socialization_1 = models.IntegerField(
        label="3.1.13. Durante su tiempo en el ejército, ¿en qué medida se hacía énfasis en el respeto por la autoridad?",
        #
        choices=C.SCALE_EMPHASIS,
        widget = widgets.RadioSelect,
        blank=False
    )
    military_socialization_2 = models.IntegerField(
        label="3.1.14. Durante su tiempo en el ejército, ¿cuánta importancia se le daba a comprender las amenazas dentro del país en ese momento?",
        #
        choices=C.SCALE_EMPHASIS,
        widget = widgets.RadioSelect,
        blank=False
    )
    military_socialization_3 = models.IntegerField(
        label="3.1.15. Durante su servicio militar, ¿hasta qué punto podía contar con la ayuda de otros reclutas?",
        # During your service, how much could you count on your peers for support?
        choices=C.SCALE_EMPHASIS,
        widget = widgets.RadioSelect,
        blank=False
    )
    # QUESTIONS NON-MILITARY
    noncombatant_geography_main = models.IntegerField(
        label="3.2.1. Entre 1989 y 1996, ¿en qué departamento residió principalmente?",
        # 3.2.1. Between 1989 amd 1996, in which subregion did you primarily reside?
        choices= C.SUBREGION_COLOMBIA,
        blank=False
    )
    noncombatant_geography_main_start_year = models.IntegerField(
        label="3.2.2. ¿En qué año vivió en ese departamento?",
        # In which period did you reside in this province?
        choices=[
            [999, "Prefer not to answer"],
            *[[y, str(y)] for y in range(1970,1996)]
        ],
        blank=False
    )
    noncombatant_geography_main_start_month = models.IntegerField(
        label="3.2.3. Mes de inicio:", # start month
        choices=C.MONTH,
        blank=False
    )
    noncombatant_geography_main_end_year = models.IntegerField(
        label="3.2.4. ¿Hasta qué año?",
        # 3.2.3. Until what year?:
        choices=[
            [999, "No responde (no leer)"],
            *[[y, str(y)] for y in range(1989,2026)]
        ],
        blank=False
    )
    noncombatant_geography_main_end_month = models.IntegerField(
        label="3.2.5. Mes final: ", # end month
        choices=C.MONTH,
        blank=False
    )
    noncombatant_geography_second_b = models.IntegerField(
        label="3.2.6. Entre 1989 y 1996, ¿vivió en algun otro departamento?",
        # During that period, did you also live in another province?
        choices= C.BINARY_SKIP,
        widget=widgets.RadioSelect,
        blank=False
    )
    noncombatant_geography_second = models.IntegerField(
        label="3.2.7. Si es así, ¿en qué departamento vivió?",
        # If yes, in which province did you also reside?
        choices= C.SUBREGION_COLOMBIA,
        blank=False
    )
    noncombatant_geography_second_start_year = models.IntegerField(
        label="3.2.8. ¿En qué año vivió en ese departamento?",
        # In which period did you reside in this province?
        choices=[
            [999, "Prefer not to answer"],
            *[[y, str(y)] for y in range(1970,1996)]
        ],
        blank=False
    )
    noncombatant_geography_second_start_month = models.IntegerField(
        label="3.2.9. Mes de inicio:",
        choices=C.MONTH,
        blank=False
    )
    noncombatant_geography_second_end_year = models.IntegerField(
        label="3.2.10. ¿Hasta qué año?",
        # Buddhist era end year:
        choices=[
            [999, "No responde (no leer)"],
            *[[y, str(y)] for y in range(1989,2026)]
        ],
        blank=False
    )
    noncombatant_geography_second_end_month = models.IntegerField(
        label="3.2.11. Fin de mes: ",
        choices=C.MONTH,
        blank=False
    )
    # QUESTIONS EXPOSURE TO VIOLENCE
    etv_bi_1 = models.IntegerField(
        label="3.3. ¿Alguna vez fue atacado o emboscado por grupos armados durante un conflicto?",
        # … were you ever ambushed by combatants of the conflict or forced to hide during the confrontation?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_1 = models.IntegerField(
        label="3.4. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_2 = models.IntegerField(
        label="3.5. ¿Alguna vez fue amenazado por grupos armados durante un conflicto?",
        # … were you ever threatened by combatants of the conflict?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_2 = models.IntegerField(
        label="3.6. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_3 = models.IntegerField(
        label="3.7. ¿Alguna vez se quedó sin comida o sin techo?",
        # … were you left without food or shelter?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_3 = models.IntegerField(
        label="3.8. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_5_1 = models.IntegerField(
        label="3.9. ¿Alguna vez fue herido físicamente, golpeado o torturado por un grupo armado durante un conflicto?",
        # … were you ever physically injured, subject to beating(s) to the body, or tortured by combatants of the conflict?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_5_1 = models.IntegerField(
        label="3.10. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_5_2 = models.IntegerField(
        label="3.11. ¿Alguna vez fue herido físicamente, golpeado o torturado por un comandante o otro recluta en un conflicto?",
        # … were you ever physically injured, subject to beating(s) to the body, or tortured by your superiors or other abudctees (LRA)?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_5_2 = models.IntegerField(
        label="3.12. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_6 = models.IntegerField(
        label="3.13. ¿Alguna vez presenció o experimentó una explosión?",
        # …have you ever witnessed or experienced a bombing?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_6 = models.IntegerField(
        label="3.14. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_7 = models.IntegerField(
        label="3.15. ¿Alguna vez presenció un disturbio/motín?",
        # … have you ever witnessed or experienced a riot?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_7 = models.IntegerField(
        label="3.16. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_8 = models.IntegerField(
        label="3.17. ¿Alguna vez presenció un asesinato o tiroteo?",
        # … have you ever witnessed or experienced a shooting?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_8 = models.IntegerField(
        label="3.18. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_9 = models.IntegerField(
        label="3.19. ¿Alguna vez presenció un ataque aéreo?",
        # … have you ever witnessed or experienced an aerial strike?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    etv_sc_9 = models.IntegerField(
        label="3.20. Si es así, ¿con qué frecuencia?",
        # If yes, how often?
        choices=C.SCALE_ETV,
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )
    etv_bi_10 = models.IntegerField(
        label="3.21. ¿Alguna vez has sido desplazado internamente?",
        # … have you ever been internally displaced?
        choices=C.BINARY_ANSWER,
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )


# FUNCTIONS
def assign_treatments(p, csv_file):
    participant = p.participant

    # Read all data from CSV
    all_data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            all_data.append(row)

    # Filter by group_participant and etv
    group_player = [
        row for row in all_data
        if int(row['group_participant']) == participant.group
           and int(row['etv']) == participant.etv
    ]

    # Find minimum nb_participant value
    if group_player:
        min_value = min(int(row['nb_participant']) for row in group_player)

        # Filter rows with minimum value
        min_rows = [
            row for row in group_player
            if int(row['nb_participant']) == min_value
        ]

        # Select row (random if multiple, otherwise take the first)
        if len(min_rows) > 1:
            selected_row = random.choice(min_rows)
        else:
            selected_row = min_rows[0]

        # Assign treatments
        participant.treatment_hope = int(selected_row['treatment_hope'])
        participant.side_ultimatum = int(selected_row['side_UG'])
        participant.treatment_other = int(selected_row['treatment_other'])
    else:
        # Handle case where no matching rows found
        # You may want to set defaults or raise an error
        pass


# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = [
        'military_binary'
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.military_binary = player.military_binary
        if participant.military_binary !=1:
            participant.etv=0
            assign_treatments(player, C.DATA_TREATMENT_LOC)
            print(participant.etv)
            print(participant.treatment_hope)
            print(participant.side_ultimatum)
            print(participant.treatment_other)
        else:
            pass
    def is_displayed(player: Player):
        return player.session.config['name'] == "session_C4P_SPANISH_w1"


class Page2_1(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.military_binary == 1 and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'conscription_binary',
                'military_tasks',
                'military_province_main',
                'maindeployment_start_year',
                'maindeployment_start_month',
                'maindeployment_length',
                'deployment_second',
            ]
        else:
            return []
    def is_displayed(player: Player):
        participant = player.participant
        return participant.military_binary == 1 and player.session.config['name'] == "session_C4P_SPANISH_w1"
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.military_binary==1 & player.conscription_binary==1 :
            participant.etv = 1
        else:
            participant.etv = 0
        assign_treatments(player, C.DATA_TREATMENT_LOC)
        print(participant.group)
        print(participant.etv)
        print(participant.treatment_hope)
        print(participant.side_ultimatum)
        print(participant.treatment_other)

class Page2_1_2(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.military_binary == 1 and player.deployment_second==1 and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'military_province_second',
                'seconddeployment_start_year',
                'seconddeployment_start_month',
                'seconddeployment_length'
            ]
        else:
            return []
    def is_displayed(player: Player):
        participant = player.participant
        return participant.military_binary == 1 and player.deployment_second==1 and player.session.config['name'] == "session_C4P_SPANISH_w1"

class Page2_2(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.military_binary != 1 and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'noncombatant_geography_main',
                'noncombatant_geography_main_start_year',
                'noncombatant_geography_main_start_month',
                'noncombatant_geography_main_end_year',
                'noncombatant_geography_main_end_month',
                'noncombatant_geography_second_b'
            ]
        else:
            return []
    def is_displayed(player: Player):
        participant = player.participant
        return participant.military_binary != 1 and player.session.config['name'] == "session_C4P_SPANISH_w1"

class Page2_2_2(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.military_binary != 1 and player.noncombatant_geography_second_b==1 and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'noncombatant_geography_second',
                'noncombatant_geography_second_start_year',
                'noncombatant_geography_second_start_month',
                'noncombatant_geography_second_end_year',
                'noncombatant_geography_second_end_month'
            ]
        else:
            return []
    def is_displayed(player: Player):
        participant = player.participant
        return participant.military_binary != 1 and player.field_maybe_none('noncombatant_geography_second_b')==1 and player.session.config['name'] == "session_C4P_SPANISH_w1"

class Page3(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        """Only return form fields if the page is displayed"""
        participant = player.participant
        if participant.military_binary == 1 and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
                'military_socialization_1',
                'military_socialization_2',
                'military_socialization_3'
            ]
        else:
            return []
    def is_displayed(player: Player):
        participant = player.participant
        return participant.military_binary == 1 and player.session.config['name'] == "session_C4P_SPANISH_w1"


class Page4(Page):
    # Different text on webpage displayed depending on age and military service status
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        participant = player.participant
        if participant.etv == 1:
            return [
                'etv_bi_1',
                'etv_sc_1',
                'etv_bi_2',
                'etv_sc_2',
                'etv_bi_3',
                'etv_sc_3',
                'etv_bi_5_1',
                'etv_sc_5_1',
                'etv_bi_5_2',
                'etv_sc_5_2',
                'etv_bi_6',
                'etv_sc_6',
                'etv_bi_7',
                'etv_sc_7',
                'etv_bi_8',
                'etv_sc_8',
                'etv_bi_9',
                'etv_sc_9',
                'etv_bi_10'
    ]
        else:
            return [
                'etv_bi_1',
                'etv_sc_1',
                'etv_bi_2',
                'etv_sc_2',
                'etv_bi_3',
                'etv_sc_3',
                'etv_bi_5_1',
                'etv_sc_5_1',
                'etv_bi_6',
                'etv_sc_6',
                'etv_bi_7',
                'etv_sc_7',
                'etv_bi_8',
                'etv_sc_8',
                'etv_bi_9',
                'etv_sc_9',
                'etv_bi_10'
    ]
    def is_displayed(player: Player):
        return player.session.config['name'] == "session_C4P_SPANISH_w1"
    def error_message(player, values):
        pairs = [
            ('etv_bi_1', 'etv_sc_1'),
            ('etv_bi_2', 'etv_sc_2'),
            ('etv_bi_3', 'etv_sc_3'),
            ('etv_bi_5_1', 'etv_sc_5_1'),
            ('etv_bi_5_2', 'etv_sc_5_2'),
            ('etv_bi_6', 'etv_sc_6'),
            ('etv_bi_7', 'etv_sc_7'),
            ('etv_bi_8', 'etv_sc_8'),
            ('etv_bi_9', 'etv_sc_9')
        ]
        for bi_field, sc_field in pairs:
            # Only validate if the binary field is in the form
            if bi_field in values and values[bi_field] == 1:
                if sc_field not in values or values[sc_field] is None:
                    return f'Por favor responda la pregunta de frecuencia.'

page_sequence = [
    Page1, # military service filter + treatment assignment
    Page2_1, # questions military service
    Page2_1_2, # additional province military service
    Page2_2, # question non-military service
    Page2_2_2, # additional question non-military service
    Page3, # military socialization
    Page4 # exposure to violence
]