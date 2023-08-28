teacher(karlos).

-!G[error(no_relevant)] 
   :  teacher(T) 
   <- .send(T, askHow, { +!G }, Plans);
      .add_plan(Plans);
      !G.
