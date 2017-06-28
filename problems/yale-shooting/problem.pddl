(define (problem yale-shooting)
    (:domain shooting)
    (:requirements :typing)
    (:objects joe - man
              colt - gun
              true false - bool)
    (:init
        (alive joe true))
    (:goal (and (alive joe false)
                (loaded colt false)))
)