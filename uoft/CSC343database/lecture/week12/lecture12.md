# lecture 12?11?

2015-12-01

## DB design:

overview

- using the **entity/relationship** (er) model to model the real world
- from there, designing a **database schema**
  - restructuring of an e/r model
  - translating an e/r model into a logical model (db schema)
- conceptualizing the real-world / visualization of databases
- Entity/relationship model
  - visual data model (daigram-based)
  - basic concept: *entities* and their *relationship*, along with the *attributes*
- entity sets
  - an entity set represents a category of objects that have properties in common and an autonomous existence
  - an entity is an instance of an entity set
- relationship sets
  - a relationship set is an association between 2+ entity sets
  - a relationship is an instance of a n-ary relationship set
- recursive relationships
  - relate an entity to itself
  - note in the second example that the relationship is not symmetric
- ternary relationships
- attributes
  - describe elementary properties of entities or relationships
  - may be single-valued or multi-valued
- composite attributes
  - are grouped attributes of the same entity or relationship that have closely connected meaning or uses
- cardinalities
  - each entity set participates in a relationship set with a minimum (min) and a maximum (max) cardinality
  - cardinalities constrain how entity instances participate in relationship instances
  - graphical representation in E/R diagrams: pairs of (min, max) values for each entity set
  - *notice: an entity might not participate in any relationship*
  - in principle, cardinalities are pairs of non-negative integers (n, N) such that n <= N, where N means "any number"
  - minimum cardinality n:
    - 0, optional
    - 1, mandatory
  - maximum cardinality N:
    - 1,
    - N,
- multiplicity of relationships
  - if entities E1 and E2 participate in relationship R, with cardinalities (n1, N1) and (n2, N2) then the multiplicity of R is N1-to-N2 (which is the same as saying N2-to-N1)
- cardinalities of attributes
  - describe min/max number of values an attribute can have
  - when the cardinality of attribute is (1,1) it can be omitted (single-valued attributes)
  - the value of an attribute may also be **null**, or have **several** values (multi-valued attributes)
  - multi-valued attributes often represent situations that can be modeled with additional entities
- keys in E/R
  - keys consist of minimal sets of attributes which uniquely identify instances of an entity set
  - in most cases, a key is formed by one or more attributes of the entity itself (internal keys)
  - sometimes, an entity doesn't have a key among its attributes. This is called a weak entity. Solution: the keys of related entities brought in to help with identification (becomeing foreign keys).
  - a key for a relationship ... strong entity
- general observations about keys
- modeling the "real world"
  - design choices: entity, an attribute or a relationship?
  - limitations of ER:...
  - ...

## ER to relational schema
- ER/UML to logical (relational) schema
- 1. restructuring an ER model
  - restructuring overview
    - input ER schema
    - output restructured ER schema
    - restructuring includes
      - analysis of redundancies
      - ...
  - entity sets versus attributes
    - an entity set should satisfy at least one of the following conditions:
      - a. it is more than the name of something: it has at least one **nonkey attribute**
      - b. it is the "**many**" in a many-one or many-many relationship
    - rules of thumb
      - a thing in its own right -> entity set
      - a detail about some other thing -> attribute
      - a detail correltated among many things -> entity set
      - really this is just about avoiding redundancies
- translation into a logical schema
  - input ER schema
  - output relational schema
  - general idea
    - each entity set becomes a relation
      - its attributes are the attributes of the entity set
    - each relationship becomes a relation
      - its attributes are
        - the keys of the entity sets that it connects, plus
        - the attributes of the relationship itself
        -
