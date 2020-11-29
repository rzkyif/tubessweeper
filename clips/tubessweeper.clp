(defglobal ?*iteration* = 0)

(deftemplate nextto
	(slot location1
		(type SYMBOL)
		(default ?NONE)
	)
	(slot location2
		(type SYMBOL)
		(default ?NONE)
	)
)

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
	(slot clearcount
		(type INTEGER)
		(default 0)
	)
)

(deffunction next-to (?tile1 ?tile2)
	(neq 
		(length 
			(find-fact ((?nt nextto))
				(or
					(and
						(eq 
							(fact-slot-value ?nt location1) 
							(fact-slot-value ?tile1 location)
						)
						(eq 
							(fact-slot-value ?nt location2) 
							(fact-slot-value ?tile2 location)
						)
					)
					(and
						(eq 
							(fact-slot-value ?nt location2) 
							(fact-slot-value ?tile1 location)
						)
						(eq 
							(fact-slot-value ?nt location1) 
							(fact-slot-value ?tile2 location)
						)
					)
				)
			)
		)
		0
	)
)

(deffunction update (?tile ?iteration)
	(if (>= (fact-slot-value ?tile iteration) ?iteration) then
		(return)
	)
	(printout t "Updating tile " (fact-slot-value ?tile location) crlf)
	(bind ?zc 0)
	(bind ?oc 0)
	(do-for-all-facts ((?tile2 tile))
		(next-to ?tile ?tile2)
		(if (eq (fact-slot-value ?tile2 status) 1) then
			(bind ?oc (+ ?oc 1))
		else 
			(if (eq (fact-slot-value ?tile2 status) 0) then
				(bind ?zc (+ ?zc 1))
			)
		)
	)
	(bind ?newtile (modify ?tile (bombcount ?zc) (clearcount ?oc) (iteration ?iteration)))
	(do-for-all-facts 
		((?tile2 tile))
		(next-to ?newtile ?tile2)
		(update ?tile2 ?iteration)
	)
)

(deffunction mark (?tile)
	(printout t "Marking tile at " (fact-slot-value ?tile location) crlf)
	(bind ?*iteration* (+ (fact-slot-value ?tile iteration) 1))
	(bind ?newtile (modify ?tile (status 5) (iteration ?*iteration*)))
	(do-for-all-facts 
		((?tile2 tile))
		(next-to ?newtile ?tile2)
		(update ?tile2 (fact-slot-value ?newtile iteration))
	)
)

(deffunction unmark (?tile)
	(printout t "Unmarking tile at " (fact-slot-value ?tile location) crlf)
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
	(printout t "Probing tile at " (fact-slot-value ?tile location) crlf)
	(bind ?*iteration* (+ (fact-slot-value ?tile iteration) 1))
  (bind ?newtile (python_probe (fact-slot-value ?tile location)))
	(bind ?newtile (modify ?tile (status 5) (iteration ?*iteration*)))
	(do-for-all-facts 
		((?tile2 tile))
		(next-to ?newtile ?tile2)
		(update ?tile2 (fact-slot-value ?newtile iteration))
	)
)

(defrule startup
	=>
	(assert (tile (location x0y0)))
	(assert (tile (location x0y1)))
	(assert (tile (location x1y0)))
	(assert (tile (location x1y1)))
	(assert (nextto (location1 x0y0) (location2 x1y0)))
	(assert (nextto (location1 x0y0) (location2 x0y1)))
	(assert (nextto (location1 x1y1) (location2 x1y0)))
	(assert (nextto (location1 x1y1) (location2 x0y1)))
)
