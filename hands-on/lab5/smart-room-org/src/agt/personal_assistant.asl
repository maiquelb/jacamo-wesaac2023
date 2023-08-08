+!ballot[scheme(S)]
  <- .wait(1000) ; // thinking on how to vote...
     // get the name of the voting machine artifact
     // defined for organizational goal "vote"
     ?goalArgument(_, ballot, "voting_machine_id", VMName) ;
     // get the workspace id where the voting machine is
     ?joined(vmws, VWId) ;
     lookupArtifact(VMName, VMId)[wid(VWId)] ;
     // focus on the voting VotingMachine using namespace vm
     vm::focus(VMId)[wid(VWId)] ;

     // consult the temperature options
     ?pref_temp(Pref) ;
     ?options(Options) ;
     ?closest(Pref, Options, Vote) ;

     // vote
     .print("Vote ", Vote) ;
     vm::vote(Vote) .


// closest(Pref,Options,V): discovers the Option closser to Pref
closest(P,[H|_],H) :- P <= H. // assuming options are ordered, if the first option is equals of greater than my pref, it is my vote
closest(P,[H1,H2|_],H1) :- P > H1 & P < H2 & P-H1 <= H2-P. // if my preference is between two options, chose the closer
closest(P,[H1,H2|_],H2) :- P > H1 & P < H2 & P-H1 >  H2-P.
closest(P,[H],H). // no more options
closest(P,[_|T],V) :- closest(P,T,V). // keep looking for options in the list

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

{ include("$moiseJar/asl/org-obedient.asl") }

// commit to missions when permitted
+permission(Ag,Norm,committed(Ag,Mission,Scheme),Deadline)[artifact_id(ArtId),workspace(_,W)]
    : .my_name(Ag)
   <- .print("I am permitted to commit to ", Mission," on ", Scheme,"... doing ");
      commitMission(Mission)[artifact_name(Scheme), wid(W)].