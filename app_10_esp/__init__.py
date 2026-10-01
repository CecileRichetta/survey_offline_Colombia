from otree.api import *


doc = """
Evaluation of the questionnaire. 
"""


class C(BaseConstants):
    NAME_IN_URL = 'app_10_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # CHOICES
    CHOICES_EVAL = [
        (0, "Completamente en desacuerdo"), # Completely disagree
        (1, "En desacuerdo"), # Disagree
        (2, "Ni de acuerdo ni en desacuerdo"), # Neither disagree nor agree
        (3, "De acuerdo"), # Agree
        (4, "Completamente de acuerdo"), # Completely agree
        (998, "No sabe (no leer)"), # Don't know
        (999, "No responde (no leer)") # Prefer not to say
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    evaluation_1 = models.IntegerField(
        label="10.1. ¿Qué tan de acuerdo está con la siguiente afirmación? La longitud del cuestionario es adecuada.",
        # The length of the questionnaire is appropriate.
        choices=C.CHOICES_EVAL,
        widget=widgets.RadioSelect,
        blank=False
    )
    evaluation_1_long = models.LongStringField(
        label="10.2. Por favor, especifique la pregunta que considera demasiado larga:",
        # Please specify which questions were too long:
        blank=True
    )
    evaluation_2 = models.IntegerField(
        label="10.3. ¿Qué tan de acuerdo está con la siguiente afirmación? Las preguntas son fáciles de entender.",
        # The questions are easy to understand.
        choices=C.CHOICES_EVAL,
        widget=widgets.RadioSelect,
        blank=False
    )
    evaluation_2_long = models.LongStringField(
        label="10.4. Por favor, indique el contenido que considere difícil de entender.",
        #Please specify which elements you found were hard to understand:
        blank=True
    )
    evaluation_3 = models.IntegerField(
        label="10.5. ¿Qué tan de acuerdo está con la siguiente afirmación? Las instrucciones y ejemplos para ambas actividades con fichas son fáciles de entender.",
        # The instructions and examples for the two tasks with the tokens are easy to understand.
        choices=C.CHOICES_EVAL,
        widget=widgets.RadioSelect,
        blank=False
    )
    evaluation_3_long = models.LongStringField(
        label="10.6. Por favor, especifique el contenido de la actividad que no se entendió:",
        # Please specify what you did not understand about the tasks:
        blank=True
    )
    evaluation_4 = models.IntegerField(
        label="10.7. ¿Qué tan de acuerdo está con la siguiente afirmación: Las preguntas sobre experiencias de violencia le hacen sentir incómodo.",
        # The questions about the experience of violence in my home country made me uncomfortable.
        choices=C.CHOICES_EVAL,
        widget=widgets.RadioSelect,
        blank=False
    )
    evaluation_4_long = models.LongStringField(
        label="10.8. ¿Qué pregunta le incomodó más?",
        # Which questions made you most uncomfortable:
        blank=True
    )
    evaluation_5 = models.IntegerField(
        label="10.9. ¿Qué tan de acuerdo está con la siguiente afirmación?: Sus derechos como participante son claros desde el principio.",
        # My rights as a participant were clear from the start.
        choices=C.CHOICES_EVAL,
        widget=widgets.RadioSelect,
        blank=False
    )
    evaluation_5_long = models.LongStringField(
        label="10.10. ¿Qué información sobre sus derechos como participante no está clara?",
        # What parts about your rights as a participant were not clear:
        blank=True
    )
    evaluation_6 = models.IntegerField(
        label="10.11. ¿Qué tan de acuerdo está con la siguiente afirmación: El cuestionario es interesante.",
        # The questionnaire was interesting.
        choices=C.CHOICES_EVAL,
        widget=widgets.RadioSelect,
        blank=False
    )
    evaluation_6_long = models.LongStringField(
        label="10.12. ¿Qué parte del cuestionario no es interesante?",
        # Which parts of the questionnaire were not interesting:
        blank=True
    )
    evaluation_7_long = models.LongStringField(
        label="10.13. ¿Qué le pareció el texto, especialmente en cuanto a su credibilidad y lo esperanzador que lo hizo sentir? ¿Tiene alguna sugerencia para mejorarlo?",
        blank=True
    )
    evaluation_other = models.LongStringField(
        label="10.14. ¿Tiene algún comentario u observación adicional sobre el cuestionario?",
        # Do you have any additional remarks or comments on the questionnaire?
        blank=True
    )
# PAGES
class Page1(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        participant = player.participant
        if participant.dropout is False and player.session.config['name'] == "session_C4P_SPANISH_w1":
            return [
        'evaluation_1',
        'evaluation_1_long',
        'evaluation_2',
        'evaluation_2_long',
        'evaluation_3',
        'evaluation_3_long',
        'evaluation_4',
        'evaluation_4_long',
        'evaluation_5',
        'evaluation_5_long',
        'evaluation_6',
        'evaluation_6_long',
        'evaluation_other'
    ]
        else:
            return [
                'evaluation_1',
                'evaluation_1_long',
                'evaluation_2',
                'evaluation_2_long',
                'evaluation_3',
                'evaluation_3_long',
                'evaluation_4',
                'evaluation_4_long',
                'evaluation_5',
                'evaluation_5_long',
                'evaluation_6',
                'evaluation_6_long',
                'evaluation_7_long',
                'evaluation_other'
            ]

page_sequence = [
    Page1
]
