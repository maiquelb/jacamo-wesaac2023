{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

// Initial beliefs and rules
!start.

// Plans
+!start : true <-
    .my_name(Me);
    .print("UAV ",Me," starting at base");
    registerUAV(Me, true);  // Register with initial buoy
    .wait(2000);  // Wait a bit to ensure proper initialization
    !search_victims.

+!search_victims : true <-
    .my_name(Me);
    .print("Starting scouting mission in assigned region");
    sendCommand(Me, "scout", []);
    !monitor_position.
-!search_victims[error(E), error_msg(M)] <-
    .print("Error in search_victims: ", M);
    .wait(1000);
    !search_victims.

+!monitor_position : true <-
    .wait(1000);
    getAgentPositions;
    !monitor_position.

// When a victim is detected
+victim_detected(VictimId, X, Y)[source(percept)] : true <-
    .my_name(Me);
    .print("Detected victim ", VictimId, " at position (", X, ",", Y, ")");
    reportVictim(VictimId, X, Y);
    // Start monitoring victim
    sendCommand(Me, "monitor", ["x", X, "y", Y]);
    // Find nearest available boat
    ?agent_positions(Positions);
    .findall(boat(BoatId,Dist),
        (Positions[BoatId] = pos(BX,BY) &
         .substring("boat", BoatId) &
         not rescue_operations(VictimId,BoatId) &  // Check if boat not already assigned
         Dist = math.sqrt((X-BX)**2 + (Y-BY)**2)),
        Boats);
    if (.length(Boats) > 0) {
        .min_by_second(Boats, boat(NearestBoat,_));
        .print("Requesting help from nearest boat: ", NearestBoat);
        .send(NearestBoat, tell, rescue_needed(VictimId, X, Y));
        +monitoring(VictimId, NearestBoat);
    } else {
        .print("No available boats found, continuing to monitor victim");
    }.

// When boat arrives at victim
+boat_arrived(VictimId)[source(Boat)] : monitoring(VictimId, Boat) <-
    .my_name(Me);
    .print("Boat arrived at victim location, stopping monitoring");
    -monitoring(VictimId, Boat);
    sendCommand(Me, "scout", []).  // Resume scouting

+!return_to_base : true <-
    .my_name(Me);
    sendCommand(Me, "return", []).
-!return_to_base[error(E), error_msg(M)] <-
    .print("Error returning to base: ", M);
    .wait(1000);
    !return_to_base.