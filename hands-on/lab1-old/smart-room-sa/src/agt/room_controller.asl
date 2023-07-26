preference(20).

!start.
+!start <- !keep_temperature.

+!keep_temperature
   :  preference(P) & temperature(C) & C > P
   <- startCooling; !wait_until(P); !keep_temperature.
+!keep_temperature
   :  preference(P) & temperature(C) & C < P
   <- startHeating; !wait_until(P); !keep_temperature.
+!keep_temperature
   <- !keep_temperature.

+!wait_until(T) : temperature(T) <- stopAirConditioner.
+!wait_until(T) <- !wait_until(T).


{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
