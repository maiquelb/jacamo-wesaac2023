package tools;

import cartago.*;
import java.util.*;
import model.Position;

public class RescueArtifact extends Artifact {
    private Map<String, String> rescueOperations; // victimId -> rescuerId
    private Map<String, Boolean> uavBuoyStatus;   // uavId -> has_buoy

    void init() {
        rescueOperations = new HashMap<>();
        uavBuoyStatus = new HashMap<>();

        defineObsProperty("rescue_operations", rescueOperations);
        defineObsProperty("uav_buoy_status", uavBuoyStatus);
    }

    @OPERATION
    void registerUAV(String uavId, boolean hasBuoy) {
        uavBuoyStatus.put(uavId, hasBuoy);
        getObsProperty("uav_buoy_status").updateValue(uavBuoyStatus);
    }

    @OPERATION
    void dropBuoy(String uavId, String victimId) {
        if (uavBuoyStatus.get(uavId)) {
            uavBuoyStatus.put(uavId, false);
            getObsProperty("uav_buoy_status").updateValue(uavBuoyStatus);
            signal("buoy_dropped", uavId, victimId);
        }
    }

    @OPERATION
    void startRescue(String victimId, String rescuerId) {
        rescueOperations.put(victimId, rescuerId);
        getObsProperty("rescue_operations").updateValue(rescueOperations);
        signal("rescue_started", victimId, rescuerId);
    }
}