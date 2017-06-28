;
; Modelling the Wumpus World in PDDL: 2nd try...
; by: Patrik Haslum
; Source web page:
;   http://users.cecs.anu.edu.au/~patrik/pddlman/wumpus.html
;

(define (domain wumpus-b)
  (:requirements :strips)
  (:predicates
   (adj ?square-1 ?square-2)
   (pit ?square)

   (at ?what ?square)
   (have ?who ?what)

   (takeable ?what)
   (is-gold ?what)
   (is-arrow ?what)

   (alive ?who)
   (dead ?who))

  (:action move
    :parameters (?who ?from ?to)
    :precondition (and (alive ?who)
		       (at ?who ?from)
		       (adj ?from ?to)
		       (not (pit ?to)))
    :effect (and (not (at ?who ?from))
		 (at ?who ?to))
    )

  (:action take
    :parameters (?who ?what ?where)
    :precondition (and (alive ?who)
		       (takeable ?what)
		       (at ?who ?where)
		       (at ?what ?where))
    :effect (and (have ?who ?what)
		 (not (at ?what ?where)))
    )

  (:action shoot
    :parameters (?who ?where ?arrow ?victim ?where-victim)
    :precondition (and (alive ?who)
		       (have ?who ?arrow)
		       (is-arrow ?arrow)
		       (at ?who ?where)
		       (alive ?victim)
		       (at ?victim ?where-victim)
		       (adj ?where ?where-victim))
    :effect (and (dead ?victim)
		 (not (alive ?victim))
		 (not (at ?victim ?where-victim))
		 (not (have ?who ?arrow)))
    )
)