package voting;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import cartago.ARTIFACT_INFO;
import cartago.Artifact;
import cartago.INTERNAL_OPERATION;
import cartago.OPERATION;
import cartago.OUTPORT;
import cartago.OperationException;
import jason.asSyntax.ASSyntax;
import jason.asSyntax.ListTerm;
import jason.asSyntax.parser.ParseException;


public class VotingMachine extends Artifact {
  private List<String> voters;
  private List<Integer> votes;
  private int timeout;

  public void init() {
    defineObsProperty("status", "closed");
    defineObsProperty("options", "");
  }

  @OPERATION
  public void open(Object[] options, Object[] voters, int timeout) {
    this.voters = new ArrayList<>();
    this.votes = new ArrayList<>();
    this.timeout = timeout;

    ListTerm optionTerms = createOptionTermsList(options);

    for (Object v: voters) {
      this.voters.add(v.toString());
    }

    //defineObsProperty("options", optionTerms);
    defineObsProperty("timeout", this.timeout);
    getObsProperty("options").updateValue(optionTerms);
    getObsProperty("status").updateValue("open");
  }

  @OPERATION
  public void vote(int vote) {
    // Checks that voting is open — and throws a failure if not
    if (getObsProperty("status").getValue().equals("close")) {
      failed("The voting machine is closed!");
    }

    // Checks if the agent invoking the operation has already voted
    if (voters.remove(getCurrentOpAgentId().getAgentName())) {
      // If not, then accept the vote
      votes.add((Integer) vote);
    } else {
      // Otherwise, throw a failure
      failed("You've already voted!");
    }
  }

  @OPERATION
  public void close() {
    int result = computeResult();

    defineObsProperty("result", result);
    getObsProperty("status").updateValue("closed");
  }

  @INTERNAL_OPERATION
  private void countdown() {
    await_time(timeout);
    log("Voting is closing!");
    close();
  }

  // This method is used to convert datum from Jason to Java
  private ListTerm createOptionTermsList(Object[] options) {
    ListTerm optionTerms = ASSyntax.createList();

    for (Object o: options) {
      try {
        optionTerms.add(ASSyntax.parseTerm(o.toString()));
      } catch (ParseException e) {
        log(e.getMessage());
      }
    }

    return optionTerms;
  }

  // This method is used to compute the winner
  private int computeResult() {
    // Aggregate the votes
    Map<Integer, Long> counts = votes.stream().collect(Collectors.groupingBy(x -> x, Collectors.counting()));
    // Returns the option with most votes
    Integer result = Collections.max(counts.entrySet(), Map.Entry.comparingByValue()).getKey();

    return result;
  }
}