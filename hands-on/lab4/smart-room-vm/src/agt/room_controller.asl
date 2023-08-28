
// if the agent gets the goal open_voting while a voting is open, do nothing.
+!open_voting[source(Ag)] : voting_status("open")
   <- ?voting_id(Id);
      .print(Ag, " asked me to open a new voting but it voting #",Id," is open").


//if the agent gets the goal open_voting while a voting is closed, open the votation
+!open_voting[source(Ag)] 
   <- ?voting_id(Id);
      .print(Ag, " asked me to open a new voting. Openning voting #", Id+1) ;
      //TODO (Task 4.3.1): open the voting (in the voting artifact)
   

      //TODO (Exercise 4.4.2) : link the voting artifact to the dweet artifact (uncomment the lines below and add a new line to link the artifacts)
      //lookupArtifact(vote,VoteArtId);
      //lookupArtifact(dweet,DweetArtId);
      
      
   .

// This plan is triggerd when a voting result becomes available
+result(T)[artifact_name(ArtName)]
   <- .println("Creating a new goal to set temperature to ",T);
      .drop_desire(temperature(_));
      !temperature(T)
   .


{ include("temp_management.asl") }

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
