;   VARIABEL GLOBAL

(defglobal ?*iteration* = 0)

;   TEMPLATE

(deftemplate tile
	(slot location
		(type SYMBOL)
		(default ?NONE)
	)
	(slot status
		(type INTEGER)
		(default -1)
	)
	(slot iteration
		(type INTEGER)
		(default 0)
	)
	(slot bombcount
		(type INTEGER)
		(default 0)
	)
	(slot unknowncount
		(type INTEGER)
		(default 0)
	)
)

;   FUNGSI

(deffunction next-to (?tile1 ?tile2)
	(python_is_next_to (fact-slot-value ?tile1 location) (fact-slot-value ?tile2 location))
)

(deffunction update (?tile ?iteration)
	(if (>= (fact-slot-value ?tile iteration) ?iteration) then
		(return)
	)
	(bind ?bc 0)
	(bind ?uc 0)
	(do-for-all-facts 
    ((?tile2 tile))
		(next-to ?tile ?tile2)
		(if (eq ?tile2:status -1) then
			(bind ?uc (+ ?uc 1))
		else 
			(if (eq ?tile2:status 5) then
				(bind ?bc (+ ?bc 1))
			)
		)
	)
	(bind ?newtile (modify ?tile (bombcount ?bc) (unknowncount ?uc) (iteration ?iteration)))
	(do-for-all-facts 
		((?tile2 tile))
		(next-to ?newtile ?tile2)
		(update ?tile2 ?iteration)
	)
)

(deffunction mark (?tile)
	(python_print "Marking tile at " (fact-slot-value ?tile location) crlf)
	(bind ?*iteration* (+ (fact-slot-value ?tile iteration) 1))
	(bind ?newtile (python_mark (fact-slot-value ?tile location)))
	(update ?newtile ?*iteration*)
)

(deffunction probe (?tile)
	(python_print "Probing tile at " (fact-slot-value ?tile location) crlf)
	(bind ?*iteration* (+ (fact-slot-value ?tile iteration) 1))
  (bind ?newtile (python_probe (fact-slot-value ?tile location)))
	(update ?newtile ?*iteration*)
)

;   RULE

(defrule start-condition
	?tile<-(tile (location x0y0) (status -1))
	=>
	(probe ?tile)
)


(defrule win-condition
	(game-finished ?status)
	=>
	(if (eq ?status win) then
		(python_print "Bot successfully finished the game!")
	else 
		(python_print "Bot failed and probed a bomb!")
	)
)

(defrule probe-if-status-eq-bc "probe when status tile = uc"
	(not (game-finished))
	?tile<-(tile (status ~-1&~0))
	(test (eq (fact-slot-value ?tile status) (fact-slot-value ?tile bombcount)))
	(test (neq (fact-slot-value ?tile unknowncount) 0))
	=> 
	(do-for-all-facts
		((?tile2 tile))
		(next-to ?tile2 ?tile)
		(if (eq (fact-slot-value ?tile2 status) -1) 
			then
			(printout t "Probing tile at " (fact-slot-value ?tile2 location) crlf)
			(probe ?tile2)
			(break)
		)
	)
)

(defrule mark-if-status-eq-uc "mark neighboor tile when status tile = uc"
	(not (game-finished))
	?tile<-(tile (status ~-1&~0))
	(test 
		(eq 
				(fact-slot-value ?tile unknowncount) 
			(- 
				(fact-slot-value ?tile status) 
				(fact-slot-value ?tile bombcount)
			)
		)
	)
	(test 
		(neq 
		(
			fact-slot-value ?tile unknowncount) 
			0
		)
	)
	=>
	(do-for-all-facts
		((?tile2 tile))
		(next-to ?tile2 ?tile)
		(if (eq (fact-slot-value ?tile2 status) -1)
			then
			(printout t "marking tile at " (fact-slot-value ?tile2 location) crlf)
			(mark ?tile2)
			(break)
		)
	)
)
