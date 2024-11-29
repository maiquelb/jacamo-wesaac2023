/* Initial beliefs and rules */
all_victims_count(10).

/* Plans */
+!start_mission
    : true <-
    .print("Starting rescue mission");
    .all_names(Agents);
    for (.member(Agent, Agents)) {
        if (.substring("uav", Agent)) {
            .send(Agent, achieve, init);
        }
    }.

+!assign_scouts
    : true <-
    .all_names(Agents);
    for (.member(Agent, Agents)) {
        if (.substring("uav", Agent)) {
            .send(Agent, achieve, start_scouting);
        }
    }.

+victim_found(VictimId, Pos)[source(Scout)]
    : true <-
    .print("Victim ", VictimId, " found by ", Scout);
    !assign_rescue(VictimId, Pos).

+!assign_rescue(VictimId, Pos)
    : true <-
    .findall(Boat, .substring("boat", Boat), Boats);
    !calculate_best_rescuer(Boats, Pos, BestBoat);
    assignVictim(VictimId, BestBoat);
    .send(BestBoat, achieve, rescue_victim(VictimId, Pos)).

+victim_rescued(VictimId)
    : true <-
    .print("Victim ", VictimId, " has been rescued");
    !check_mission_complete.

+!check_mission_complete
    : rescued_victims(R) & all_victims_count(R) <-
    .print("All victims have been rescued!");
    .broadcast(tell, mission_complete).