(define (problem sfo-jfk)
    (:domain air-cargo)
    (:objects c1 c2 - cargo sfo jfk - airport p1 p2 - plane)
    (:init
        (at c1 sfo)
        (at p1 sfo)
        (at c2 jfk)
        (at p2 jfk))
    (:goal (and
        (at c1 jfk)
        (at c2 sfo))))