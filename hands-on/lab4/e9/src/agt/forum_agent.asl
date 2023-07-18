+!submit_post[scheme(S)]
   <- ?message(Msg) ;
      submitPost(Msg) ;
      .print("Sent message : ", Msg) .

+!retrieve_post[scheme(S)]
   <- retrievePost(-1) ;
      ?topic(Topic) ;
      ?post(Msg) ;
      .print("Received message : ", Msg) .

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

{ include("$moiseJar/asl/org-obedient.asl") }

// commit to missions when permitted
+permission(Ag,Norm,committed(Ag,Mission,Scheme),Deadline)[artifact_id(ArtId),workspace(_,W)]
    : .my_name(Ag)
   <- .print("I am permitted to commit to ",Mission," on ",Scheme,"... doing ");
      commitMission(Mission)[artifact_name(Scheme), wid(W)].