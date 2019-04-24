from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    )
import random

doc = """
In Cournot competition, firms simultaneously decide the units of products to
manufacture. The unit selling price depends on the total units produced. In
this implementation, there are 2 firms competing for 1 period.
"""


class Constants(BaseConstants):
    name_in_url = 'cournot'
    players_per_group = 3
    num_rounds = 6
    print("execute constants class")
    print("players per group = ", players_per_group)
    instructions_template = 'cournot_best/instructions.html'                    ###This must match the directory name within templates


    total_capacity = 60         # Total production capacity of all players
    max_units_per_player = int(total_capacity / players_per_group)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
   print("group class")
   unit_price = models.CurrencyField()
   total_units = models.IntegerField(
        doc="""Total units produced by all players"""
    )



   def set_payoffs(self):
       players = self.get_players()
       print("defining payoffs")
       self.total_units = sum([p.units for p in players])
       self.unit_price = Constants.total_capacity - self.total_units
       #setattr(self.prev_total_units, 5)
       self.prev_total_units = 5
       self.prev_total_units = self.in_round(self.round_number-1).total_units  ##### I want this to generate a variable that I can then put into the html pages
       print(self.round_number)
       print(self.in_round(self.round_number-1).total_units)
       for p in players:
           p.payoff = self.unit_price * p.units


class Player(BasePlayer):
    units = models.IntegerField(
        min=0, max=Constants.max_units_per_player,
        doc="""Quantity of units to produce"""
    )

    def other_player(self):
       print("baseplayer round number")
       print(self.round_number)
       return self.get_others_in_group()[0]

