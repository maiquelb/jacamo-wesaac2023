package tools;

import com.google.gson.Gson;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.io.IOException;
import java.util.Map;

public class SimulationClient {
    private String baseUrl;
    private HttpClient client;
    private Gson gson;

    public SimulationClient() {
        this.baseUrl = "http://localhost:5000";  // Default URL
        this.client = HttpClient.newHttpClient();
        this.gson = new Gson();
    }

    public void sendCommand(String agentId, String command, Map<String, Object> params) {
        try {
            Map<String, Object> requestBody = Map.of(
                "agent_id", agentId,
                "command", command,
                "params", params
            );

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/command"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(gson.toJson(requestBody)))
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() != 200) {
                throw new RuntimeException("Command failed: " + response.body());
            }
        } catch (Exception e) {
            throw new RuntimeException("Error sending command: " + e.getMessage());
        }
    }

    public Map<String, Object> getAgentPositions() {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/agents"))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                return gson.fromJson(response.body(), Map.class);
            } else {
                throw new RuntimeException("Failed to get positions: " + response.body());
            }
        } catch (Exception e) {
            throw new RuntimeException("Error getting positions: " + e.getMessage());
        }
    }
}