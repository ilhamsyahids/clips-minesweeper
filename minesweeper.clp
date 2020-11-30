(deffacts no-bomb
    (aman 0 0)
)

(defrule stop-exec
    (stop)
    =>
    (halt)
)

(defrule open-tile
    (not (flag ?x ?y))
    (aman ?x ?y)
    (not (open ?x ?y))
    (size ?n)
    (test (>= ?x 0))
    (test (< ?x ?n))
    (test (>= ?y 0))
    (test (< ?y ?n))
    (not (using-program))
    =>
    (printout t "(1" ?x " , "  ?y ")" crlf)
)

(defrule pattern11-vertical-upedge
    (open ?i1 ?j)
    (open ?i2 ?j)
    (value ?i1 ?j 1)
    (value ?i2 ?j 1)
    (test (= ?i2 (+ ?i1 1)))
    (or (test (= ?i1 0)) 
        (and (open ?i3 ?j) (test (= ?i3 (- ?i1 1)))))
    =>
    (assert (aman (+ ?i2 1) (+ ?j 1))
            (aman (+ ?i2 1) ?j)
            (aman (+ ?i2 1) (- ?j 1)))
    ;(printout t "pattern11-vertical-upedge" crlf)
)

(defrule pattern11-vertical-downedge
    (open ?i1 ?j)
    (open ?i2 ?j)
    (value ?i1 ?j 1)
    (value ?i2 ?j 1)
    (test (= ?i2 (+ ?i1 1)))
    (size ?n)
    (or (test (= ?i2 (- ?n 1))) 
        (and (open ?i3 ?j) (test (= ?i3 (+ ?i2 1)))))
    =>
    (assert (aman (- ?i1 1) (+ ?j 1))
            (aman (- ?i1 1) ?j)
            (aman (- ?i1 1) (- ?j 1)))
    ;(printout t "pattern11-vertical-down" crlf)
)

(defrule pattern11-horizontal-leftedge
    (open ?i ?j1)
    (open ?i ?j2)
    (value ?i ?j1 1)
    (value ?i ?j2 1)
    (test (= ?j2 (+ ?j1 1)))
    (or (test (= ?j1 0)) 
        (and (open ?j3 ?i) (test (= ?j3 (- ?j1 1)))))
    =>
    (assert (aman (- ?i 1) (+ ?j2 1))
        (aman ?i (+ ?j2 1))
        (aman (+ ?i 1) (+ ?j2 1)))
    ;(printout t "pattern11-vertical-left" crlf)
)

(defrule pattern11-horizontal-rightedge
    (open ?i ?j1)
    (open ?i ?j2)
    (value ?i ?j1 1)
    (value ?i ?j2 1)
    (test (= ?j2 (+ ?j1 1)))
    (size ?n)
    (or (test (= ?j2 (- ?n 1))) 
        (and (open ?j3 ?i) (test (= ?j3 (+ ?j2 1)))))
    =>
    (assert (aman (- ?i 1) (- ?j1 1))
            (aman ?i (- ?j1 1))
            (aman (+ ?i 1) (- ?j1 1)))
    ;(printout t "pattern11-vertical-right" crlf)
)

(defrule pattern12-vertical-upedge
    (open ?i1 ?j)
    (open ?i2 ?j)
    (value ?i1 ?j ?value1)
    (value ?i2 ?j ?value2)
    (test (>= ?value1 1))
    (test (>= ?value2 2))
    (test (= ?i2 (+ ?i1 1)))
    (or (test (= ?i1 0)) 
        (and (open ?i3 ?j) (test (= ?i3 (- ?i1 1)))))
    =>
    (assert (flag (+ ?i2 1) (+ ?j 1))
            (flag (+ ?i2 1) (- ?j 1)))
    ;(printout t "pattern11-vertical-upedge" crlf)
)

(defrule pattern12-vertical-downedge
    (open ?i1 ?j)
    (open ?i2 ?j)
    (value ?i1 ?j ?value1)
    (value ?i2 ?j ?value2)
    (test (>= ?value1 2))
    (test (>= ?value2 1))
    (test (= ?i2 (+ ?i1 1)))
    (size ?n)
    (or (test (= ?i2 (- ?n 1))) 
        (and (open ?i3 ?j) (test (= ?i3 (+ ?i2 1)))))
    =>
    (assert (flag (- ?i1 1) (+ ?j 1))
            (flag (- ?i1 1) (- ?j 1)))
    ;(printout t "pattern11-vertical-down" crlf)
)

(defrule pattern12-horizontal-leftedge
    (open ?i ?j1)
    (open ?i ?j2)
    (value ?i ?j1 ?value1)
    (value ?i ?j2 ?value2)
    (test (>= ?value1 1))
    (test (>= ?value2 2))
    (test (= ?j2 (+ ?j1 1)))
    (or (test (= ?j1 0)) 
        (and (open ?j3 ?i) (test (= ?j3 (- ?j1 1)))))
    =>
    (assert (flag (- ?i 1) (+ ?j2 1))
        (flag (+ ?i 1) (+ ?j2 1)))
    ;(printout t "pattern11-vertical-left" crlf)
)

(defrule pattern12-horizontal-rightedge
    (open ?i ?j1)
    (open ?i ?j2)
    (value ?i ?j1 ?value1)
    (value ?i ?j2 ?value2)
    (test (>= ?value1 2))
    (test (>= ?value2 1))
    (test (= ?j2 (+ ?j1 1)))
    (size ?n)
    (or (test (= ?j2 (- ?n 1))) 
        (and (open ?j3 ?i) (test (= ?j3 (+ ?j2 1)))))
    =>
    (assert (flag (- ?i 1) (- ?j1 1))
            (flag (+ ?i 1) (- ?j1 1)))
    ;(printout t "pattern11-vertical-right" crlf)
)

(defrule pattern-siku-kiri-atas
    (open ?i1 ?j1)
    (open ?i2 ?j1)
    (open ?i1 ?j2)
    (value ?i1 ?j1 ?val1)
    (value ?i2 ?j1 ?val2)
    (value ?i1 ?j2 ?val3)
    (test (>= ?val1 1))
    (test (>= ?val2 1))
    (test (>= ?val3 1))
    (test (= ?i2 (+ ?i1 1)))
    (test (= ?j2 (+ ?j1 1)))
    =>
    (assert (siku (+ ?i1 1) (+ ?j1 1)))
)

(defrule pattern-siku-kanan-atas
    (open ?i1 ?j1)
    (open ?i2 ?j1)
    (open ?i1 ?j2)
    (value ?i1 ?j1 ?val1)
    (value ?i2 ?j1 ?val2)
    (value ?i1 ?j2 ?val3)
    (test (>= ?val1 1))
    (test (>= ?val2 1))
    (test (>= ?val3 1))
    (test (= ?i2 (+ ?i1 1)))
    (test (= ?j1 (+ ?j2 1)))
    =>
    (assert (siku (+ ?i1 1) (- ?j1 1)))
)

(defrule pattern-siku-kiri-bawah
    (open ?i1 ?j1)
    (open ?i2 ?j1)
    (open ?i1 ?j2)
    (value ?i1 ?j1 ?val1)
    (value ?i2 ?j1 ?val2)
    (value ?i1 ?j2 ?val3)
    (test (>= ?val1 1))
    (test (>= ?val2 1))
    (test (>= ?val3 1))
    (test (= ?i1 (+ ?i2 1)))
    (test (= ?j2 (+ ?j1 1)))
    =>
    (assert (siku (- ?i1 1) (+ ?j1 1)))
)

(defrule pattern-siku-kanan-bawah
    (open ?i1 ?j1)
    (open ?i2 ?j1)
    (open ?i1 ?j2)
    (value ?i1 ?j1 ?val1)
    (value ?i2 ?j1 ?val2)
    (value ?i1 ?j2 ?val3)
    (test (>= ?val1 1))
    (test (>= ?val2 1))
    (test (>= ?val3 1))
    (test (= ?i1 (+ ?i2 1)))
    (test (= ?j1 (+ ?j2 1)))
    =>
    (assert (siku (- ?i1 1) (- ?j1 1)))
)

