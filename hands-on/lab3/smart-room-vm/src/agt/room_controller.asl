// This plan is triggered by an initial goal set in the .jcm project file.
// Options refers to the possible temperature values agents can vote for.
+!voting(Options)
   <- !open_voting(Id, Options);
      // TODO (Task 3): remove the .wait internal action and the close_voting sub-goal.
      // The voting machine will now closed automatically using the internal action.
      .wait(4000);
      !close_voting(Id)
   .

+!open_voting(Id, Options)
   <- Id = 1; // The identifier should be incremented when running multiple votes
      .concat(vote, Id, ArtNameS);
      .term2string(ArtNameT, ArtNameS);
      .all_names(AllAgents);
      .my_name(Me);
      .delete(Me, AllAgents, Voters);
      vm::makeArtifact(ArtNameS, "voting.VotingMachine", [], ArtId);
      vm::focus(ArtId);
      // TODO (Task 4): create a new artifact "dweeter" of type "social.DweetArtifact". The artifact's
      // init method takes as a parameter a dweet.io thing identifer to be used when publishing dweets.
      // E.g., the latest dweets for andrei-easss2023: https://dweet.io/get/latest/dweet/for/andrei-easss2023
      // TODO (Task 4): link the voting machine artifact with the dweeter artifact
      vm::open(Options, Voters, 4000);
      // In the current implementation, a new voting machine is created for each vote.
      // The room controller broadcasts the name of the voting machine to all agents.
      .print("Artifact created, broadcasting artifact name: ", ArtNameT);
      .broadcast(tell, open_voting(ArtNameT));
   .

+!close_voting(Id)
   <- .print("Time is out, the vote should now be closed.");
      // TODO (Tak 2): invoke close operation on the voting machine artifact
   .

// This plan is triggerd when a voting result becomes available
+vm::result(T)[artifact_name(ArtName)]
   <- .println("Creating a new goal to set temperature to ",T);
      .drop_desire(temperature(_));
      !temperature(T);
      .broadcast(untell, open_voting(ArtName));
   .

tolerance(2). // used in temp_management

{ include("temp_management.asl") }

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
