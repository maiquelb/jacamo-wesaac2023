
// if the agent gets the goal open_voting while a voting is open, do nothing.
+!open_voting[source(Ag)] : voting_status("open")
   <- ?voting_id(Id);
      .print(Ag, " asked me to open a new voting but it voting #",Id," is open").


//if the agent gets the goal open_voting while a voting is closed, open the votation
+!open_voting[source(Ag)] 
   <- ?voting_id(Id);
      .print(Ag, "asked me to open a new voting. Openning voting #", Id+1) ;
      //TODO (Task 3.2.1): open the voting (in the voting artifact)
      open; //<== APAGAR
   .

// This plan is triggerd when a voting result becomes available
+result(T)[artifact_name(ArtName)]
   <- .println("Creating a new goal to set temperature to ",T);
      .drop_desire(temperature(_));
      !temperature(T)
   .

//tolerance(2). // used in temp_management

{ include("temp_management.asl") }

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
