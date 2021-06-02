# Milestone 6 - Refactoring Report

**Team members:**
Michael Curley
Drake Moore

**Github team/repo:**
Lonande


## Plan

- implement a room builder similar to game builder for easier instantiation
- update all unit tests for more code coverage

~~- create a python "interface" for all objects with an "asciiRender" function~~
- when returning a game state to players, make sure to censor other actor
  locations
- create a python "interface" for the rule checker and have it passed in to
  game manager rather than be static
- abstract json parsing for the tests directory
- try to figure out a fix for the circular dependencies
- update testLevel to pass test cases
- update testRoom to use new constructors


## Changes

- added a RoomBuilder object and tests
- removed asciiRender interface from **Plan**, an Enum cannot inherit from more
  than one type so this interface would be unused for its intent
- rule checker updated to no longer be static, games with different rules may
  simply overwrite one or all methods
- updated testLevel to pass given test cases
- updated testRoom to use new constructors, updated room test cases to not
  include walls as traversable (since our original assumption was wrong)
- changed the game manager's udpate game state for player to censor unneeded information
- added a snarlParser.py and an autoTest.py to aid in future testing


## Future Work

If circular dependencies become an issue we will fix it then, until now it is just a
stylistic inconvenience.

## Conclusion

We were already satisfied with the status of our code base; it is concise, documented
and has built in (passing) unit tests.  We took this week as a chance to clean up a
few minor outstanding issues that were not addressed in any assignments.  Overall,
the tests harnesses are now automated, json parsing is abstracted and player
information is no longer exposed.  We didn’t do any significant changes to the logic
or structure of the design and kept our changes confined to small areas.
