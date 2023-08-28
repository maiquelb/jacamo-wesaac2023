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
  private int timeout = 10000;

  public void init() {
    Object[] options = {15,20,25,30};
    ListTerm optionTerms = createOptionTermsList(options);
    defineObsProperty("options",optionTerms); 
    defineObsProperty("timeout", this.timeout); 
    defineObsProperty("voting_id",0); 
    // TODO (Task 4.1.1): define a status property with values "open"/"closed"
  }

  @OPERATION
  public void open() {
    // Checks that voting is closed — and do nothing if not
    if (getObsProperty("voting_status").getValue().equals("closed")) {
    
      this.voters = new ArrayList<>();
      this.votes = new ArrayList<>();

      this.voters.clear(); //when the poll opens, there is no voter yet
      
      int currentVotingId =  getObsProperty("voting_id").intValue();
      getObsProperty("voting_id").updateValue(currentVotingId+1); 

      // TODO (Task 4.1.2): update the "voting_status" observable property to "open" to announce that voting is open


      // start the countdown to close the voting
      execInternalOp("countdown");

    }
  }

  @OPERATION
  public void vote(int vote) {
    // Checks that voting is open — and throws a failure if not
    if (getObsProperty("voting_status").getValue().equals("closed")) {
      failed("The voting machine is closed!");
    }
    
    // Checks if the agent invoking the operation has already voted
    if(voters.contains(getCurrentOpAgentId().getAgentName()))
        failed("You've already voted!");

    // If everithing is fine, accept the vote
    votes.add((Integer) vote);
    voters.add(getCurrentOpAgentId().getAgentName());        
    log("recorded vote " + vote + " - " + getCurrentOpAgentId().getAgentName());
  }


   @INTERNAL_OPERATION
  public void close() {
    
    // TODO (Task 4.1.2): update the "voting_status" observable property to "closed"

    int result = computeResult(); //the result value is stored in the variable "result"

    // TODO (Task 4.1.2): use a signal called "result" to expose the result (stored in the "result" variable )
    

    

    // TODO (Task 4.4.2): uncomment this block after completing the room controller agent program
    /*
     try {
       log("Publishing the result to dweet.io: " + result);
       execLinkedOp("publish-port", "dweet", String.valueOf(result));
     } catch (OperationException e) {W
       log("Failed to publish the result: " + e.getMessage());
     }
     
    log("Voting is closed. The result is " + result);
    */
  }
   

  // TODO (Task 3): implement an internal operation with a countdown. The internal operation should be
  // invoked at the end of the open() operation.
  @INTERNAL_OPERATION
  private void countdown() {
    await_time(this.timeout);

    log("Voting is closing!");

    execInternalOp("close");
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
