package tools;

import cartago.*;
import java.util.*;
import model.Position;

public class LocationArtifact extends Artifact {
    private Map<String, Position> agentPositions;
    private Map<String, Position> victimPositions;
    private Map<String, String> victimStatus; // victim -> status (discovered, monitored, rescued)

    void init() {
        agentPositions = new HashMap<>();
        victimPositions = new HashMap<>();
        victimStatus = new HashMap<>();

        defineObsProperty("agent_positions", agentPositions);
        defineObsProperty("victim_positions", victimPositions);
        defineObsProperty("victim_status", victimStatus);
    }

    @OPERATION
    void updatePosition(String agentId, double x, double y) {
        Position pos = new Position(x, y);
        agentPositions.put(agentId, pos);
        getObsProperty("agent_positions").updateValue(agentPositions);
        signal("position_updated", agentId, x, y);
    }

    @OPERATION
    void reportVictim(String victimId, double x, double y) {
        Position pos = new Position(x, y);
        victimPositions.put(victimId, pos);
        victimStatus.put(victimId, "discovered");
        getObsProperty("victim_positions").updateValue(victimPositions);
        getObsProperty("victim_status").updateValue(victimStatus);
        signal("victim_discovered", victimId, x, y);
    }

    @OPERATION
    void updateVictimStatus(String victimId, String status) {
        victimStatus.put(victimId, status);
        getObsProperty("victim_status").updateValue(victimStatus);
        signal("victim_status_updated", victimId, status);
    }
}