;; Transport a number of objects from their start- to their goal-locations, using a briefcase.
;; Each location is accessible from each other location, objects can be put into the briefcase
;; or taken out of the briefcase. When a move is made between locations, then all objects inside
;; the briefcase are also moved, which is encoded by a conditional effect.

(define (domain briefcase)
(:requirements :adl :typing)
(:types portable location)
(:predicates (at ?y - portable ?x - location)
             (in ?x - portable)
             (is-at ?x - location))

(:action move
  :parameters (?m ?l - location)
  :precondition  (is-at ?m)
  :effect (and (is-at ?l)
               (not (is-at ?m))
		       (forall (?x - portable) (when (in ?x) (and (at ?x ?l) (not (at ?x ?m)))))))

(:action take-out
  :parameters (?x - portable)
  :precondition (in ?x)
  :effect (not (in ?x)))

(:action put-in
  :parameters (?x - portable ?l - location)
  :precondition (and (not (in ?x)) (at ?x ?l) (is-at ?l))
  :effect (in ?x)))

