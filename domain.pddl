 (define (domain taxi)
	(:requirements :durative-actions :strips :typing :fluents)
	(:types player
	        car - unit
	        person
	        person unit - movable
	 		location)


	(:predicates
	    (is-enemy ?p1 ?p2 - player)
	    (has-unit ?p - player ?u - unit)
		(at ?obj1 - movable ?loc1 - location)
		(connected ?loc1 - location ?loc2 - location)
		(empty ?obj1 - unit)
		(inside ?obj1 - person ?obj2 - unit)
		(waiting ?oj1 - person)
		(destination ?obj1 - person ?loc1 - location))



	(:functions
    		(payment ?obj1 - person)
    		(distance ?locfrom - location ?locto - location)
    		(total-revenue ?obj - player))



	(:durative-action move
		:parameters (?player1 - player)
		            (?unit1 - unit)
					(?locfrom - location)
					(?locto - location)
		:duration (= ?duration (distance ?locfrom ?locto))
		:condition (and
						(at start (has-unit ?player1 ?unit1))
						(at start (at ?unit1 ?locfrom))
						(at start (connected ?locfrom ?locto)))
		:effect    (and
					    (at end (not (at ?unit1 ?locfrom)))
						(at end (at ?unit1 ?locto))))



	(:durative-action load
		:parameters (?player1 - player)
		            (?unit1 - unit)
		            (?loc - location)
		            (?per1 - person)
		:duration (= ?duration 1)
		:condition (and
						(at start (has-unit ?player1 ?unit1))
						(at start (at ?unit1 ?loc))
						(at start (at ?per1 ?loc))
						(at start (empty ?unit1))
						(at start (waiting ?per1)))
		:effect    (and
						(at end (not (empty ?unit1)))
						(at end (inside ?per1 ?unit1))))



	(:durative-action unload
		:parameters (?player1 - player)
		            (?unit1 - unit)
		            (?loc - location)
		            (?per1 - person)
		:duration (= ?duration 1)
		:condition (and
		                    (at start (has-unit ?player1 ?unit1))
							(at start (at ?unit1 ?loc))
							(at start (inside ?per1 ?unit1))
							(at start (destination ?per1 ?loc)))
		:effect 	  (and
							(at end (not (waiting ?per1)))
							(at end (not (inside ?per1 ?unit1)))
							(at end (empty ?unit1))
							(at end (increase (total-revenue ?player1) (payment ?per1))))))

