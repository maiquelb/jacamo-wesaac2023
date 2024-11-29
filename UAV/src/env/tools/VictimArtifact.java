package tools;

import cartago.*;
import model.Position;
import java.util.ArrayList;
import java.util.List;

public class VictimArtifact extends Artifact {
    private List<Position> victims;

    void init() {
        victims = new ArrayList<>();
        defineObsProperty("victims_found", 0);
        defineObsProperty("victims_locations", victims);
    }

    @OPERATION
    void reportVictim(Position pos) {
        victims.add(pos);
        ObsProperty victimsCount = getObsProperty("victims_found");
        victimsCount.updateValue(victimsCount.intValue() + 1);

        ObsProperty victimsLoc = getObsProperty("victims_locations");
        victimsLoc.updateValue(victims);

        signal("victim_found", pos);
    }

    @OPERATION
    void victimRescued(Position pos) {
        victims.remove(pos);
        ObsProperty victimsCount = getObsProperty("victims_found");
        victimsCount.updateValue(victimsCount.intValue() - 1);

        ObsProperty victimsLoc = getObsProperty("victims_locations");
        victimsLoc.updateValue(victims);

        signal("victim_rescued", pos);
    }
}