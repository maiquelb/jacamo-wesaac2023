!keep_temperature(20).
//!keep_temperature(35).


+!keep_temperature(P)
   :  temperature(C) & C > P
   <- startCooling; !wait_until(P); !keep_temperature(P).
+!keep_temperature(P)
   :  temperature(C) & C < P
   <- startHeating; !wait_until(P); !keep_temperature(P).
+!keep_temperature(P)
   <- !keep_temperature(P).

+!wait_until(T) : temperature(T) <- stopAirConditioner.
+!wait_until(T) <- !wait_until(T).


{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
