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
    defineObsProperty("timeout", this.timeout);
    defineObsProperty("voting_id",0); 
    defineObsProperty("voting_status","closed"); 
  }

  @OPERATION
  public void open() {
    // Checks that voting is closed — and do nothing if not
    if (getObsProperty("voting_status").getValue().equals("closed")) {
    
      this.voters = new ArrayList<>();
      this.votes = new ArrayList<>();

      this.voters.clear(); //when the poll opens, there is no voter yet

      getObsProperty("voting_status").updateValue("open");     
      
      int currentVotingId =  getObsProperty("voting_id").intValue();
      
      getObsProperty("voting_id").updateValue(currentVotingId+1); 

      
    }
  }

  @OPERATION
  public void vote(int vote) {
    // Checks that voting is open — and throws a failure if not
    if (getObsProperty("voting_status").getValue().equals("close")) {
      failed("The voting machine is closed!");
    }
    
    // Checks if the agent invoking the operation has already voted
    if(voters.contains(getCurrentOpAgentId().getAgentName()))
        failed("You've already voted!");

    // If everything is fine, accept the vote
    votes.add((Integer) vote);
    voters.add(getCurrentOpAgentId().getAgentName());        
    log("recorded vote " + vote + " - " + getCurrentOpAgentId().getAgentName());
  }

  @OPERATION  
  public void close() {
    
    getObsProperty("voting_status").updateValue("closed");

    int result = computeResult(); //the result value is stored in the variable "result"
    
    signal("result",result); 
     
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