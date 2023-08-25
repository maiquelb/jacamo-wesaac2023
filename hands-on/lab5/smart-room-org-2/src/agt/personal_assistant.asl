
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


/*
   The agent wants to keep the temperature as close as possible to its preference.
   If the temperature os not close of the agent's preference, it launches a new schema to manage the voting process.
*/
+!keep_temperature 
   : preference(P) &
     not temperature_in_range(P) &
     not scheme(temp_r1,decide_temp,_) &
     group(r1, room, GrpArtId)[artifact_id(OrgArtId)] &
     formationStatus(ok)[artifact_id(GrpArtId)] 
   <- .print("Current temperature is different of my preferred one, which is ", P ,". Launching a new schema.");      
      .wait(1000); //wait a second just to better observe the output
      //TODO (exercise 5.3.2): create a new schema to manage a voting

      //TODO (exercise 5.3.3): make the existing group to manage the voting
      
      !keep_temperature;
       .

+!keep_temperature
   <- .wait(1000);
      !keep_temperature.


-!keep_temperature
   <- .wait(1000);
      !keep_temperature.


/* If the goal of for a new temperature has been achieved, the scheme is destroyed. */
+goalState(SchId,voting,[],[],satisfied)[artifact_id(SchArtId)] 
   : scheme(SchId,_,_)[artifact_id(OrgBoardArtId)]
   <- .random(R); .wait(R*100); //wait a random while as another agent may be currently finishing the schema
      !finish_schema(SchId, OrgBoardArtId).

+!finish_schema(SchId, OrgBoardArtId) : scheme(SchId,_,_)[artifact_id(OrgBoardArtId)]  
    <-  destroyScheme(SchId)[artifact_id(OrgBoardArtId)].

+!finish_schema(SchId, OrgBoardArtId).

-!finish_schema(SchId, OrgBoardArtId)
   <- .print("Failed to destroy the schema ", SchId, ". It has been possibly destroyed by another agent").


//----------------- Greeting management --------------   

+!greet : language(english)
    <- .print("hello world.").            

+!greet : language(french)
    <- .print("bonjour.").     

+!greet
    <- .print("I do not know how to greet.").    



+!vote_done
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
