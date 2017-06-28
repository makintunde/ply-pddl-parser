(define (domain shooting)
    (:requirements :typing)
    (:types gun man bool)
    (:predicates (loaded ?g - gun ?b - bool)
                 (alive ?m - man ? b - bool)
                 (istrue ?b - bool))
    (:action shoot
        :parameters (?m - man ?g - gun ?b - bool)
        :precondition (and (alive ?m ?b)
                           (loaded ?g))
        :effect (and (alive ?m ?b)
                     (not (istrue ?b))
                     (not (alive ?m ?b))
                     (istrue ?b))
        :effect (and (not (alive ?m))
                     (not (loaded ?g))))
    (:action load
        :parameters (?g - gun)
        :precondition (not (loaded ?g))
        :effect (and (loaded ?g)))
)