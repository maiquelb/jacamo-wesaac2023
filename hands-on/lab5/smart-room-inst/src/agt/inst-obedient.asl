// obligation to achieve a goal by broadcasting a belief
// =====================================================  
+obligation(Ag,R,done(Scheme,Goal,Ag),Deadline) //the agent perceives the obligation following the NPL notation
: .my_name(Ag) 
     & constitutive_rule(X,done(Scheme,Goal,Ag),broadcast(Performative,Bel)[sai__agent(Ag)],M) //The agent looks for a constitutive rule defining how the goal is achieved 
     & X==sai__freestandingY & T\==true & M
     & Bel
   <- .print("I am obliged to ",Goal,". I found a constitutive rule that shows me. I have to ", broadcast(Performative,Bel));
       sai.bridges.jacamo.broadcast_sai(Performative,Bel,[smart_house_inst]).




// obligation to achieve a goal
// ============================  
+obligation(Ag,R,done(Scheme,Goal,Ag),Deadline) //the agent perceives the obligation following the NPL notation
   : .my_name(Ag) 
     & constitutive_rule(X,done(Scheme,Goal,Ag),ToDo[sai__agent(Ag)],M) //The agent looks for a constitutive rule defining how the goal is achieved 
     & X==sai__freestandingY & T\==true & M
   <- .print("I am obliged to ",Goal,". I found a constitutive rule that shows me I have to produce the event ", ToDo);
      ToDo.
      



// obligations to commitment must be handled by the institution and ignored by the agent.
+obligation(Ag,R,committed(Ag,Mission,Scheme),DeadLine)  
   : .my_name(Ag).


// an unknown type of obligation was received
+obligation(Ag,R,What,DeadLine)  
   : .my_name(Ag)
   <- println("I am obliged to ",What,", but I don't know what to do!").