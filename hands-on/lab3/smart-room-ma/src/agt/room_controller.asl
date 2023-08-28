+!voting(Options) 
   <- !open_voting(Id,Options);
      !wait_votes(Id);
      !close_voting(Id).

+!open_voting(Id,Options)
   <- Id = 1;
      .broadcast(tell, open_voting(Id,Options,4000)).

+!wait_votes(Id) <- .wait(all_votes_received(Id), 4000, _).

all_votes_received(Id)
  :- .count(vote(Id,_)[source(_)], 3).  // equals number of votes


+!close_voting(Id)
   <- ?most_voted(Id,T);
      .println("New goal to set temperature to ",T);
      .broadcast(tell, close_voting(Id,T));
      !temperature(T);
   .
most_voted(Id,T)
   :- .findall(
          t(C,V), 
          vote(Id,V) & .count(vote(Id,V)[source(_)],C), 
          LV)
      & .print("votes: ",LV)
      & .max(LV,t(_,T)).


tolerance(2). // used in temp_management
{ include("temp_management.asl") }

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
