(define (problem vehicle-example)
    (:domain vehicle)
    (:objects
        truck car - vehicle
        full half empty - fuellevel
        paris berlin rome madrid - location)
    (:init
        (at truck rome)
        (at car paris)
        (fuel truck half)
        (fuel car full)
        (next full half)
        (next half empty)
        (accessible car paris berlin)
        (accessible car berlin rome)
        (accessible car rome madrid)
        (accessible truck rome paris)
        (accessible truck rome berlin)
        (accessible truck berlin paris)
    )
    (:goal (and (at truck paris)
                (at car rome))
    )
)