(defglobal ?*iteration* = 0)

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

(deffunction next-to (?tile1 ?tile2)
	(python_is_next_to (fact-slot-value ?tile1 location) (fact-slot-value ?tile2 location))
)

(deffunction update (?tile ?iteration)
	(if (>= (fact-slot-value ?tile iteration) ?iteration) then
		(return)
	)
	(python_print "Updating tile " (fact-slot-value ?tile location) crlf)
	(bind ?bc 0)
	(bind ?uc 0)
	(do-for-all-facts 
    ((?tile2 tile))
		(next-to ?tile ?tile2)
		(if (eq (fact-slot-value ?tile2 status) -1) then
			(bind ?uc (+ ?uc 1))
		else 
			(if (eq (fact-slot-value ?tile2 status) 5) then
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
	(bind ?newtile (modify ?tile (status 5) (iteration ?*iteration*)))
	(do-for-all-facts 
		((?tile2 tile))
		(next-to ?newtile ?tile2)
		(update ?tile2 (fact-slot-value ?newtile iteration))
	)
)

(deffunction unmark (?tile)
	(python_print "Unmarking tile at " (fact-slot-value ?tile location) crlf)
	(bind ?*iteration* (+ (fact-slot-value ?tile iteration) 1))
	(bind ?status (python_info (fact-slot-value ?tile location)))
	(bind ?newtile (modify ?tile (status ?status) (iteration ?*iteration*)))
	(do-for-all-facts 
		((?tile2 tile))
		(next-to ?newtile ?tile2)
		(update ?tile2 (fact-slot-value ?newtile iteration))
	)
)

(deffunction probe (?tile)
	(python_print "Probing tile at " (fact-slot-value ?tile location) crlf)
	(bind ?*iteration* (+ (fact-slot-value ?tile iteration) 1))
  (bind ?newtile (python_probe (fact-slot-value ?tile location)))
	(bind ?newnewtile (modify ?newtile (status 5) (iteration ?*iteration*)))
	(do-for-all-facts 
		((?tile2 tile))
		(next-to ?newnewtile ?tile2)
		(update ?tile2 (fact-slot-value ?newnewtile iteration))
	)
)


(defrule probe-if-status-eq-uc "probe when status tile = uc"
	(tile ?tile)
	(test (eq (fact-slot-value ?tile status) (fact-slot-value ?tile unknowncount)))
	=> 
	(do-for-all-facts
		((?tile2 tile))
		(next-to ?tile2 ?tile)
		(if (eq (fact-slot-value ?tile2 status) -1)
			then
			(printout t "Probing tile at " (fact-slot-value ?tile2 location) crlf)
			; (probe ?tile2)
			(break)
		)
	)
)