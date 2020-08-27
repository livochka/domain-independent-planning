(define (domain taxi)
	(:requirements  :duration-inequalities :durative-actions :strips :typing :fluents  :adl :equality :preferences )

	(:types player
	        car - unit
	        person
	 		location)


	(:predicates
	    (is-delivered ?pers - person ?pl - player)
	    (is-enemy ?p1 ?p2 - player)
	    (has-unit ?p - player ?u - unit)
		(at-unit ?obj1 - unit ?loc1 - location)
		(at-person ?obj1 - person ?loc1 - location)
		(connected ?loc1 - location ?loc2 - location)
		(empty ?obj1 - unit)
		(inside ?obj1 - person ?obj2 - unit)
		(destination ?obj1 - person ?loc1 - location)
		(carry ?pl - player ?p - person))



	(:functions
    		(payment ?obj1 - person)
    		(distance ?locfrom - location ?locto - location))



	(:durative-action move
		:parameters (?player1 - player ?unit1 - unit ?locfrom - location ?locto - location)
		:duration (= ?duration (distance ?locfrom ?locto))
		:condition (and
						(over all (has-unit ?player1 ?unit1))
						(at start (at-unit ?unit1 ?locfrom))
						(over all (connected ?locfrom ?locto)))
		:effect    (and
					    (at start (not (at-unit ?unit1 ?locfrom)))
						(at end (at-unit ?unit1 ?locto))))



	(:durative-action load
		:parameters (?player1 - player ?unit1 - unit ?loc - location ?per1 - person)
		:duration (= ?duration 1)
		:condition (and
						(over all (has-unit ?player1 ?unit1))
						(at start (at-unit ?unit1 ?loc))
						(at start (at-person ?per1 ?loc))
						(at start (empty ?unit1))
		            )
		:effect    (and
						(at start (not (empty ?unit1)))
						(at start (not (at-person ?per1 ?loc)))
						(at end (inside ?per1 ?unit1))
						(at end (carry ?player1 ?per1)))
					)



	(:durative-action unload

		:parameters (?player1 - player ?unit1 - unit ?loc - location ?per1 - person)
		:duration (= ?duration 1)
		:condition (and
		                    (over all (has-unit ?player1 ?unit1))
							(at start (at-unit ?unit1 ?loc))
							(at start(carry ?player1 ?per1))
							(at start (inside ?per1 ?unit1))
							(over all (destination ?per1 ?loc)))
		:effect 	  (and
							(at end (not (inside ?per1 ?unit1)))
							(at end (empty ?unit1))
							(at end (is-delivered ?per1 ?player1)))))

