# Um zu gewinnen, muss man die letzte Schlange sein.
# Man stirbt, wenn man:
#    1. Den Rand berührt
#    2. Seinen eigenen Körper berührt
#    3. Eine andere Schlange berührt
#    4. Den Kopf einer Schlange berührt und man kleiner oder gleich groß ist
#    5. Man verhungert 
#
# Theoretisch gute Heuristik:
#    So viel Food wie möglich konsumieren
#    Andere eliminieren
#    Nicht eliminiert werden
#
# Taktiken zum Eliminieren:
#    1. einkesseln
#    2. kleinere Angreifen
#
# Taktiken zum überleben:
#    1. nicht in Spirale kommen (loops vermeiden)
#    2. Rand meiden?
#    3. Köpfe größerer meiden?
#
#
#
# Agent:
# MinMax?
# Baum explorieren, und besten Pfad wählen
#
# Brauchen:
#    rate_path()
#    rate_state()
#    explore_possible_next_states()    Soll 

import typing

#   function Alpha-Beta-Decision(state) returns an action
#     return the a in Actions(state) maximizing Min-Value(Result(a, state))
def alpha_beta_decision(game_state: typing.Dict) -> typing.Dict:
  actions = {
    "up": True, 
    "down": True, 
    "left": True, 
    "right": True
  }
  return {"move": "up"}  # TODO: Placeholder

#  function Max-Value(state, α, β) returns a utility value
#    inputs:   state, current state in game
#              α, the value of the best alternative for max along the path to state
#              β, the value of the best alternative for min along the path to state
#    if Terminal-Test(state) then return Utility(state)
#    v ← −∞
#    for a, s in Successors(state) do
#      v ← Max(v, Min-Value(s, α, β))
#      if v ≥ β then return v
#      α ← Max(α, v)
#    return v
def max_value(game_state, alpha, beta) -> float:
  return

#  function Min-Value(state, α, β) returns a utility value
#    same as Max-Value but with roles of α, β reversed
def min_value(game_state, alpha, beta) -> float:
  return