!greet.

+!greet : language(english)
    <- .print("hello world.").            

+!greet : language(french)
    <- .print("bonjour.").                

+!inform_date
   <- .date(Y,M,D); //check the current date
      .print("Current date ", Y, "-", M, "-", D).

+day_of_week(D)
   <- .print("Today is ", D).


//-------------------------------------------------------------    

{ include("$jacamo/templates/common-cartago.asl") }
{ include("$jacamo/templates/common-moise.asl") }

// uncomment the include below to have an agent compliant with its organisation
//{ include("$moise/asl/org-obedient.asl") }
