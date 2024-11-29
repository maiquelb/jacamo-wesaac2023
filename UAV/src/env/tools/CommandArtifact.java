package tools;

import cartago.*;
import java.util.*;
import com.google.gson.Gson;

public class CommandArtifact extends Artifact {
    private SimulationClient simClient;

    void init() {
        simClient = new SimulationClient();
        defineObsProperty("last_command_status", "none");
    }

    @OPERATION
    void sendCommand(String agentId, String command, Object[] params) {
        Map<String, Object> paramMap = new HashMap<>();
        for (int i = 0; i < params.length; i += 2) {
            if (i + 1 < params.length) {
                paramMap.put(params[i].toString(), params[i + 1]);
            }
        }

        try {
            if (command.equals("scout")) {
                int stationIndex = Integer.parseInt(agentId.replaceAll("\\D+", "")) % 5;
                paramMap.put("start_x", 100);
                paramMap.put("start_y", 100 + (stationIndex * 150));
            }

            simClient.sendCommand(agentId, command, paramMap);
            getObsProperty("last_command_status").updateValue("success");
        } catch (Exception e) {
            getObsProperty("last_command_status").updateValue("failed: " + e.getMessage());
            failed(e.getMessage());
        }
    }

    @OPERATION
    void getAgentPositions() {
        try {
            Map<String, Object> positions = simClient.getAgentPositions();
            signal("agent_positions", positions);
        } catch (Exception e) {
            failed(e.getMessage());
        }
    }
}