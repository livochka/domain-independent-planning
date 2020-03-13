(define (problem taxi-example)

	(:domain taxi)
	(:objects player1 player2- player
			  car1 car2 - unit
			  pas1 - passenger
			  loc1 loc2 loc3 loc4 loc5 - location)

	(:init 
		   (has-unit player1 car1)
		   (has-unit player2 car2)
		   (is-enemy player1 player2)
		   (at car1 loc1)
		   (empty car1) 
		   (at pas1 loc2)
		   (waiting pas1)
		   (= (total-revenue) 0)
		   (destination pas1 loc5) 
		   (= (payment pas1) 100)
		   (connected loc1 loc2)
		   (= (distance loc1 loc2) 2)
		   (connected loc2 loc4)
		   (= (distance loc2 loc4) 2)
		   (connected loc4 loc3)
		   (= (distance loc4 loc3) 2)
		   (connected loc3 loc1)
		   (= (distance loc3 loc1) 2)
		   (connected loc1 loc5)
		   (= (distance loc1 loc5) 1)
		   (connected loc2 loc5)
		   (= (distance loc2 loc5) 1)
		   (connected loc3 loc5)
		   (= (distance loc3 loc5) 1)
		   (connected loc4 loc5)
		   (= (distance loc4 loc5) 1)
		   )

    (:goal (at pas1 loc5)) 

	(:metric maximize (total-revenue)))