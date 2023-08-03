package social;

import java.io.IOException;

import org.apache.hc.client5.http.classic.HttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.HttpHeaders;
import org.apache.hc.core5.http.HttpResponse;
import org.apache.hc.core5.http.HttpStatus;
import org.apache.hc.core5.http.Method;
import org.apache.hc.core5.http.io.entity.StringEntity;
import org.apache.hc.core5.http.message.BasicClassicHttpRequest;

import cartago.Artifact;
import cartago.LINK;
import cartago.OPERATION;

public class DweetArtifact extends Artifact {
  private final static String DWEET_ENDPOINT = "https://dweet.io/dweet/for/";

  private String dweetEndpoint;

  void init(String username) {
    dweetEndpoint = DWEET_ENDPOINT + username;
  }

  @LINK
  @OPERATION
  public void dweet(String message) {
    BasicClassicHttpRequest request = new BasicClassicHttpRequest(Method.POST, dweetEndpoint);

    // Note: Dweet.io will ignore the payload if the content type is not set 
    request.setHeader(HttpHeaders.CONTENT_TYPE, "application/json");
    request.setEntity(new StringEntity("{ \"text\" : \"" + message + "\" }"));

    try {
      HttpClient client = HttpClients.createDefault();
      HttpResponse response = client.execute(request);

      // If the request is successful, it will return 200 (not 201)
      if (response.getCode() != HttpStatus.SC_OK) {
        failed("Dweet status code: " + response.getCode());
      }
    } catch (IOException e) {
      log("IOException while posting tweet: " + e.getMessage());
    }
  }
}