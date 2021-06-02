## General Info  

Name: Traveller

Implementation language: Python 3.6.8

*Specification by Nathaniel Gordon and Tal Puhov*

## Purpose

The high-level purpose of the desired project is to provide the services of a route planner through a network of towns for a role-playing game.

The project should consist of a single module named "/traveller.py" which is able to support the following operations:
- the creation of a town network (represented as a *simple graph*) with named nodes
- the placement of a named character in a town
- a query whether a specified character can reach a designated town without running into any other characters

As necessitated by these items, the module will store information regarding the state of the game, including:

- the town network, including names and topological relationship
- the names and positions of multiple characters

## Classes and Functions

For compatibility with our current code, we require a class **TownNetwork**" containing:
  - field **towns**" which is a Collection of (*name, connectivity*) tuples
      - *name* is a String
      - *connectivity* is a collection of connected town names
  - field **characters** which is a collection of (*name, location*) tuples
      - *name* is a String
      - *location* is a String matching a town name
  - function **create_town**(*town_name, neighbors*) -> None
    - *town_name* is a String
    - *neighbors* is tuple of String
  - function **place_character**(*char_name, town_name*) -> bool
    - *char_name* is a String
    - *town_name* is a String
    - returns True if successful, otherwise returns False.
  - function **path_is_unblocked**(*char_name, dest*) -> bool
    - *char_name* is a String
    - *dest* is a String
    - returns True if there is a path from the town where character *name* currently resides to the town *dest*, otherwise returns False.

Any other functionality is up to the implementation and has no specific naming guidelines.