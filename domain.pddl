(define (domain taxi)
	(:requirements :durative-actions :strips :typing :fluents) 
	(:types player
	        car - unit
	        person - passenger
	        passenger, unit - movable
	 		location)


	(:predicates
	    (is-enemy ?p1 ?p2 - player) 
	    (has-unit ?p - player ?u - unit)
		(at ?obj1 - movable ?loc1 - location)
		(connected ?loc1 - location ?loc2 - location)
		(empty ?obj1 - unit)
		(inside ?obj1 - person ?obj2 - unit)
		(waiting ?oj1 - person)
		(destination ?obj1 - person ?loc1 - location)
		
	)


	(:functions
    		(payment ?obj1 - person)
    		(distance ?locfrom - location ?locto - location)
    		(total-revenue ?obj - player))




	(:durative-action move
		:parameters (?player1 - player ?unit1 - unit 
					 ?locfrom - location ?locto - location)
		:duration (= ?distance (distance ?locfrom ?locto))
		:precondition (and  
							(has-unit ?player1 ?unit1)
							(at ?unit1 ?locfrom)
							(connected ?locfrom ?locto))
		:effect 	  (and
							(not (at ?unit1 ?locfrom))
							(at ?unit1 ?locto)))



	(:action load
		:parameters (?player1 - player ?unit1 - unit ?loc - location ?per1 - person)
		:precondition (and 
							(has-unit ?player1 ?unit1)
							(at ?unit1 ?loc)
							(at ?per1 ?loc)
							(empty ?unit1)
							(waiting ?per1))
		:effect 	  (and
							(not (empty ?unit1))
							(inside ?per1 ?unit1)))



	(:action unload
		:parameters (?player1 - player ?unit1 - unit ?loc - location ?per1 - person)
		:precondition (and 
							(at ?unit1 ?loc)
							(inside ?per1 ?unit1)
							(destination ?per1 ?loc))
		:effect 	  (and
							(not (waiting ?per1))
							(not (inside ?per1 ?unit1))
							(empty ?unit1)
							(increase (total-revenue) (payment ?per1)))

