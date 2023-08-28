options([15,20,25,30]).



// This plan is triggerd when a voting result becomes available
+result(T)[artifact_name(ArtName)]
   <- .println("Creating a new goal to set temperature to ",T);
      .drop_desire(temperature(_));
      !temperature(T)
   .




{ include("temp_management.asl") }

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

//{ include("$moiseJar/asl/org-obedient.asl") }

{ include("inst-obedient.asl") }