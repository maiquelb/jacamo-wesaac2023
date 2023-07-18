
+!greet :language(english)
    <- .print("hello world.").            

+!greet :language(french)
    <- .print("bonjour.").                



//-------------------------------------------------------------    

{ include("$jacamo/templates/common-cartago.asl") }
{ include("$jacamo/templates/common-moise.asl") }

// uncomment the include below to have an agent compliant with its organisation
//{ include("$moise/asl/org-obedient.asl") }
