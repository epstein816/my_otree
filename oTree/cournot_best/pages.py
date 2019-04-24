from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Decide(Page):
    form_model = 'player'
    form_fields = ['units']
    print("decide page")


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant to decide."

    def after_all_players_arrive(self):
        self.group.set_payoffs()




class Results(Page):
    def vars_for_template(self):
        print("results page round number")
        print(self.round_number)
        return {
        'other_player_units': self.player.other_player().units
        }
        return {

        }

page_sequence = [
  #  Introduction,
    Decide,
    ResultsWaitPage,
    Results
]
