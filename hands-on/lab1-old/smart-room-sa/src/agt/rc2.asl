preference(20).

!start.
+!start <- !keep_temperature.

+!keep_temperature
   :  preference(P) & hvac::temperature(C) & C > P
   <- startCooling; !wait_until(P); !keep_temperature.
+!keep_temperature
   :  preference(P) & hvac::temperature(C) & C < P
   <- startHeating; !wait_until(P); !keep_temperature.
+!keep_temperature
   <- !keep_temperature.

+!wait_until(T) : hvac::temperature(CT) & math.abs(T-CT) < 3  <- stopAirConditioner.
+!wait_until(T) <- !wait_until(T). // busy waiting (!)


{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
