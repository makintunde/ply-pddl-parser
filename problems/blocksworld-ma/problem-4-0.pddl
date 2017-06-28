(define (problem BLOCKS-4-0)
(:domain BLOCKS)
(:objects
    d - block
    b - block
    a - block
    c - block

    (:private a1
        a1 - agent
    )

    (:private a2
        a2 - agent
    )
)

(:init
    (handempty a1)
    (handempty a2)
    (clear c)
    (clear a)
    (clear b)
    (clear d)
    (ontable c)
    (ontable a)
    (ontable b)
    (ontable d)

)
(:goal (and (on d c) (on c b) (on b a)))
)
