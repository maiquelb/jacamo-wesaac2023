package tools;

import cartago.*;
import java.util.*;

public class RescueGoalArtifact extends Artifact {
    private int totalVictims;
    private int rescuedVictims;
    private Map<String, String> victimAssignments; // victim -> rescuer

    void init(int numVictims) {
        totalVictims = numVictims;
        rescuedVictims = 0;
        victimAssignments = new HashMap<>();

        defineObsProperty("total_victims", totalVictims);
        defineObsProperty("rescued_victims", rescuedVictims);
        defineObsProperty("mission_complete", false);
    }

    @OPERATION
    void assignVictim(String victimId, String rescuerId) {
        victimAssignments.put(victimId, rescuerId);
        signal("victim_assigned", victimId, rescuerId);
    }

    @OPERATION
    void victimRescued(String victimId) {
        rescuedVictims++;
        victimAssignments.remove(victimId);
        getObsProperty("rescued_victims").updateValue(rescuedVictims);

        if (rescuedVictims == totalVictims) {
            getObsProperty("mission_complete").updateValue(true);
            signal("mission_completed");
        }

        signal("victim_rescued", victimId);
    }

    @OPERATION
    void getRescuerForVictim(String victimId, OpFeedbackParam<String> rescuer) {
        rescuer.set(victimAssignments.get(victimId));
    }
}