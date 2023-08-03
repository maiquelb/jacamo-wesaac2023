// Checks that the current temperature is close to the target 
// temperature (+/- some tolerance level)
temperature_in_range(T)
	:- not now_is_colder_than(T) & not now_is_warmer_than(T).

// Checks that the current temperature is not lower than the 
// target temperature above a tolerance level
now_is_colder_than(T)
	//:- temperature(C) & tolerance(DT) & (T - C) > DT.
	:- temperature(C) & C < T.

// Checks that the current temperature is not higher than the 
// target temperature above a tolerance level
now_is_warmer_than(T)
	//:- temperature(C) & tolerance(DT) & (C - T) > DT.
	:- temperature(C) & C > T.

+!temperature(T): temperature_in_range(T)
	<- 	println("Temperature achieved: ",T).

/* The following plans are used to heat the room */
+!temperature(T): now_is_colder_than(T)
	<-  println("It is too cold -> heating...");
	    startHeating;
		!heat_until(T).

+!heat_until(T): temperature_in_range(T)
 	<-  stopAirConditioner;
 		println("Temperature achieved ",T).

+!heat_until(T): now_is_colder_than(T)
	<-  .wait(100);
	    !heat_until(T).

+!heat_until(T): now_is_warmer_than(T)
	<-  .wait(100);
	    !temperature(T).

/* The following plans are used to cool down the room */
+!temperature(T): now_is_warmer_than(T)
	<-  println("It is too hot -> cooling until ", T);
	    startCooling;
		!cool_until(T).

+!cool_until(T): temperature_in_range(T)
 	<- stopAirConditioner;
 	   println("Temperature achieved ",T).

+!cool_until(T): now_is_warmer_than(T)
	<-  .wait(100);
	    !cool_until(T).

+!cool_until(T): now_is_colder_than(T)
	<-  .wait(100);
	    !temperature(T).

