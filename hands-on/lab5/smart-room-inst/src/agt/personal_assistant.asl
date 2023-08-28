
//----------------- Greeting management --------------   

+!greet : language(english)
    <- .print("hello world.").            

+!greet : language(french)
    <- .print("bonjour.").     

+!greet
    <- .print("I do not know how to greet.").    


// closest(Pref,Options,V): discovers the Option closser to Pref
closest(P,[H|_],H) :- P <= H. // assuming options are ordered, if the first option is equals of greater than my pref, it is my vote
closest(P,[H1,H2|_],H1) :- P > H1 & P < H2 & P-H1 <= H2-P. // if my preference is between two options, chose the closer
closest(P,[H1,H2|_],H2) :- P > H1 & P < H2 & P-H1 >  H2-P.
closest(P,[H],H). // no more options
closest(P,[_|T],V) :- closest(P,T,V). // keep looking for options in the list


+obligation(Ag,R,done(Scheme,Goal,Ag),Deadline) //the agent perceives the obligation following the NPL notation
   : .my_name(Ag) 
     & constitutive_rule(X,done(Scheme,Goal,Ag),vote(Preference)[sai__agent(Ag)],M) //The agent looks for a constitutive rule defining how the goal is achieved 
     & X==sai__freestandingY & T\==true & M & preference(Preference)
   <- .print("I am obliged to ",Goal,". I found a constitutive rule that shows me I have to produce the event vote(", Preference,")");
      vote(Preference).      

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

{ include("inst-obedient.asl") }



