package tools;

import cartago.*;
import model.*;
import java.util.*;

public class TaskBoard extends Artifact {
    private Map<String, Task> tasks;
    private Map<String, List<String>> agentCapabilities;  // agent -> list of TaskTypes

    void init() {
        tasks = new HashMap<>();
        agentCapabilities = new HashMap<>();
        defineObsProperty("tasks", tasks);
    }

    @OPERATION
    void registerCapability(String agentId, String capability) {
        agentCapabilities.computeIfAbsent(agentId, k -> new ArrayList<>()).add(capability);
    }

    @OPERATION
    void createTask(String taskId, String type, Position location, double priority) {
        Task task = new Task(taskId, Task.TaskType.valueOf(type), location, priority);
        tasks.put(taskId, task);
        getObsProperty("tasks").updateValue(tasks);
        signal("new_task", taskId, type, location);
    }

    @OPERATION
    void assignTask(String taskId, String agentId) {
        Task task = tasks.get(taskId);
        if (task != null) {
            task.setStatus("assigned");
            task.setAssignedTo(agentId);
            getObsProperty("tasks").updateValue(tasks);
            signal("task_assigned", taskId, agentId);
        }
    }

    @OPERATION
    void completeTask(String taskId) {
        Task task = tasks.get(taskId);
        if (task != null) {
            task.setStatus("completed");
            getObsProperty("tasks").updateValue(tasks);
            signal("task_completed", taskId);

            // Generate follow-up tasks based on completion
            generateFollowUpTasks(task);
        }
    }

    private void generateFollowUpTasks(Task completedTask) {
        switch (completedTask.getType()) {
            case SCOUT:
                if (completedTask.getStatus().equals("completed")) {
                    // Create monitoring and buoy delivery tasks
                    String monitorTaskId = "monitor_" + completedTask.getId();
                    String deliveryTaskId = "delivery_" + completedTask.getId();

                    createTask(monitorTaskId, "MONITOR_VICTIM", completedTask.getLocation(), 1.0);
                    createTask(deliveryTaskId, "DELIVER_BUOY", completedTask.getLocation(), 0.8);
                }
                break;

            case DELIVER_BUOY:
                // Create torch task after buoy delivery
                String torchTaskId = "torch_" + completedTask.getId();
                createTask(torchTaskId, "SHINE_TORCH", completedTask.getLocation(), 0.7);
                break;

            case MONITOR_VICTIM:
                // Potentially create rescue task
                String rescueTaskId = "rescue_" + completedTask.getId();
                createTask(rescueTaskId, "RESCUE", completedTask.getLocation(), 0.9);
                break;
        }
    }
}