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


/**
 * This class implements a voting machine used to vote among a number of options espressed as integer
 * values. In our scenario, agents instantiate and use voting machines to reach consensus on the
 * target temperature to be set in a shared room.
 */
@ARTIFACT_INFO(
  outports = {
    @OUTPORT(name = "publish-port")
  }
)
public class VotingMachine extends Artifact {
  private List<String> voters;
  private List<Integer> votes;
  private int timeout;

  public void init() {
    // TODO (Task 1): define a status property with values open/closed
  }

  @OPERATION
  public void open(Object[] options, Object[] voters, int timeout) {
    this.voters = new ArrayList<>();
    this.votes = new ArrayList<>();

    for (Object v: voters) {
      this.voters.add(v.toString());
    }

    ListTerm optionTerms = createOptionTermsList(options);
    // TODO (Task 1): expose the options in optionTerms as an observable property named "options"

    this.timeout = timeout;
    defineObsProperty("timeout", this.timeout);

    // TODO (Task 1): update the "status" observable property to "open" to announce that voting is open

    // TODO (Task 3): uncomment this line after implementing the countfown internal operation
    // execInternalOp("countdown");
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

    // TODO (Task 1): expose the result as an observable property named "result"

    // TODO (Task 1): update the "status" observable property to "close" to announce that voting is closed

    // TODO (Task 4): uncomment this block after completing the room controller agent program
    // try {
      // log("Publishing the result to dweet.io: " + result);
      // execLinkedOp("publish-port", "dweet", String.valueOf(result));
    // } catch (OperationException e) {
    //   log("Failed to publish the result: " + e.getMessage());
    // }
  }

  // TODO (Task 3): implement an internal operation with a countdown. The internal operation should be
  // invoked at the end of the open() operation.
  @INTERNAL_OPERATION
  private void countdown() {
    log("Voting is closing!");

    // TODO (Task 3): Use the await_time method to wait for the specified timeout, then invoke the
    // close operation.
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
