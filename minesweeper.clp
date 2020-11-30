(deffacts no-bomb
    (aman 0 0)
)

(defrule open-tile
    (aman ?x ?y)
    (not (open ?x ?y))
    (not (using-program))
    =>
    (printout t "(1" ?x " , "  ?y ")" crlf)
)

(defrule pattern11-vertical-1
    (open ?i1 ?j)
    (open ?i2 ?j)
    (value ?i1 ?j 1)
    (value ?i2 ?j 1)
    (test (= ?i2 (+ ?i1 1)))
    =>
    (assert (aman (- ?i1 1) (+ ?j 1)))
    (assert (aman (+ ?i2 1) (+ ?j 1)))
    (assert (aman (- ?i1 1) (- ?j 1)))
    (assert (aman (+ ?i2 1) (- ?j 1)))
)

(defrule pattern11-vertical-2
    (open ?i1 ?j)
    (open ?i2 ?j)
    (value ?i1 ?j 1)
    (value ?i2 ?j 1)
    (test (= ?i1 (+ ?i2 1)))
    =>
    (assert (aman (+ ?i1 1) (+ ?j 1)))
    (assert (aman (- ?i2 1) (+ ?j 1)))
    (assert (aman (+ ?i1 1) (- ?j 1)))
    (assert (aman (- ?i2 1) (- ?j 1)))
)

(defrule pattern11-horizontal-1
    (open ?i ?j1)
    (open ?i ?j2)
    (value ?i ?j1 1)
    (value ?i ?j2 1)
    (test (= ?j1 (+ ?j2 1)))
    =>
    (assert (aman (+ ?i 1) (+ ?j1 1)))
    (assert (aman (+ ?i 1) (- ?j2 1)))
    (assert (aman (- ?i 1) (+ ?j1 1)))
    (assert (aman (- ?i 1) (- ?j2 1)))
)


(defrule pattern11-horizontal-2
    (open ?i ?j1)
    (open ?i ?j2)
    (value ?i ?j1 1)
    (value ?i ?j2 1)
    (test (= ?j2 (+ ?j1 1)))
    =>
    (assert (aman (+ ?i 1) (+ ?j2 1)))
    (assert (aman (+ ?i 1) (- ?j1 1))) 
    (assert (aman (- ?i 1) (+ ?j2 1))) 
    (assert (aman (- ?i 1) (- ?j1 1))) 
)

(defrule pattern12-horizontal-1
    (open ?i ?j1)
    (open ?i ?j2)
    (open ?i ?j3) (test (= ?i (+ ?j2 1)))           ;TEST lagi
    (open ?i2 ?j4) (test (= (- ?i 1) (+ ?j2 1)))    ;TEST lagi
    (value ?i ?j1 ?val1)
    (value ?i ?j2 ?val2)
    (test (= ?j2 (+ ?j1 1)))
    (test (>= ?val1 1))
    (test (>= ?val2 2))
    =>
    (assert (mark (+ ?i 1) (+ ?j2 1)))
)


;(defrule pattern12-horizontal-2
;    (open ?i ?j1)
;    (open ?i ?j2)
;    (open ?i (+ ?j2 1))
;    (open (- ?i 1) (+ ?j2 1))
;    (value ?i ?j1 ?val1)
;    (value ?i ?j2 ?val2)
;    (test (= ?j2 (+ ?j1 1)))
;    (test (>= ?val1 1))
;    (test (>= ?val2 2))
;    =>
;    (assert (mark (+ ?i 1) (+ ?j2 1)))
;)

