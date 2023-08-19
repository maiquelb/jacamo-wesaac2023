
// Checks that the current temperature is close to the target 
// temperature (+/- some tolerance level)
temperature_in_range(T)
	:- not now_is_colder_than(T) & not now_is_warmer_than(T).

// Checks that the current temperature is not lower than the 
// target temperature above a tolerance level
now_is_colder_than(T)
	:- temperature(C) & tolerance(DT) & (T - C) > DT.

// Checks that the current temperature is not higher than the 
// target temperature above a tolerance level
now_is_warmer_than(T)
	:- temperature(C) & tolerance(DT) & (C - T) > DT.

+!keep_temperature 
   //: preference(P) & temperature(C) & P\==C &
   : preference(P) &
     not temperature_in_range(P) &
     voting_status("closed") &
     not scheme(temp_r1,decide_temp,_) &
     group(r1, room, GrpArtId)[artifact_id(OrgArtId)] &
     formationStatus(ok)[artifact_id(GrpArtId)] 
   <- .print("Current temperature is different of my preferred one, which is ", P);
      //.send(rc,achieve,open_voting);
      //.wait(voting_status("open"));      
      createScheme(temp_r1,decide_temp,SchArtId)[artifact_id(OrgArtId)];
      addScheme(temp_r1)[artifact_id(GrpArtId)];
      !keep_temperature;
       .

+!keep_temperature
   <- .wait(1000);
      !keep_temperature.


-keep_temperature
   <- .wait(1000);
      !keep_temperature.

+goalState(temp_r1,voting,[],[],satisfied)[artifact_id(SchArtId)] : schemes([temp_r1])[artifact_id(GrpArtId)]
   <- .print("Going to destroy scheme...");
      .wait(5000);
      
      //destroy[artifact_id(SchArtId)].
      removeScheme(temp_r1)[artifact_id(GrpArtId)].
//----------------- Greeting management --------------   

+!greet : language(english)
    <- .print("hello world.").            

+!greet : language(french)
    <- .print("bonjour.").     

+!greet
    <- .print("I do not know how to greet.").    



+!ballot_done
  <- 
     ?preference(Pref) ; // consult the agent's preference
     ?options(Options) ; // consult the temperature options
     ?closest(Pref, Options, Vote) ;

     // vote
     .print("Vote ", Vote) ;
     vote(Vote) .
     


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
/*+permission(Ag,Norm,committed(Ag,Mission,Scheme),Deadline)[artifact_id(ArtId),workspace(_,W)]
    : .my_name(Ag)
   <- .print("I am permitted to commit to ", Mission," on ", Scheme,"... doing ");
      commitMission(Mission)[artifact_name(Scheme), wid(W)].
*/
      