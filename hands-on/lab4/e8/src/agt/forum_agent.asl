+!submit_post
   <- ?message(Msg) ;
      submitPost(Msg) ;
      .print("Sent message : ", Msg) .

+!retrieve_post
   <- retrievePost(-1) ;
      ?topic(Topic) ;
      ?post(Msg) ;
      .print("Received message : ", Msg) .

{ include("$jacamoJar/templates/common-cartago.asl") }