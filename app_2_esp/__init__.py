from otree.api import *

doc = """
Demographics questions
"""


class C(BaseConstants):
    NAME_IN_URL = 'app_2_esp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    VENN_COLOMBIA = 'imgs/venn_colombia.png'
    # CHOICES IN VARIABLES
    EDUCATION = [
        (0, "Sin educación formal"),  #
        (1, "Primaria incompleta"),  #
        (2, "Primaria completa"),  #
        (3, "Secundaria incompleta"),  #
        (4, "Secundaria completa"),  #
        (5, "Educación técnica incompleta"),  #
        (6, "Educación técnica completa"),  #
        (7, "Educación universitaria incompleta"),  #
        (8, "Educación universitaria completa"),  #
        (9, "Máster o doctorado (posgrado)"),  #
        (10, "Otro"),
        (998, "No sabe (no leer)"),  # Don't know
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    DEPENDENTS_SALARY = [
        (0, "Una persona"), # one person
        (1, "Dos personas"), # two people
        (2, "Tres personas"), # three people
        (3, "Cuatro personas"), # four people
        (4, "Cinco personas"), # five people
        (5, "Más de cinco personas"), # more than give people
        (998, "No sabe (no leer)"),  # Don't know
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    RELIGION = [
        (0, "Católico"), # Catolico
        (1, "Cristiano (no católico)"), # Christian non-Catholic
        (2, "Ortodoxo"), # Orthodox
        (3, "Protestante"), #
        (4, "Judío"), #
        (5, "Budista"),
        (6, "Otro"), #
        (7, "No creo en ninguna religión"), #
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    RELIGIOSITY = [
        (0, "No es nada religioso"), # Not religious at all
        (1, "Algo religioso"), # Somewhat religious
        (2, "Religioso"), # Religious
        (3, "Muy religioso"), # Very religious
        (997, "No aplica (no leer)"),  # Not applicable
        (999, "Prefiero no decirlo") # Prefer not to say
    ]
    INSECURITY = [
        (0, "Nunca"), # Never
        (1, "Solo una o dos veces"), # Just once or twice
        (2, "Varias veces"), # Several times
        (3, "Muchas veces"), # Many times
        (4, "Siempre"), # Always
        (998, "No sabe (no leer)"),  # Don't know
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    SCALE_AGREEMENT = [
        (0, "Completamente en desacuerdo"), # Completely disagree
        (1, "En desacuerdo"), # Disagree
        (2, "Ni de acuerdo ni en desacuerdo"), # Neither disagree or agree
        (3, "De acuerdo"), # Agree
        (4, "Completamente de acuerdo"), # Completely agree
        (998, "No sabe (no leer)"),  # Don't know
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    ECONOMIC_STATUS_1 = [
        (0, "Muy malas"), # Very bad
        (1, "Bastante malas"), # Fairly bad
        (2, "Ni buenas ni malas"), # Neither bad nor good
        (3, "Bastante buenas"), # Fairly good
        (4, "Muy buenas"), # Very good
        (998, "No sabe (no leer)"),  # Don't know
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    ECONOMIC_STATUS_2 = [
        (0, "Menos de $1.750.000"), # Less than 10'000BHT
        (1, "Entre $1.750.001 y $3.500.000"), # 10'000 to 20'000BHT
        (2, "Entre $3.500.001 y $5.250.000"), # 20'000 to 30'000BHT
        (4, "Entre $5.250.001 y $7.000.000"), # 40'000 to 5'000BHT
        (5, "Entre $7.000.001 y $8.750.000"), # more than 50'000BHT
        (6, "Entre $8.750.000 y $10.500.000"),
        (7, "$10.500.000 en adelante"),
        (998, "No sabe (no leer)"),  # Don't know
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    BINARY_ANSWER = [
        (1, "Sí"),  # Yes
        (0, "No"), # No
        (999, "No responde (no leer)")  # Prefer not to say
    ]
    BINARY_ANSWER_NA = [
        (1, "Sí"),  # Yes
        (0, "No"), # No
        (997, "No aplica (no leer)"),  # Not applicable
        (999, "No responde (no leer)")  # Prefer not to say
    ]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # SOCIO-DEM VARIABLES
    recall = models.StringField(
        label="2.1. Por favor, ¿cuál es su nombre completo?",
        blank=False
    )
    age = models.IntegerField(
        label="2.2. Por favor, indique cuántos años tiene (en años):",
        min=48,
        max=54,
        blank=False
    )
    education = models.IntegerField(
        label="2.3. ¿Cuál es su nivel más alto de educación alcanzado?",
        choices=C.EDUCATION,
        blank=False,
        widget=widgets.RadioSelect
    )
    education_other = models.StringField(
        label="2.3.1. Si otro:",
        blank=True
    )
    eco_status_1 = models.IntegerField(
        label="2.4. En general, ¿cómo describiría sus condiciones actuales de vida?",
        widget=widgets.RadioSelect,
        choices=C.ECONOMIC_STATUS_1,
        blank=False
    )
    eco_status_2 = models.IntegerField(
        label="2.5. Sumando todas sus fuentes de ingresos, ¿cuál es el ingreso bruto mensual de su hogar (antes de deducir "
              "impuestos, contribuciones a la seguridad social y otros gastos)?",
        choices=C.ECONOMIC_STATUS_2,
        widget=widgets.RadioSelect,
        blank=False
    )
    dependents_salary = models.IntegerField(
        label="2.6. Incluyendose a usted ¿Cuántas personas viven en su hogar?",
        # How many people live in your household? + definition household
        choices=C.DEPENDENTS_SALARY,
        widget=widgets.RadioSelect,
        blank=False
    )
    religion = models.IntegerField(
        label="2.7. ¿Cuál es su religión?", # what is your religion?
        choices=C.RELIGION,
        widget=widgets.RadioSelect,
        blank=False
    )
    religiosity = models.IntegerField(
        label="2.8. ¿Qué tan religioso es? ", # how religious are you?
        choices=C.RELIGIOSITY,
        widget=widgets.RadioSelect,
        blank=True
    )
    insecurity = models.IntegerField(
        label="2.9. En el último año, ¿con qué frecuencia usted o algún miembro de su familia se ha sentido inseguro en su casa "
              "o en su barrio?, si es que alguna vez ha ocurrido",
        # Over the past year, how often, if ever, have you or anyone in your family felt unsafe in your home or neighborhood?
        choices=C.INSECURITY,
        widget=widgets.RadioSelect,
        blank=False
    )
    group_attachment_1 = models.IntegerField(
        label="2.10. Qué tan de acuerdo esta con la siguiente afirmación: ¿Siento un fuerte apego a Colombia?",
        choices=C.SCALE_AGREEMENT,
        widget=widgets.RadioSelect,
        blank=False
    )
    group_attachment_2 = models.IntegerField(
        label="2.11. ¿Qué tan de acuerdo está  con la siguiente afirmación: A menudo se considera colombiano?",
        choices=C.SCALE_AGREEMENT,
        widget=widgets.RadioSelect,
        blank=False
    )
    venn_1 = models.IntegerField(
        label="2.12. Le voy a mostrar unos dibujos de círculos. Entre más se juntan o se superponen los dos círculos, más "
              "cercana es la relación entre las dos personas. En estos dibujos, el círculo 'Yo' lo representa a usted, "
              "y el círculo 'Otro' representa a los simpatizantes del Pacto Histórico. De acuerdo a esto, ¿cuál de estos "
              "dibujos describe mejor qué tan cerca se siente usted de ellos? (Encuestador mostrar tarjeta P.2.12)",
        choices=[
            (0, "(1)"),
            (1, "(2)"),
            (2, "(3)"),
            (3, "(4)"),
            (4, "(5)"),
            (998, "No sabe (no leer)"),
            (999, "No responde (no leer)")
        ],
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    venn_2 = models.IntegerField(
        label="2.13. Ahora le voy a hacer una pregunta parecida, pero pensando en un grupo diferente. En estos dibujos, "
              "el círculo 'Yo' lo sigue representando a usted, pero ahora el círculo 'Otro' representa a individuos de "
              "grupos que compartieron los objetivos que perseguían las FARC durante el conflicto. Pensando en ese grupo, "
              "¿cuál de estos dibujos describe mejor qué tan cerca se siente usted de ellos?",
        choices=[
            (0, "(1)"),
            (1, "(2)"),
            (2, "(3)"),
            (3, "(4)"),
            (4, "(5)"),
            (998, "No sabe (no leer)"),
            (999, "No responde (no leer)")
        ],
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )

# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = [
        'recall',
        'age',
        'education',
        'education_other',
        'eco_status_1',
        'eco_status_2',
        'dependents_salary',
        'religion',
        'religiosity',
        'insecurity'
    ]
    def is_displayed(player: Player):
        return player.session.config['name'] == "session_C4P_SPANISH_w1"
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.recontact_1 = player.recall
        participant.age = player.age
        player.recall = "Anonymous"
    def error_message(player, values):
        # Only validate religiosity if religion is NOT 7 AND NOT 999
        if values['religion'] != 7 and values['religion'] != 999:
            if values.get('religiosity') is None:
                return 'Por favor indique qué tan religioso es.'


class Page2(Page):
    form_model = 'player'
    form_fields = [
        'group_attachment_1',
        'group_attachment_2',
        "venn_1",
        "venn_2"
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['name'] == "session_C4P_SPANISH_w1"
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
#        participant.age = player.age
        if player.venn_2 > 0 and player.venn_2!=998 and player.venn_2!=999:
            participant.group = 0
            print(participant.group)
        else:
            participant.group = 1
            print(participant.group)


page_sequence = [
    Page1, # socio-demographics
    Page2 # group + group attachment
]
