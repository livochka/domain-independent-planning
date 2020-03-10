(define (domain taxi)
	(:requirements :strips :typing) 
	(:types car person - movable
	 		location)


	(:predicates
		(at ?obj1 - movable ?loc1 - location)
		(connected ?loc1 - location ?loc2 - location)
		(empty ?obj1 - car)
		(inside ?obj1 - person ?obj2 - car)
		(waiting ?oj1 - person)
		(destination ?obj1 - person ?loc1 - location)
	)


	(:functions
    		(payment ?obj1 - person)
    		(total-revenue))

    (:functions
    		(distance ?loc1 - location ?loc2 - location)
    		(total-distance))


	(:action move
		:parameters (?car1 - car ?locfrom - location ?locto - location)
		:precondition (and 
							(at ?car1 ?locfrom)
							(connected ?locfrom ?locto))
		:effect 	  (and
							(not (at ?car1 ?locfrom))
							(at ?car1 ?locto))



	(:action load
		:parameters (?car1 - car ?loc - location ?per1 - person)
		:precondition (and 
							(at ?car1 ?loc)
							(at ?per1 ?loc)
							(empty ?car1)
							(waiting ?per1))
		:effect 	  (and
							(not (empty ?car1))
							(inside ?per1 ?car1)))



	(:action unload
		:parameters (?car1 - car ?loc - location ?per1 - person)
		:precondition (and 
							(at ?car1 ?loc)
							(inside ?per1 ?car1)
							(destination ?per1 ?loc))
		:effect 	  (and
							(not (waiting ?per1))
							(not (inside ?per1 ?car1))
							(empty ?car1)
							(increase (total-revenue) (payment ?per1)))

