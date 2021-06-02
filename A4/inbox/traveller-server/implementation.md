# MEMORANDUM

### DATE: 2/2/2021
### TO: Drake Moore & Michael Curley
### FROM: John Hassan & Marty Vo
### SUBJECT: traveller-server Implementation

We made some slight changes to the design. Here they are:

Instead of defining existingPlayers as a static variable within its class,
we defined it outside of the class as a global variable. Considering this variable will not be able to be updated inside of the class with each player added, we moved it outside in order to make the functionality of your specifications achievable.

This process was also done with existingTowns, as the same logic applies.