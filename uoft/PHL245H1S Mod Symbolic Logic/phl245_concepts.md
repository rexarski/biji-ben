#PHL245 Concepts
##Unit 1 Reason and argument
**Premises or assumptions**: reasons or justification for the conclusion.

**Conclusion**: the statement, thesis or opinion being argued for.

**Premise indicators**:

**Conclusion indicators**:

**Deductive arguments**: the conclusion can be conclusively deduced from the premises or evidence.

**Validity**: The conclusion must follow from the premises.

**Deductively valid**: an argument is deductively valid if and only if the conclusion is true if all the premises are true. An argument is invalid if and only if it is not valid.

**Soundness**: the premises are true and the argument is valid.

**Sound**: an argument is sound if and only if it is valid and all its premise are true.

##Unit 2 Sentential logic: symbolization
**Sentential logic (SL)**: a branch of logic in which sentences or propositions are used as the basic units. It is also called Propositional Logic or Propositional Calculus.

**Sentence letters**:

**Sentential connectives or logical operators**:

**Parentheses or brackets**:

##Unit 3 Derivations for sentential logic natural deduction
**Derivation**: a derivation is a proof or demonstration that shows how a sentence or sentences can be derived (obtained by making valid inferences) from a set of sentences.

**Direct derivation**:

**Conditional derivation**:

**Indirect derivation**:

**Modus Ponens (mp)**:

**Modus Tollens (mt)**:

**Double Negation (dn)**:

**Repetition (r)**:

**Theorem**: a theorem is a sentence that is true no matter what else is the case. Tautology.

**Simplification (s)**:

**Adjunction (adj)**:

**Modus Tollendo Ponens (mtp)**:

**Addition (add)**:

**Biconditional-Conditional (bc)**:

**Conditional-Biconditional (cb)**:

**Negation of conditional (nc)**:

**Conditional as disjunction (cdj)**:

**Separation of case (sc)**:

**De Morgan's (dm)**:

**Negation of biconditional (nb)**:

##Unit 4 Semantics: fun with truth-tables
**Truth-value assignment (TVA)**: an assignment of truth-values to the atomic sentences.

**tautology**: cannot be false, an analytic or logical truth, true by definition. (true for every TVA, truth-functionally true)

**contradiction**: cannot be true, an analytic or logic falsehood, false by definition. (false for every TVA, truth-functionally false)

**contingent sentence**: can be true or false, logically indeterminate, logically contingent, synthetic. (true on some TVA's and false on some TVA's. truth-functionally indeterminate, truth-functionally contingent)

**logically equivalent**: two sentences are logically equivalent iff there is no truth-value assignment on which two sentences different truth-values. (they are logically equivalent iff two sentences have the same truth-value for every truth-value assignment.)

**consistent**: a set of sentences is consistent iff there is at least one truth-value assignment on which all the members of the set are true.

**inconsistent**: a set of sentences is inconsistent iff there is no truth-value assignment on which all members of the set are true (it is not consistent).

**tautologically implies**: a set of sentences tautologically implies a sentence phi iff there is no truth-value assignment for which all the sentences in the set are true and phi is false.

**valid**: an argument is valid iff there is no truth-value assignment for which all the premises are true and the conclusion is false.

##Unit 5 Symbolization: predicates and quantifiers
**subject**: the object(s), person(s) or place(s) that the sentence is about.

**predicate**: what is being said about (or predicated of) the subject -- often a property or an action.

**universally quantified terms**:

**existentially quantified terms**:

**canonical form of the universal quantified sentence:**

**canonical form of the existential quantified sentence**:

~**SQUARE OF OPPOSITION**:

**universal affirmative**: all A's are B. (A)

**universal negative**: No A's are B. (E)

**particular affirmative**: Some A's are B. (I)

**particular negative**: Some A's are not B. (O)

**contradictions (A & O, I & E)**: the diagonals - if one is true, the other is false.

**contraries (A & E)**: in traditional syllogistic logic, they can both be false but cannot both be true.

**subcontraries (I & O)**: in traditional syllogistic logic, they can both be true but cannot both be false.

**bound variable**: a variable, x, is bound iff it occurs within the scope of an x-qunatifier.

**free variable**: a variable, x, is free iff it is not bound.

**symmetry**: a binary relation is symmetrical iff it is the case that if one thing stands in that relation to another, then the latter stands in that relation to the first.

**asymmetry**: a binary relation is asymmetrical iff it is the case that if one thing stands in that relation to another, the latter cannot stand in that relation to the first.

**transitivity**: a binary relation is transitive iff the case that if one thing stands in the relation to a second, and the second stands in the same relation to a third, then the first stands in that relation to the third.

**intransitivity**: a binary relation is intransitive iff it's the case that if one thing stands in the relation to a second, and the second stands in the same relation to a third, then the first cannot stand in that relation to the third.

**reflexivity**: a binary relation is unrestrictedly reflexive if it is the case that everything stands in that relation to itself.

**irreflexivity**: a binary relation is irreflexive if and only if it's the case that nothing can stand in that relation to itself.

**Leibniz's Law**: aka the principle of the identity of indiscernible. x is identical to y, x = y, iff every property of x is a property of y, and no property that does not belong to x belongs to y.

**canonical form of the unique individual sentence**:

##Unit 6 Derivations for predicate logic
**Universal instantiation (UI)**:

**Existential generalization (EG)**:

**Existential instantiation (EI)**:

**Quantifier negation (QN)**:

**Universal derivation (UD)**:

##Unit 7 Interpretations and models: semantics for predicate logic
**interpretation**: an interpretation assigns meaning to predicates and singular terms.

**extension**: the extension of a predicate is the set of members of the universe that the predicate picks out (that satisfy the predicate).

**an interpretation defines**:
- the universe (must not be empty)
- monadic, dyadic and higher-place predicates
- the individual constants (zero place operation letters)
- truth-values of sentential atomic sentences (zero place predicates)
- monadic, dyadic or higher-place operations


**logical truth**: a sentence P is logically true if and only if P is true on every interpretation.

**logical falsehood**: a sentence P is logically false if and only if P is false on every interpretation.

**contingent sentence**: a sentence P is contingent if and only if P is neither a logical truth nor a logical false hood. (It is true on some interpretations and false on some interpretations.)

**consistent**: a set of sentences is consistent if and only if there is at least one interpretation on which all the members of the set are true.

**logically equivalent**: two sentences are logically equivalent if and only if there is no interpretation on which they have different truth-values. (they are logically equivalent if and only if they have the same truth-vale on every interpretation.)

**validity**: an argument in predicate logic is valid if and only if there is no interpretation on which every premise is true and the conclusion is false. An argument is invalid if and only if the argument is not valid.

**tautological implication**: a set of sentences tautologically implies a sentence phi if and only if there is no interpretation on which all the sentences in the set are true and phi is false.

