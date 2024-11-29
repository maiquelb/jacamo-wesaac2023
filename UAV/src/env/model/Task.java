package model;

public class Task {
    public enum TaskType {
        SCOUT,
        DELIVER_BUOY,
        MONITOR_VICTIM,
        SHINE_TORCH,
        RESCUE
    }

    private String id;
    private TaskType type;
    private Position location;
    private String status;  // "pending", "assigned", "completed"
    private String assignedTo;
    private double priority;

    public Task(String id, TaskType type, Position location, double priority) {
        this.id = id;
        this.type = type;
        this.location = location;
        this.status = "pending";
        this.priority = priority;
    }

    // Getters and setters
    public String getId() { return id; }
    public TaskType getType() { return type; }
    public Position getLocation() { return location; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getAssignedTo() { return assignedTo; }
    public void setAssignedTo(String agent) { this.assignedTo = agent; }
    public double getPriority() { return priority; }
}