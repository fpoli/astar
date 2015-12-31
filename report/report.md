Relazione
=========


Modellazione
------------

(Come abbiamo modellato ambiente, agente, azioni, sensori)

### Ambiente

### Agente


Strategie
---------

### RandomBot

Un bot che sceglie azioni a caso.

### SimpleGoalBot

Un bot senza funziona di utilità.
(2 righe...)

### MaxnBot

Un bot che usa la ricerca MaxN per la scelta dell'azione.
(5 righe...)

### ParanoidBot

Un bot che usa la ricerca Paranoid per la scelta dell'azione.
(5 righe...)

(differenza tra MaxN e Paranoid)


Euristiche
----------

### GoldHeuristic

Assume che tutti gli agenti scompaiano dalla mappa, e calcola la quantità d'oro
finale per ciascuno.
Utilizza la quantità di oro finale come funzione di utilità.

### EloGoldHeuristic

Come GoldHeuristic, ma calcola anche quanti punti riceverebbe ogni giocatore
alla fine della partita in base al sistema Elo.
Utilizza i punti guadagnati o persi come funzione di utilità.

### MineGoldHeuristic

Come GoldHeuristic, ma include anche l'oro che il giocatore guadagnerebbe se,
rimanendo solo sulla mappa, potesse spostarsi ed andare a conquistare una
miniera in più. Eventualmente passando prima alla taverna.

È un euristica molto efficace abbinata a minimax, perché permette di scegliere
la strada più corta per arrivare ad una miniera (e taverna) senza dover
aumentare la profondità della ricerca.


Casi d'uso
----------

(link ad alcune partite...)

(Alcuni screenshot con siegazione di quale azione è stata scelta dal bot e
perchè...)


Consuntivo orario
-----------------

- Progettazione: (...)
- Implementazione modelli e comunicazione server: (...)
- Implementazione algoritmi: (...)
- Implementazione bot: (...)
- Implementazione euristiche: (...)
- Stesura relazione: (...)


Riferimenti
-----------

- Semplice bot open source "di partenza": https://github.com/ornicar/vindinium-starter-python
- Libreria open source per Vindinium che abbiamo usato: https://github.com/renatopp/vindinium-python
- Ricerca MaxN: "An Algorithmic Solution of N-Person Games", Luckhardt-Irani, 1986
- Ricerca Paranoid: "On Pruning Techniques for Multi-Player Games", Sturtevant-Korf, 2000
- Euristica MineGold: https://www.reddit.com/r/vindinium/comments/2kgsx4/a_chat_with_the_creator_of_the_best_performing/
