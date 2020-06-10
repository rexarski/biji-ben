# lecture 9

2015-11-17 18:15:44

## xquery continued

- generous comparison
  - two sequences, use `A=B`, does not mean totally equivalent but at least equivalent
    - say, `(1,2) = (2,3)` is true
- strict comparison
  - alternative: the comparison operators
    - eq, ne, lt, le, gt, ge
    - succeed only if both sequences have length one
- eliminating duplicates
  - apply function `distinct-values` to a sequence
    - it strips tags away and compare elements
    - but it does not restore tags back
- branching expressions
  - `if (<<E1>>) then <<E2>> else <<E3>>`
- any type can be treated as a boolean
  - the **effective boolean value (EBV)** of an expression is:
    - the value of the expression, if it is already of type boolean
    - ow it is FALSE if the expression evaluates to 0, "" or ()
    - TRUE if not
- quantifier expression
  - `some <<variable>> in <<E1>> satisfies <<E2>>`
  - `every <<variable>> in <<E1>> satisfies <<E2>>`
- coparison based on document order
  - `<<E1>> < <<E2>> and <<E1>> > <<E2>>`
- set operators
  - `<<E1>> union <<E2>>`
  - `<<E1>> intersect <<E2>>`
  - `<<E1>> except <<E2>>`
  - returned result does not include duplicates

## design theory for relational databases

### functional dependency
- `X -> Y` X functionally determines Y
  - if two tuples agree on all the attributes in set X, they must also agree on all the attributes in set Y
### attributes
### projecting
### minimal basis
