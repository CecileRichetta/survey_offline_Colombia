from otree.api import *


doc = """
Manipulation check and Emotions.
"""


class C(BaseConstants):
    NAME_IN_URL = 'app_7_ESP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # SCALE
    ANSWER_SCALE = [
        (0, "Totalmente en desacuerdo"), # Strongly disagree
        (1, "En desacuerdo"), # Disagree
        (2, "Ni de acuerdo ni en desacuerdo"), # Neither disagree nor agree
        (3, "De acuerdo"), # Agree
        (4, "Totalmente de acuerdo"), # Strongly agree
        (998, "No sabe (no leer)"), # Don't know
        (999, "No responde (no leer)") # Prefer not to say
    ]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    empathy_6 = models.IntegerField(
        # dynamic labels in the webpage
        choices=C.ANSWER_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    guilt_1 = models.IntegerField(
        # dynamic labels in webpage
        choices=C.ANSWER_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    anger_2 = models.IntegerField(
        # dynamic labels in webpage
        choices=C.ANSWER_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )
    fear_1 = models.IntegerField(
        # dynamic labels in webpage
        choices=C.ANSWER_SCALE,
        widget=widgets.RadioSelect,
        blank=False
    )


# FUNCTIONS



# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = [
        'empathy_6',
        'guilt_1',
        'anger_2',
        'fear_1',
    ]

page_sequence = [
    Page1 # group emotions
]