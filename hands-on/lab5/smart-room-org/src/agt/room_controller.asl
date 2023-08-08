+!voting(Options)
   <- +options(Options) .

+!announce_options[scheme(S)]
   <- ?options(Options) ;
      .broadcast(tell, options(Options)) .

+!open_voting[scheme(S)]
   <- // get voters from organization (agents playing assistant)
      .wait(100) ;
      .findall(A, play(A, assistant, _), Voters);

      // get the voting options 
      ?options(Options) ;

      // open "voting machine" for votes
      vm::open(Options, Voters, 10000);

      .print("Options are ", Options, " voters are ", Voters);

      // set the argument of organizational goal "vote"
      setArgumentValue(ballot, voting_machine_id, v1)[artifact_name(S)] .

+!close_voting[scheme(S)]
   <- .print("Time is out, the vote should now be closed.") ;
      vm::close .

+vm::result(T)[artifact_name(ArtName)]
   <- .println("Creating a new goal to set temperature to ", T) ;
      .drop_desire(temperature(_)) ;
      !temperature(T) .


tolerance(2) . // used in temp_management
{ include("temp_management.asl") }

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

{ include("$moiseJar/asl/org-obedient.asl") }