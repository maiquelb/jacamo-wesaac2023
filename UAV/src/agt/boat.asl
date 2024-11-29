{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

// Initial beliefs and rules
!start.

// Plans
+!start : true <-
    .my_name(Me);
    .print("Boat ",Me," starting at base");
    !wait_for_rescue.

+!wait_for_rescue : true <-
    .wait(500);
    !wait_for_rescue.

// When receiving rescue request from UAV
+rescue_needed(VictimId, X, Y)[source(UAV)] : true <-
    .my_name(Me);
    .print("Received rescue request from ", UAV, " for victim ", VictimId);
    startRescue(VictimId, Me);
    sendCommand(Me, "goto", ["x", X, "y", Y]);
    +rescuing(VictimId).

// When reached victim location
+at_victim_location(VictimId)[source(percept)] : rescuing(VictimId) <-
    .my_name(Me);
    .print("Reached victim ", VictimId, ", starting rescue operation");
    // Notify monitoring UAV
    .broadcast(tell, boat_arrived(VictimId));
    updateVictimStatus(VictimId, "rescued");
    -rescuing(VictimId);
    // Return to nearest dock
    sendCommand(Me, "return", []).

// When reached dock with victim
+at_dock[source(percept)] : true <-
    .my_name(Me);
    .print("Returned to dock, victim rescued successfully");
    !wait_for_rescue.