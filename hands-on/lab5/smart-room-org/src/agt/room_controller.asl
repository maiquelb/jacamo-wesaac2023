options([15,20,25,30]).


+!options_announced
   <- ?options(Options) ;
      .broadcast(tell, options(Options)) .


// if the voting is open, do nothing.
+!voting_open : voting_status("open").


//if the voting is closed, open the votation
+!voting_open
   <- ?voting_id(Id);
      .print("Openning voting #", Id+1) ;
      open;
   .

// This plan is triggerd when a voting result becomes available
+result(T)[artifact_name(ArtName)]
   <- .println("Creating a new goal to set temperature to ",T);
      .drop_desire(temperature(_));
      !temperature(T)
   .
     

+!voting_closed
   <- close.


{ include("temp_management.asl") }

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

{ include("$moiseJar/asl/org-obedient.asl") }