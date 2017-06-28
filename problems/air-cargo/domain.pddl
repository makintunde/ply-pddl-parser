(define (domain air-cargo)
    (:requirements :typing :adl)
    (:types cargo plane airport)
    (:predicates (at ?t - (either cargo plane) ?a - airport)
                 (in ?c - cargo ?p - plane))

    (:action load
        :parameters (?c - cargo ?p - plane ?a - airport)
        :precondition (and (at ?c ?a) (at ?p ?a))
        :effect (and (not (at ?c ?a)) (in ?c ?p)))

    (:action unload
        :parameters (?c - cargo ?p - plane ?a - airport)
        :precondition (and (in ?c ?p) (at ?p ?a))
        :effect (and (at ?c ?a) (not (in ?c ?p))))

    (:action fly
        :parameters (?p - plane ?a1 ?a2 - airport)
        :precondition (and (at ?p ?a1) (not (= ?a1 ?a2)))
        :effect (and (not (at ?p ?a1)) (at ?p ?a2))))