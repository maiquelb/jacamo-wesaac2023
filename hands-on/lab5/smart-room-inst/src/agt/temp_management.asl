temperature_in_range(T)
	:- not now_is_colder_than(T) & not now_is_warmer_than(T).

now_is_colder_than(T)
	:- temperature(C) & tolerance(DT) & (T - C) > DT.

now_is_warmer_than(T)
	:- temperature(C) & tolerance(DT) & (C - T) > DT.

+!temperature(T): temperature_in_range(T)
	<- 	.print("Temperature achieved: ",T).

+!temperature(T): now_is_colder_than(T)
	<-  .print("It is too cold -> heating...");
	    startHeating;
		!heat_until(T).

+!heat_until(T): temperature_in_range(T)
 	<-  stopAirConditioner;
 		.print("Temperature achieved ",T).

+!heat_until(T): now_is_colder_than(T)
	<-  .wait(100);
	    !heat_until(T).

+!heat_until(T): now_is_warmer_than(T)
	<-  .wait(100);
	    !temperature(T).

+!temperature(T): now_is_warmer_than(T)
	<-  .print("It is too hot -> cooling...");
	    startCooling;
		!cool_until(T).

+!cool_until(T): temperature_in_range(T)
 	<- stopAirConditioner;
 	   .print("Temperature achieved ",T).

+!cool_until(T): now_is_warmer_than(T)
	<-  .wait(100);
	    !cool_until(T).

+!cool_until(T): now_is_colder_than(T)
	<-  .wait(100);
	    !temperature(T).
