(define (problem BLOCKS-4-0)
(:domain BLOCKS)
(:objects
    D - block
    B - block
    A - block
    C - block
    E - block
    F - block
    G - block
    H - block
    I - block)
(:INIT (HANDEMPTY)
       (CLEAR F)
       (ONTABLE A)
       (ON F E)
       (ON E B)
       (ON B D)
       (ON D C)
       (ON C I)
       (ON I G)
       (ON G H)
       (ON G H)
       (ON H A))
(:goal
    (AND
        (ON D I)
        (ON I A)
        (ON A B)
        (ON B H)
        (ON H G)
        (ON G F)
        (ON F E)
        (ON E C))))
