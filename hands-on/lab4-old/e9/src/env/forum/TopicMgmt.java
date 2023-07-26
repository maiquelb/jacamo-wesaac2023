package forum;

import cartago.*;
import java.util.ArrayList;
import java.util.List;

public class TopicMgmt extends Artifact {

	private ArrayList<String> messages;

	void init(String topic) {
		defineObsProperty("topic", topic);
		defineObsProperty("post", "");
		this.messages = new ArrayList<>();
	}

	@OPERATION
	void submitPost(String msg) {
		this.messages.add(msg);
	}

	@OPERATION
	void retrievePost(int index) {
		String msg = "";
		if (!this.messages.isEmpty()) {
			if ((index < 0) || (index >= this.messages.size())) {
				msg = this.messages.get(this.messages.size() - 1);
			} else {
				msg = this.messages.get(index);
			}
		}
		getObsProperty("post").updateValue(msg);
	}

}