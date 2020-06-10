# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" !!!!!!!!!!!!!!!!!!!!! STOP !!!!!!!!!!!!!!!!!!!!!!!!!!!!

    This file is big and messy and deals with the translation from PDDL (with ADL)
    to some nice internal data structures.

    To look here is to take the first step down the path to madness.

    Look at strips_problem.py instead.
"""

import itertools

import strips_problem
from utilities import (AND_CONDITION, CONDITIONAL_EFFECT, EQUALS_CONDITION,
                       EXISTS_CONDITION, FORALL_CONDITION, IMPLY_CONDITION,
                       INCREASE_CONDITION, NOT_CONDITION, OR_CONDITION,
                       POST_COND, PRE_COND, ProblemException, cond_prefix,
                       default_type_name, grounding_error_code,
                       inequality_prefix, lower_var_alphabet)


class Object:
    """ A PDDL object """

    def __init__(self, name, otype, constant):
        """ Make a new Object
            (Object, str, Type, bool) -> None
        """
        self.name = name
        self.otype = otype
        self.constant = constant

    def __dump__(self):
        """ Return a full string representation of the object
            (Object) -> None
        """
        return self.name + " - " + str(self.otype)

    def __str__(self):
        """ Return a short string representation of the object
            (Object) -> str
        """
        return self.name

class Type:
    """ A PDDL type """

    def __init__(self, name, parent):
        """ Make a new Type
            (Type, str, Type) -> None
        """
        self.name = name
        self.parent = parent
        self.objects = []

    def __dump__(self):
        """ Return a full string representation of the type
            (Type) -> None
        """
        if self.parent:
            return self.name + " - " + self.parent.name
        else:
            return self.name

    def __str__(self):
        """ Return a short string representation of the type
            (Type) -> str
        """
        return self.name

    def add_object(self, obj):
        """ Add the object to the type and to all of its ancestors.
            (Type, str) -> None
        """
        if obj not in self.objects:
            self.objects.append(obj)
            if self.parent:
                self.parent.add_object(obj)


class Function:
    """ A PDDL numeric function """

    def __init__(self, name, variables, types):
        """ Make a new Function
            (Function, str, [str], [Type]) -> None
        """
        self.name = name
        self.variables = variables
        self.types = types
        self.values = {}

    def __dump__(self):
        """ Return a full string representation of the function
            (Function) -> None
        """
        return "( " + self.name + " " + " ".join([x + " - " + str(y)\
            for x, y in zip(self.variables, self.types)]) + " ) - numeric"

    def __str__(self):
        """ Return a short string representation of the function
            (Function) -> str
        """
        return "( " + self.name + " " + " ".join(self.variables) + " )"


class Predicate:
    """ A domain predicate """

    def __init__(self, name, variables, types):
        """ Make a new Predicate
            (Predicate, str, [str], [Type]) -> None
        """
        self.name = name
        self.variables = variables
        self.types = types
        self.groundings = []
        self.neg_groundings = []


    def __dump__(self):
        """ Return a full string representation of the predicate
            (Predicate) -> None
        """
        return self.__str__()

    def __str__(self):
        """ Return a short string representation of the predicate
            (Predicate) -> str
        """
        return "( " + self.name + " " + " ".join([x + " - " + str(y)\
            for x, y in zip(self.variables, self.types)]) + " )"

    def __lt__(self, other) :
        return str(self) < str(other)

class Condition:
    """ A formula used as a precondition or head of an axiom or conditional effect. """

    def __init__(self):
        """ Make a new condition.
            (Condition) -> None
        """
        self.groundings = []
        self.desc = None

    def substitute_derived_predicates(self, derived_predicates, seen_preds):
        """ Replace the derived predicates in the condition with the
            conditions of the derived predicates.
            (Condition, { Predicate : [DerivedPredicate] }, [Predicate]) -> Condition
        """
        return self

    def has_quant(self):
        """ Return true iff this condition or one of its descendants is a quantifier
           (Condition) -> bool
        """
        return False

    def flatten(self):
        """ Flatten conjunctions and disjunctions.
            (Condition) -> None
        """
        return self

    def collect_neg_precs(self, neg_precs, param_types, collect = True):
        """ Recurse through the condition tree looking for negative preconditions
            (Condition, { str : Predicate }, { str : Type }, bool) -> None
        """
        pass

    def detect_statics(self, candidates, neg_candidates):
        """ Remove entries from candidates which are deleted somewhere in this
            condition. Default to doing nothing.
            (Condition, set([(Predicate, [str]), set([(Predicate, [str])]) -> None
        """
        pass

    def get_encode_conds(self, encode_conds, do_encode):
        """ Populate encode_conds with conditions that actually need to be
            properly encoded for invariants preprocessing and in SAT.
            (Condition, set([Condition]), bool) -> None
        """
        pass


class PredicateCondition(Condition):
    """ A formula consisting of just a Predicate """

    def __init__(self, pred, variables):
        """ Make a new PredicateCondition.
            (PredicateCondition, Predicate, [str]) -> None
        """
        super(PredicateCondition, self).__init__()
        self.pred = pred
        self.variables = variables
        self.sign = True
        self.ground_conditions = {}

    def __dump__(self):
        """ Return a full string representation of the condition
            (PrecdicateCondition) -> None
        """
        return self.__str__()

    def __str__(self):
        """ Return a short string representation of the condition
            (PredicateCondition) -> str
        """
        if self.sign:
            return "(" + self.pred.name + " " + " ".join(self.variables) + ")"
        else:
            return "(not (" + self.pred.name + " " + " ".join(self.variables) + "))"

    def substitute_vars(self, substitutions):
        """ Replace the variables in this condition as specified in substitutions.
            Return a copy of the condition.
            (PredicateCondition, { str : str }) -> PredicateCondition
        """
        return PredicateCondition(self.pred, [substitutions[v] for v in self.variables])

    def substitute_derived_predicates(self, derived_predicates, seen_preds):
        """ Replace the derived predicates in the condition with the conditions
            of the derived predicates.
            (PredicateCondition, { Predicate : [DerivedPredicate] }, [Predicate]) -> Condition
        """
        if self.pred in derived_predicates:
            if self.pred in seen_preds:
                raise ProblemException("Error cycle in derived predicate definitions: " +\
                    self.pred.name, grounding_error_code)
            sp_copy = list(seen_preds)
            sp_copy.append(self.pred)
            dp_copies = []
            for dp in derived_predicates[self.pred]:
                dp.precondition = dp.precondition.substitute_derived_predicates(derived_predicates, sp_copy)
                dp_copies.append(dp.precondition.substitute_vars(dict(list(zip(dp.param_names, self.variables)))))
            if len(dp_copies) > 1:
                return OrCondition(dp_copies)
            return dp_copies[0]
        return self

    def nnf(self, negation = False):
        """ Convert the condition to negation normal form.
            (PredicateCondition, bool) -> Condition
        """
        if negation:
            self.sign = False
        return self

    def collect_neg_precs(self, neg_precs, param_types, collect = True):
        """ Recurse through the condition tree looking for negative preconditions
            (Condition, { str : Predicate }, { str : Type } ) -> None
        """
        if not self.sign and collect:
            if self.pred.name not in neg_precs:
                neg_precs[self.pred.name] = self.pred

    def compute_relevant_vars(self, var_types):
        """ Compute, store, and return the relevant variables to this condition.
            (PredicateCondition, { str : Type }) -> [str]
        """
        self.relevant_vars = []
        self.var_types = {}
        self.var_indices = {}   #Each element here is a list as there might be dups
        for vid, var in enumerate(self.variables):
            if var[0] == "?":
                assert var in var_types
                self.relevant_vars.append(var)
                self.var_types[var] = var_types[var]
                if var not in self.var_indices:
                    self.var_indices[var] = []
                self.var_indices[var].append(vid)
        return self.relevant_vars

    def assign_cond_code(self, cond_index, code_conds):
        """ Make a condition code for this condition.
            (PredicateCondition, [int], { str : Condition }) -> None
        """
        self.cond_code = cond_prefix + str(cond_index[0])
        code_conds[self.cond_code] = self
        cond_index[0] += 1

    def detect_statics(self, candidates, neg_candidates):
        """ Remove entries from candidates which are deleted somewhere in this effect.
            (PredicateCondition, set([(Predicate, [str])], set([(Predicate, [str])) -> None
        """
        if self.sign:
            for grounding in self.groundings:
                neg_candidates.discard((self.pred, grounding))
        else:
            for grounding in self.groundings:
                candidates.discard((self.pred, grounding))

    def link_groundings(self, static_preds, neg_static_preds):
        """ Link the groundings in this condition to the groundings in its
            predicate. Also conditions from this action which have no groundings,
            which refer only to static predicates, equalities, etc.

            (PredicateCondition, set([(Predicate, (str, ...))]),
                set([(Predicate, (str, ...))])) -> Condition
        """
        new_groundings = []
        for grounding in self.groundings:
            t_grounding = list(self.variables)
            for vid, var in enumerate(self.relevant_vars):
                for vi in self.var_indices[var]:
                    t_grounding[vi] = grounding[vid]
            t_grounding = tuple(t_grounding)
            pg_pair = (self.pred, t_grounding)
            if (not self.sign and pg_pair not in neg_static_preds) or\
               (self.sign and pg_pair not in static_preds):
                new_groundings.append(grounding)
                self.ground_conditions[grounding] = tuple(t_grounding)
        self.groundings = new_groundings
        if not self.groundings:
            return None
        return self

    def make_flat_effects(self, ground_effects, grounding):
        """ Make the flat list of ground effects
            (PredicateCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        ground_effects.append((self, grounding, self.sign))

    def make_flat_preconditions(self, ground_precs, grounding):
        """ Make the flat list of ground preconditions
            (PredicateCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        ground_precs.append((self, grounding, self.sign))


class NotCondition(Condition):
    """ A formula consisting of just negation - Instances of this class are
        removed in the conversion to NNF.
    """

    def __init__(self, condition):
        """ Make a new NotCondition.
            (NotCondition, Condition) -> None
        """
        super(NotCondition, self).__init__()
        self.condition = condition
        self.desc = NOT_CONDITION

    def __dump__(self):
        """ Return a full string representation of the condition
            (NotCondition) -> str
        """
        return "(not " + self.condition.__dump__() + ")"

    def __str__(self):
        """ Return a short string representation of the condition
            (NotCondition) -> str
        """
        return "(not ...)"

    def substitute_vars(self, substitutions):
        """ Replace the variables in this condition as specified in substitutions.
            Return a copy of the condition.
            (NotCondition, { str : str }) -> NotCondition
        """
        return NotCondition(self.condition.substitute_vars(substitutions))

    def substitute_derived_predicates(self, derived_predicates, seen_preds):
        """ Replace the derived predicates in the condition with the
            conditions of the derived predicates.
            (NotCondition, { Predicate : [DerivedPredicate] }, [Predicate]) -> NotCondition
        """
        self.condition = self.condition.substitute_derived_predicates(derived_predicates,
            seen_preds)
        return self

    def nnf(self, negation = False):
        """ Convert the condition to negation normal form.
            (NotCondition, bool) -> Condition
        """
        return self.condition.nnf(not negation)


class AndCondition(Condition):
    """ A formula consisting of a conjunction """

    def __init__(self, conditions):
        """ Make a new AndCondition.
            (AndCondition, [Condition]) -> None
        """
        super(AndCondition, self).__init__()
        self.conditions = conditions
        self.ground_conditions = []
        self.desc = AND_CONDITION

    def __dump__(self):
        """ Return a full string representation of the condition
            (AndCondition) -> str
        """
        return "(and " + " ".join([x.__dump__() for x in self.conditions]) + ")"

    def __str__(self):
        """ Return a short string representation of the condition
            (AndCondition) -> str
        """
        return "(and ...)"

    def substitute_vars(self, substitutions):
        """ Replace the variables in this condition as specified in substitutions.
            Return a copy of the condition.
            (AndCondition, { str : str }) -> AndCondition
        """
        return AndCondition([cond.substitute_vars(substitutions) for cond in self.conditions])

    def substitute_derived_predicates(self, derived_predicates, seen_preds):
        """ Replace the derived predicates in the condition with the
            conditions of the derived predicates.
            (AndCondition, { Predicate : [DerivedPredicate] }, [Predicate]) -> AndCondition
        """
        for cid, cond in enumerate(self.conditions):
            self.conditions[cid] = cond.substitute_derived_predicates(derived_predicates, seen_preds)
        return self

    def nnf(self, negation = False):
        """ Convert the condition to negation normal form.
            (AndCondition, bool) -> Condition
        """
        for cid, cond in enumerate(self.conditions):
            self.conditions[cid] = cond.nnf(negation)
        if negation:
            return OrCondition(self.conditions)
        return self

    def flatten(self):
        """ Flatten conjunctions and disjunctions.
            (AndCondition) -> None
        """
        child_conjs = [cond for cond in self.conditions\
            if isinstance(cond, AndCondition)]
        for cond in child_conjs:
            self.conditions.remove(cond)
            self.conditions.extend(cond.conditions)
        for cond in self.conditions:
            cond.flatten()

    def has_quant(self):
        """ Return true iff this condition or one of its descendants is a quantifier
           (AndCondition) -> bool
        """
        for cond in self.conditions:
            if cond.has_quant():
                return True
        return False

    def collect_neg_precs(self, neg_precs, param_types, collect = True):
        """ Recurse through the condition tree looking for negative preconditions
            (AndCondition, { str : Predicate }, { str : Type }, bool) -> None
        """
        for cond in self.conditions:
            cond.collect_neg_precs(neg_precs, param_types, collect)

    def compute_relevant_vars(self, var_types):
        """ Compute, store, and return the relevant variables to this condition.
            (AndCondition, { str : Type }) -> [str]
        """
        self.relevant_vars = []
        for condition in self.conditions:
            for rv in condition.compute_relevant_vars(var_types):
                if rv not in self.relevant_vars:
                    self.relevant_vars.append(rv)
        self.var_types = {}
        for rv in self.relevant_vars:
            assert rv in var_types
            self.var_types[rv] = var_types[rv]
        self.var_indices = dict([(v, [i]) for i, v in enumerate(self.relevant_vars)])
        return self.relevant_vars

    def assign_cond_code(self, cond_index, code_conds):
        """ Assign a code to this condition.
            (AndCondition, [int], { str : Condition }) -> None
        """
        self.cond_code = cond_prefix + str(cond_index[0])
        code_conds[self.cond_code] = self
        cond_index[0] += 1
        for condition in self.conditions:
            condition.assign_cond_code(cond_index, code_conds)

    def detect_statics(self, candidates, neg_candidates):
        """ Remove entries from candidates which are deleted somewhere in this cond.
            (AndCondition, set([(Predicate, [str])], set([(Predicate, [str])) -> None
        """
        for condition in self.conditions:
            condition.detect_statics(candidates, neg_candidates)

    def link_groundings(self, static_preds, neg_static_preds):
        """ Link the groundings in this condition to the groundings in its
            sub_conditions and prune statics, and conditions without groundings.
            (AndCondition, set([(Predicate, (str, ...))]),
                set([(Predicate, (str, ...))])) -> Condition
        """
        new_conditions = []
        for condition in self.conditions:
            condition = condition.link_groundings(static_preds, neg_static_preds)
            if isinstance(condition, AndCondition):
                for cond in condition.conditions:
                    self.conditions.append(cond)
            elif condition is not None:
                sub_indices = [self.var_indices[v][0] for v in condition.relevant_vars]
                ground_conditions = {}
                for grounding in self.groundings:
                    sub_grounding = tuple([grounding[i] for i in sub_indices])
                    if sub_grounding in condition.groundings:
                        ground_conditions[grounding] = sub_grounding
                if ground_conditions:
                    self.ground_conditions.append(ground_conditions)
                    new_conditions.append(condition)
        self.conditions = new_conditions

        new_groundings = []
        for grounding in self.groundings:
            for ground_conditions in self.ground_conditions:
                if grounding in ground_conditions:
                    new_groundings.append(grounding)
                    break
        self.groundings = new_groundings
        if not self.groundings:
            return None
        if len(self.conditions) == 1:
            return self.conditions[0]
        return self

    def make_flat_effects(self, ground_effects, grounding):
        """ Make the flat list of ground effects
            (AndCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        for cid, condition in enumerate(self.conditions):
            condition.make_flat_effects(ground_effects, self.ground_conditions[cid][grounding])

    def make_flat_preconditions(self, ground_precs, grounding):
        """ Make the flat list of ground preconditions
            (AndCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        for cid, condition in enumerate(self.conditions):
            if grounding in self.ground_conditions[cid]:
                 condition.make_flat_preconditions(ground_precs, self.ground_conditions[cid][grounding])

    def get_encode_conds(self, encode_conds, do_encode):
        """ Populate encode_conds with conditions that actually need to be
            properly encoded for invariants preprocessing and in SAT.
            (AndCondition, set([Condition])) -> None
        """
        if do_encode:
            encode_conds.add(self)
        for condition in self.conditions:
            condition.get_encode_conds(encode_conds, do_encode)


class OrCondition(Condition):
    """ A formula consisting of a disjunction """

    def __init__(self, conditions):
        """ Make a new OrCondition.
            (OrCondition, [Condition]) -> None
        """
        super(OrCondition, self).__init__()
        self.conditions = conditions
        self.ground_conditions = []
        self.desc = OR_CONDITION

    def __dump__(self):
        """ Return a full string representation of the condition
            (OrCondition) -> str
        """
        return "(or " + " ".join([x.__dump__() for x in self.conditions]) + ")"

    def __str__(self):
        """ Return a short string representation of the condition
            (OrCondition) -> str
        """
        return "(or ...)"

    def substitute_vars(self, substitutions):
        """ Replace the variables in this condition as specified in substitutions.
            Return a copy of the condition.
            (OrCondition, { str : str }) -> OrCondition
        """
        return OrCondition([cond.substitute_vars(substitutions) for cond in self.conditions])

    def substitute_derived_predicates(self, derived_predicates, seen_preds):
        """ Replace the derived predicates in the condition with the
            conditions of the derived predicates.
            (OrCondition, { Predicate : [DerivedPredicate] }, [Predicate]) -> OrCondition
        """
        for cid, cond in enumerate(self.conditions):
            self.conditions[cid] = cond.substitute_derived_predicates(derived_predicates,
                seen_preds)
        return self

    def nnf(self, negation = False):
        """ Convert the condition to negation normal form.
            (OrCondition, bool) -> Condition
        """
        for cid, cond in enumerate(self.conditions):
            self.conditions[cid] = cond.nnf(negation)
        if negation:
            return AndCondition(self.conditions)
        return self

    def flatten(self):
        """ Flatten conjunctions and disjunctions.
            (OrCondition) -> None
        """
        child_conjs = [cond for cond in self.conditions if isinstance(cond, OrCondition)]
        for cond in child_conjs:
            self.conditions.remove(cond)
            self.conditions.extend(cond.conditions)
        for cond in self.conditions:
            cond.flatten()

    def has_quant(self):
        """ Return true iff this condition or one of its descendants is a quantifier
           (OrCondition) -> bool
        """
        for cond in self.conditions:
            if cond.has_quant():
                return True
        return False

    def collect_neg_precs(self, neg_precs, param_types, collect = True):
        """ Recurse through the condition tree looking for negative preconditions
            (OrCondition, { str : Predicate }, { str : Type }, bool) -> None
        """
        for cond in self.conditions:
            cond.collect_neg_precs(neg_precs, param_types, collect)

    def compute_relevant_vars(self, var_types):
        """ Compute, store, and return the relevant variables to this condition
            along with their types.

            (OrCondition, { str : Type }) -> [str]
        """
        self.relevant_vars = []
        for condition in self.conditions:
            for rv in condition.compute_relevant_vars(var_types):
                if rv not in self.relevant_vars:
                    self.relevant_vars.append(rv)
        self.var_types = {}
        for rv in self.relevant_vars:
            assert rv in var_types
            self.var_types[rv] = var_types[rv]
        self.var_indices = dict([(v, [i]) for i, v in enumerate(self.relevant_vars)])
        return self.relevant_vars

    def assign_cond_code(self, cond_index, code_conds):
        """ Assign a code to this condition.
            (OrCondition, [int], { str : Condition }) -> None
        """
        self.cond_code = cond_prefix + str(cond_index[0])
        code_conds[self.cond_code] = self
        cond_index[0] += 1
        for condition in self.conditions:
            condition.assign_cond_code(cond_index, code_conds)

    def detect_statics(self, candidates, neg_candidates):
        """ Remove entries from candidates which are deleted somewhere in this cond.
            (OrCondition, set([(Predicate, [str])], set([(Predicate, [str])) -> None
        """
        for condition in self.conditions:
            condition.detect_statics(candidates, neg_candidates)

    def link_groundings(self, static_preds, neg_static_preds):
        """ Link the groundings in this condition to the groundings in its
            sub_conditions and prune statics, and conditions without groundings.
            (OrCondition, set([(Predicate, (str, ...))],
                set([(Predicate, (str, ...))])) -> Condition
        """
        new_conditions = []
        for condition in self.conditions:
            condition = condition.link_groundings(static_preds, neg_static_preds)
            if isinstance(condition, OrCondition):
                for cond in condition.conditions:
                    self.conditions.append(cond)
            elif condition is not None:
                ground_conditions = {}
                sub_indices = [self.var_indices[v] for v in condition.relevant_vars]
                for grounding in self.groundings:
                    sub_grounding = tuple([grounding[i] for i in sub_indices])
                    if sub_grounding in condition.groundings:
                        ground_conditions[grounding] = sub_grounding
                if ground_conditions:
                    self.ground_conditions.append(ground_condtions)
                    new_conditions.append(condition)
        self.conditions = new_conditions

        new_groundings = []
        for grounding in self.groundings:
            for ground_conditions in self.ground_conditions:
                if grounding in ground_conditions:
                    new_groundings.append(grounding)
                    break
        self.groundings = new_groundings

        if not self.groundings:
            return None
        if len(self.conditions) == 1:
            return self.conditions[0]
        return self

    def make_flat_preconditions(self, ground_precs, grounding):
        """ Make the flat list of ground preconditions
            (OrCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        ground_precs.append((self, grounding))

    def get_encode_conds(self, encode_conds, do_encode):
        """ Populate encode_conds with conditions that actually need to be
            properly encoded for invariants preprocessing and in SAT.
            (OrCondition, set([Condition])) -> None
        """
        encode_conds.add(self)
        for condition in self.conditions:
            condition.get_encode_conds(encode_conds, True)

class ForAllCondition(Condition):
    """ A formula consisting of a forall quantifier, a variable, and a condition. """

    def __init__(self, var, v_type, condition):
        """ Make a new ForAllCondition.
            (ForAllCondition, str, Type, Condition) -> None
        """
        super(ForAllCondition, self).__init__()
        self.var = var
        self.v_type = v_type
        self.condition = condition
        self.ground_conditions = {}
        self.desc = FORALL_CONDITION

    def __dump__(self):
        """ Return a full string representation of the condition
            (ForAllCondition) -> str
        """
        out_str = "(forall (" + self.var
        if self.v_type:
            out_str += " - " + str(self.v_type)
        return out_str + ") " + self.condition.__dump__() + ")"

    def __str__(self):
        """ Return a short string representation of the condition
            (ForAllCondition) -> str
        """
        out_str = "(forall " + self.var
        if self.v_type:
            out_str += " - " + str(self.v_type)
        return out_str + " ... )"

    def substitute_vars(self, substitutions):
        """ Replace the variables in this condition as specified in substitutions.
            Return a copy of the condition. We might need to also rename the
            quantifier variable.
            (ForAllCondition, { str : str }) -> ForAllCondition
        """
        subs = dict(substitutions)
        if self.var in list(substitutions.values()):
            for v in lower_var_alphabet:
                if v not in list(substitutions.values()):
                    subs[self.var] = v
                break
            assert self.var in subs
        else:
            subs[self.var] = self.var
        return ForAllCondition(self.var, self.v_type, self.condition.substitute_vars(subs))

    def substitute_derived_predicates(self, derived_predicates, seen_preds):
        """ Replace the derived predicates in the condition with the
            conditions of the derived predicates.
            (ForAllCondition, { Predicate : [DerivedPredicate] }, [Predicate]) -> ForAllCondition
        """
        self.condition = self.condition.substitute_derived_predicates(derived_predicates,
            seen_preds)
        return self

    def nnf(self, negation = False):
        """ Convert the condition to negation normal form.
            (ForAllCondition, bool) -> Condition
        """
        self.condition = self.condition.nnf(negation)
        if negation:
            return ExistsCondition(self.var, self.v_type, self.condition)
        return self

    def flatten(self):
        """ Flatten conjunctions and disjunctions.
            (ForAllCondition) -> None
        """
        self.condition.flatten()

    def has_quant(self):
        """ Return true iff this condition or one of its descendants is a quantifier
           (ForAllCondition) -> bool
        """
        return True

    def collect_neg_precs(self, neg_precs, param_types, collect = True):
        """ Recurse through the condition tree looking for negative preconditions
            (ForAllCondition, { str : Predicate }, { str : Type }, bool) -> None
        """
        param_types = dict(param_types)
        param_types[self.var] = self.v_type
        self.condition.collect_neg_precs(neg_precs, param_types, collect)

    def compute_relevant_vars(self, var_types):
        """ Compute, store, and return the relevant variables to this condition.
            (ForAllCondition, { str : Type } ) -> [str]
        """
        var_types = dict(var_types)
        assert self.var not in var_types
        var_types[self.var] = self.v_type
        self.relevant_vars = list(self.condition.compute_relevant_vars(var_types))
        if self.var in self.relevant_vars:
            self.relevant_vars.remove(self.var)
        else:
            print("Warning: problem contains a useless forall quantifier")
        self.var_types = {}
        for rv in self.relevant_vars:
            assert rv in var_types
            self.var_types[rv] = var_types[rv]
        self.var_indices = dict([(v, [i]) for i, v in enumerate(self.relevant_vars)])
        self.var_indices[self.var] = [len(self.relevant_vars)]
        return self.relevant_vars

    def assign_cond_code(self, cond_index, code_conds):
        """ Assign a code to this condition.
            (ForAllCondition, [int], { str : Condition }) -> None
        """
        self.cond_code = cond_prefix + str(cond_index[0])
        code_conds[self.cond_code] = self
        cond_index[0] += 1
        self.condition.assign_cond_code(cond_index, code_conds)

    def detect_statics(self, candidates, neg_candidates):
        """ Remove entries from candidates which are deleted somewhere in this cond.
            (ForAllCondition, set([(Predicate, [str])], set([(Predicate, [str])) -> None
        """
        self.condition.detect_statics(candidates, neg_candidates)

    def link_groundings(self, static_preds, neg_static_preds):
        """ Link the groundings in this condition to the groundings in its
            sub_conditions.

            We do the quantifiers backwards (working from their childrens
            groundings to theirs. This is so we can deal with the quantifiers
            introduced variable.

            (ForAllCondition, set([(Predicate, (str, ...))],
                set([(Predicate, (str, ...))])) -> Condition
        """
        self.condition = self.condition.link_groundings(static_preds, neg_static_preds)
        if self.condition is None:
            return None

        for cgrounding in self.condition.groundings:
            grounding = [None]*len(self.relevant_vars)
            for vid, var in enumerate(self.condition.relevant_vars):
                index = self.var_indices[var][0]
                if index >= len(self.relevant_vars):
                    var_val = cgrounding[vid]
                else:
                    grounding[index] = cgrounding[vid]
            grounding = tuple(grounding)
            if grounding not in self.ground_conditions:
                self.ground_conditions[grounding] = {}

            self.ground_conditions[grounding][var_val] = cgrounding

        new_groundings = []
        for grounding in self.groundings:
            if grounding in self.ground_conditions:
                new_groundings.append(grounding)
        self.groundings = new_groundings

        if not self.groundings:
            return None
        return self

    def make_flat_effects(self, ground_effects, grounding):
        """ Make the flat list of ground effects
            (ForAllCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        for cgrounding in list(self.ground_conditions[grounding].values()):
            self.condition.make_flat_effects(ground_effects, cgrounding)

    def make_flat_preconditions(self, ground_precs, grounding):
        """ Make the flat list of ground preconditions
            (ForAllCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        for cgrounding in list(self.ground_conditions[grounding].values()):
            self.condition.make_flat_preconditions(ground_precs, cgrounding)

    def get_encode_conds(self, encode_conds, do_encode):
        """ Populate encode_conds with conditions that actually need to be
            properly encoded for invariants preprocessing and in SAT.
            (ForAllCondition, set([Condition])) -> None
        """
        if do_encode:
            encode_conds.add(self)
        self.condition.get_encode_conds(encode_conds, do_encode)

class ExistsCondition(Condition):
    """ A formula consisting of an exists quantifier, a variable, and a condition."""

    def __init__(self, var, v_type, condition):
        """ Make a new ExistsCondition.
            (ExistsCondition, str, Type, Condition) -> None
        """
        super(ExistsCondition, self).__init__()
        self.var = var
        self.v_type = v_type
        self.condition = condition
        self.ground_conditions = {}
        self.desc = EXISTS_CONDITION

    def __dump__(self):
        """ Return a full string representation of the condition
            (ExistsCondition) -> str
        """
        out_str = "(exists (" + self.var
        if self.v_type:
            out_str += " - " + str(self.v_type)
        return out_str + ") " + self.condition.__dump__() + ")"

    def __str__(self):
        """ Return a short string representation of the condition
            (ExistsCondition) -> str
        """
        out_str = "(exists " + self.var
        if self.v_type:
            out_str += " - " + str(self.v_type)
        return out_str + " ... )"

    def substitute_vars(self, substitutions):
        """ Replace the variables in this condition as specified in substitutions.
            Return a copy of the condition. We might need to also rename the
            quantifier variable.

            (ExistsCondition, { str : str }) -> ExistsCondition
        """
        subs = dict(substitutions)
        if self.var in list(substitutions.values()):
            for v in lower_var_alphabet:
                if v not in list(substitutions.values()):
                    subs[self.var] = v
                break
            assert self.var in subs
        else:
            subs[self.var] = self.var
        return ExistsCondition(self.var, self.v_type, self.condition.substitute_vars(subs))

    def substitute_derived_predicates(self, derived_predicates, seen_preds):
        """ Replace the derived predicates in the condition with the
            conditions of the derived predicates.
            (ExistsCondition, { Predicate : [DerivedPredicate] }, [Predicate]) -> ExistsCondition
        """
        self.condition = self.condition.substitute_derived_predicates(derived_predicates,
            seen_preds)
        return self

    def nnf(self, negation = False):
        """ Convert the condition to negation normal form.
            (ExistsCondition, bool) -> Condition
        """
        self.condition = self.condition.nnf(negation)
        if negation:
            return ForAllCondition(self.var, self.v_type, self.condition)
        return self

    def flatten(self):
        """ Flatten conjunctions and disjunctions.
            (ExistsCondition) -> None
        """
        self.condition.flatten()

    def has_quant(self):
        """ Return true iff this condition or one of its descendants is a quantifier
           (ExistsCondition) -> bool
        """
        return True

    def collect_neg_precs(self, neg_precs, param_types, collect = True):
        """ Recurse through the condition tree looking for negative preconditions
            (ExistsCondition, { str : Predicate }, { str : Type }, bool) -> None
        """
        param_types = dict(param_types)
        param_types[self.var] = self.v_type
        self.condition.collect_neg_precs(neg_precs, param_types, collect)

    def compute_relevant_vars(self, var_types):
        """ Compute, store, and return the relevant variables to this condition.
            (ExistsCondition, { str : Type }) -> [str]
        """
        var_types = dict(var_types)
        assert self.var not in var_types
        var_types[self.var] = self.v_type

        self.relevant_vars = list(self.condition.compute_relevant_vars(var_types))
        if self.var in self.relevant_vars:
            self.relevant_vars.remove(self.var)
        else:
            print("Warning: problem contains a useless exists quantifier")
        self.var_types = {}
        for rv in self.relevant_vars:
            assert rv in var_types
            self.var_types[rv] = var_types[rv]
        self.var_indices = dict([(v, [i]) for i, v in enumerate(self.relevant_vars)])
        self.var_indices[self.var] = [len(self.relevant_vars)]
        return self.relevant_vars

    def assign_cond_code(self, cond_index, code_conds):
        """ Assign a code to this condition.
            (ExistsCondition, [int], { str : Condition }) -> None
        """
        self.cond_code = cond_prefix + str(cond_index[0])
        code_conds[self.cond_code] = self
        cond_index[0] += 1
        self.condition.assign_cond_code(cond_index, code_conds)

    def detect_statics(self, candidates, neg_candidates):
        """ Remove entries from candidates which are deleted somewhere in this cond.
            (ExistsCondition, set([(Predicate, [str])], set([(Predicate, [str])) -> None
        """
        self.condition.detect_statics(candidates, neg_candidates)

    def link_groundings(self, static_preds, neg_static_preds):
        """ Link the groundings in this condition to the groundings in its
            sub_conditions.

            We do the quantifiers backwards (working from their childrens
            groundings to theirs. This is so we can deal with the quantifiers
            introduced variable.

            (ExistsCondition, set([(Predicate, (str, ...))],
                set([(Predicate, (str, ...))])) -> Condition
        """
        self.condition = self.condition.link_groundings(static_preds, neg_static_preds)
        if self.condition is None:
            return None

        for cgrounding in self.condition.groundings:
            grounding = [None]*len(self.relevant_vars)
            for vid, var in enumerate(self.condition.relevant_vars):
                index = self.var_indices[var][0]
                if index >= len(self.relevant_vars):
                    var_val = cgrounding[vid]
                else:
                    grounding[index] = cgrounding[vid]
            grounding = tuple(grounding)
            if grounding not in self.ground_conditions:
                self.ground_conditions[grounding] = {}
            self.ground_conditions[grounding][var_val] = cgrounding

        new_groundings = []
        for grounding in self.groundings:
            if grounding in self.ground_conditions:
                new_groundings.append(grounding)
        self.groundings = new_groundings

        if not self.groundings:
            return None
        return self

    def make_flat_preconditions(self, ground_precs, grounding):
        """ Make the flat list of ground preconditions
            (ExistsCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        ground_precs.append((self, grounding))

    def get_encode_conds(self, encode_conds, do_encode):
        """ Populate encode_conds with conditions that actually need to be
            properly encoded for invariants preprocessing and in SAT.
            (ForAllCondition, set([Condition])) -> None
        """
        encode_conds.add(self)
        self.condition.get_encode_conds(encode_conds, True)

class IncreaseCondition(Condition):
    """ A formula consisting of an increase condition, a variable, and a value.
    """

    def __init__(self, var, value, value_args):
        """ Make a new IncreaseCondition.
            (IncreaseCondition, Function, int/Function, [str]) -> None
        """
        super(IncreaseCondition, self).__init__()
        self.var = var
        self.value = value
        self.value_args = value_args
        self.ground_conditions = {}
        self.desc = INCREASE_CONDITION

    def __dump__(self):
        """ Return a full string representation of the condition
            (IncreaseCondition) -> str
        """
        return self.__str__()

    def __str__(self):
        """ Return a short string representation of the condition
            (IncreaseCondition) -> str
        """
        if isinstance(self.value, int):
            return "(increase " + str(self.var) + " " + str(self.value) + ")"
        return "(increase " + str(self.var) + " (" + self.value.name + " " +\
            " ".join(self.value_args) + "))"

    def substitute_vars(self, substitutions):
        """ Replace the variables in this condition as specified in substitutions.
            Return a copy of the condition.
            (IncreaseCondition, { str : str }) -> IncreaseCondition
        """
        return IncreaseCondition(self.var, self.value, [substitutions[v] for v in self.value_args])

    def nnf(self, negation = False):
        """ Convert the condition to negation normal form.
            (IncreaseCondition, bool) -> Condition
        """
        assert not negation
        return self

    def compute_relevant_vars(self, var_types):
        """ Compute, store, and return the relevant variables to this condition.
            (IncreaseCondition, { str : Type } ) -> [str]
        """
        self.relevant_vars = list(self.value_args)
        self.var_types = {}
        self.var_indices = {}
        for vid, rv in enumerate(self.relevant_vars):
            assert rv in var_types
            self.var_types[rv] = var_types[rv]
            if rv not in self.var_indices:
                self.var_indices[rv] = []
            self.var_indices[rv].append(vid)
        return self.relevant_vars

    def assign_cond_code(self, cond_index, code_conds):
        """ Assign a code to this condition.
            (IncreaseCondition, [int], { str : Condition }) -> None
        """
        self.cond_code = cond_prefix + str(cond_index[0])
        code_conds[self.cond_code] = self
        cond_index[0] += 1

    def link_groundings(self, static_preds, neg_static_preds):
        """ If the value is not a number then we need to link the groundings
            to their values.
            (IncreaseCondition, set([(Predicate, (str, ...))],
                set([(Predicate, (str, ...))])) -> Condition
        """
        sub_indices = [self.var_indices[v] for v in self.value_args]
        for grounding in self.groundings:
            f_args = tuple([grounding[ii] for i in sub_indices for ii in i])
            if isinstance(self.value, Function):
                if f_args not in self.value.values:
                    raise ProblemException("Unknown increase function args: " +
                        ", ".join(f_args), grounding_error_code)
                self.ground_conditions[grounding] = self.value.values[f_args]
            else:
                self.ground_conditions[grounding] = self.value

        return self

    def make_flat_effects(self, ground_effects, grounding):
        """ Make the flat list of ground effects
            (IncreaseCondition, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        ground_effects.append((self, grounding))


class EqualsCondition(Condition):
    """ A formula consisting of an equlity constraint """

    def __init__(self, variables):
        """ Make a new EqualsCondition.
            (EqualsCondition, [int/Constant]) -> None
        """
        super(EqualsCondition, self).__init__()
        self.variables = variables
        self.sign = True
        self.desc = EQUALS_CONDITION

    def __dump__(self):
        """ Return a full string representation of the condition
            (EqualsCondition) -> str
        """
        return self.__str__()

    def __str__(self):
        """ Return a short string representation of the condition
            (EqualsCondition) -> str
        """
        if self.sign:
            return "(= " + self.variables[0] + " " + self.variables[1] + ")"
        else:
            return "(!= " + self.variables[0] + " " + self.variables[1] + ")"

    def substitute_vars(self, substitutions):
        """ Replace the variables in this condition as specified in substitutions.
            Return a copy of the condition.
            (EqualsCondition, { str : str }) -> EqualsCondition
        """
        return EqualsCondition([substitutions[v] for v in self.variables])

    def nnf(self, negation = False):
        """ Convert the condition to negation normal form.
            (EqualsCondition, bool) -> Condition
        """
        if negation:
            self.sign = False
        return self

    def collect_neg_precs(self, neg_precs, param_types, collect = True):
        """ Recurse through the condition tree looking for negative preconditions
            (EqualsCondition, { str : Predicate }, { str : Type }, bool) -> None
        """
        if not self.sign and collect:
            if inequality_prefix not in neg_precs:
                neg_precs[inequality_prefix] = []
            for v in self.variables:
                assert v in param_types
            neg_precs[inequality_prefix].append([param_types[v] for v in self.variables])

    def compute_relevant_vars(self, var_types):
        """ Compute, store, and return the relevant variables to this condition.
            (EqualsCondition, { str : Type }) -> [str]
        """
        self.relevant_vars = []
        self.var_types = {}
        self.var_indices = {}
        for vid, rv in enumerate(self.variables):
            if rv[0] == "?":
                assert rv in var_types
                self.relevant_vars.append(rv)
                self.var_types[rv] = var_types[rv]
                if rv not in self.var_indices:
                    self.var_indices[rv] = []
                self.var_indices[rv].append(vid)
        return self.relevant_vars

    def assign_cond_code(self, cond_index, code_conds):
        """ Assign a code to this condition.
            (EqualsCondition, [int], { str : Condition }) -> None
        """
        self.cond_code = cond_prefix + str(cond_index[0])
        code_conds[self.cond_code] = self
        cond_index[0] += 1

    def link_groundings(self, static_preds, neg_static_preds):
        """ This condition will be removed.
            (EqualsCondition, set([(Predicate, (str, ...))],
                set([(Predicate, (str, ...))])) -> None
        """
        return None

class ConditionalEffect(Condition):
    """ A conditional effect. """

    def __init__(self, condition, effect):
        """ Make a new conditional effect.
            (ConditionalEffect, Condition, Condition) -> None
        """
        super(ConditionalEffect, self).__init__()
        self.condition = condition
        self.effect = effect
        self.ground_preconditions = {}
        self.ground_effects = {}

        self.flat_ground_effects = {}
        self.flat_ground_preconditions = {}
        self.desc = CONDITIONAL_EFFECT

    def __dump__(self):
        """ Write a string representation of the effect.
            (ConditionalEffect) -> None
        """
        return "(when " + self.condition.__dump__() + " " +\
            self.effect.__dump__() + ")"

    def __str__(self):
        """Return a short string representation of the effect
            (ConditionalEffect) -> str
        """
        return "(when ...)"

    def substitute_derived_predicates(self, derived_predicates, seen_preds):
        """ Replace the derived predicates in the conditional effect with the
            conditions of the derived predicates.

            (ConditionalEffect, { Predicate : [DerivedPredicate] }, [Predicate]) -> ConditionalEffect
        """
        self.condition = self.condition.substitute_derived_predicates(derived_predicates, seen_preds)
        return self

    def nnf(self, negation = False):
        """ Convert the conditions of this conditional effect into NNF.
            (ConditionalEffect, bool) -> Condition
        """
        assert not negation
        self.condition = self.condition.nnf(negation)
        self.effect = self.effect.nnf(negation)
        return self

    def flatten(self):
        """ Flatten conjunctions and disjunctions.
            (ConditionalEffect) -> None
        """
        self.condition.flatten()
        self.effect.flatten()

    def collect_neg_precs(self, neg_precs, param_types, collect = True):
        """ Recurse through the condition tree looking for negative preconditions
            (ConditionalEffect, { str : Predicate }, { str : Type } ) -> None
        """
        self.condition.collect_neg_precs(neg_precs, param_types, True)

    def compute_relevant_vars(self, var_types):
        """ Compute, store, and return the relevant variables to this effect.
            (ConditionalEffect, { str : Type }) -> [str]
        """
        self.relevant_vars = list(self.condition.compute_relevant_vars(var_types))
        eff_rv = self.effect.compute_relevant_vars(var_types)
        for rv in eff_rv:
            if rv not in self.relevant_vars:
                self.relevant_vars.append(rv)
        self.var_types = {}
        for rv in self.relevant_vars:
            assert rv in var_types
            self.var_types[rv] = var_types[rv]
        self.var_indices = dict([(v, [i]) for i, v in enumerate(self.relevant_vars)])
        return self.relevant_vars

    def assign_cond_code(self, cond_index, code_conds):
        """ Assign a code to this condition.
            (ConditionalEffect, [int], { str : Condition }) -> None
        """
        self.cond_code = cond_prefix + str(cond_index[0])
        code_conds[self.cond_code] = self
        cond_index[0] += 1
        self.condition.assign_cond_code(cond_index, code_conds)
        self.effect.assign_cond_code(cond_index, code_conds)

    def detect_statics(self, candidates, neg_candidates):
        """ Remove entries from candidates which are deleted somewhere in this effect.
            (ConditionalEffect, set([(Predicate, [str])], set([(Predicate, [str])) -> None
        """
        self.effect.detect_statics(candidates, neg_candidates)

    def link_groundings(self, static_preds, neg_static_preds):
        """ Link the groundings in this condition to the groundings in its
            sub_conditions and remove condtions with no groundings or that are
            static.
            (ConditionalEffect, set([(Predicate, (str, ...))],
                set([(Predicate, (str, ...))])) -> Condition
        """
        self.effect = self.effect.link_groundings(static_preds, neg_static_preds)
        if self.effect is None:
            return None

        self.condition = self.condition.link_groundings(static_preds, neg_static_preds)
        if self.condition is None:
            return self.effect

        pre_sub_indices = [self.var_indices[v][0] for v in self.condition.relevant_vars]
        pre_groundings = set(self.condition.groundings)
        eff_sub_indices = [self.var_indices[v][0] for v in self.effect.relevant_vars]
        eff_groundings = set(self.effect.groundings)

        new_groundings = []
        for grounding in self.groundings:
            eff_sub_grounding = tuple([grounding[i] for i in eff_sub_indices])
            if eff_sub_grounding in eff_groundings:
                self.ground_effects[grounding] = eff_sub_grounding
                new_groundings.append(grounding)
                pre_sub_grounding = tuple([grounding[i] for i in pre_sub_indices])
                if pre_sub_grounding in pre_groundings:
                    self.ground_preconditions[grounding] = pre_sub_grounding
        self.groundings = new_groundings

        if not self.groundings:
            return None
        return self

    def make_flat_effects(self, ground_effects, grounding):
        """ Make the flat list of ground effects
            (ConditionalEffect, [(Predicate, bool, (str, ...))], (str, ...)) -> None
        """
        ground_effects.append((self, grounding))
        t_effects = []
        self.effect.make_flat_effects(t_effects, self.ground_effects[grounding])
        self.flat_ground_effects[grounding] = t_effects
        t_precs = []
        self.condition.make_flat_preconditions(t_precs, self.ground_preconditions[grounding])
        self.flat_ground_preconditions[grounding] = t_precs

    def get_encode_conds(self, encode_conds, do_encode):
        """ Populate encode_conds with conditions that actually need to be
            properly encoded for invariants preprocessing and in SAT.
            (ForAllCondition, set([Condition])) -> None
        """
        encode_conds.add(self)
        self.condition.get_encode_conds(encode_conds, False)
        self.effect.get_encode_conds(encode_conds, False)

class Action:
    """ A non-grounded planning action """

    def __init__(self, name, parameters, types, precondition, effect, is_derived):
        """ Make a new a action.
            (Action, str, [str], [Type], Condition, Condition, bool) -> None
        """
        self.name = name
        self.param_names = parameters
        self.parameters = list(zip(parameters, types))
        self.param_types = dict([(p, t) for (p, t) in self.parameters])
        self.precondition = precondition
        self.effect = effect
        self.is_derived = is_derived
        self.is_noop = False

        self.groundings = []
        self.ground_preconditions = {}
        self.ground_effects = {}

        #These will be lists of PredicateConditions or Conditional Effects
        self.flat_ground_effects = {}
        self.flat_ground_preconditions = {}

    def __dump__(self):
        """ Write a string representation of the operator to the given file in
            the fast-downward output format.
            (Action, file) -> None
        """
        if self.is_derived:
            return "(:derived " + self.effect.__dump__() + "\n  " +\
                self.precondition.__dump__() + "\n)\n"

        out_str =  "(:action " + self.name + "\n"
        out_str += "   :parameters (" + " ".join([p + " - " + str(t)
            for p,t in self.parameters]) + ")\n"
        out_str += "   :precondition (and\n"
        if isinstance(self.precondition, PredicateCondition):
            out_str += "    " + self.precondition.__dump__()
        else:
            assert isinstance(self.precondition, AndCondition)
            for cond in self.precondition.conditions:
                out_str += "     " + cond.__dump__() + "\n"
        out_str += "   )\n"
        out_str += "   :effect (and\n"
        if isinstance(self.effect, PredicateCondition):
            out_str += "    " +self.effect.__dump__()
        else:
            assert isinstance(self.effect, AndCondition)
            for cond in self.effect.conditions:
                out_str += "     " + cond.__dump__() + "\n"
        out_str += "   )\n"
        out_str += ")\n"
        return out_str

    def __str__(self):
        """ Return a short string representation of the operator.
            (Action) -> str
        """
        if self.is_derived:
            return "(:derived " + self.pred_cond.__dump__() + " ...)"
        return "( " + self.name + " ... )"


    def substitute_derived_predicates(self, derived_predicates):
        """ Replace the derived predicates in the actions precondition and
            the conditions of its conditional effects, with the conditions
            of the derived predicates.
            (Action, { (Predicate) : [DerivedPredicate] }) -> None
        """
        if self.precondition:
            self.precondition = self.precondition.substitute_derived_predicates(derived_predicates, [])
        self.effect = self.effect.substitute_derived_predicates(derived_predicates, [])

    def nnf(self):
        """ Convert the conditions of this conditional effect into NNF.
            (Action, bool) -> None
        """
        if self.precondition:
            self.precondition = self.precondition.nnf()
        self.effect = self.effect.nnf()

    def flatten(self):
        """ Flatten conjunctions and disjunctions.
            (Action) -> None
        """
        if self.precondition:
            self.precondition.flatten()
        self.effect.flatten()

    def collect_neg_precs(self, neg_precs, param_types):
        """ Recurse through the condition tree looking for negative preconditions
            (Action, { str : Predicate }, { str : Type } ) -> None
        """
        if self.precondition:
            self.precondition.collect_neg_precs(neg_precs, param_types, True)
        self.effect.collect_neg_precs(neg_precs, param_types, False)

    def compute_relevant_vars(self):
        """ Compute, store, and return the relevant variables to this dp.
            (Action) -> set([str])
        """
        self.relevant_vars = list(self.param_names)
        if self.precondition:
            self.precondition.compute_relevant_vars(self.param_types)
        self.effect.compute_relevant_vars(self.param_types)
        self.var_indices = dict([(v, i) for i, v in enumerate(self.relevant_vars)])
        return self.relevant_vars

    def detect_statics(self, candidates, neg_candidates):
        """ Remove entries from candidates which are deleted somewhere in this
            action.
            (Action, set([(Predicate, [str])], set([(Predicate, [str])) -> None
        """
        self.effect.detect_statics(candidates, neg_candidates)

    def link_groundings(self, static_preds, neg_static_preds):
        """ Link the groundings in this action to the groundings in its
            pre and post conditions. And do the same for the conditions in these.

            Remove conditions from this action which have no groundings,
            which refer only to static predicates, equalities, etc.

            (Action, set([(Predicate, (str, ...))]), set([(Predicate, (str, ...))])) -> None
        """
        self.effect = self.effect.link_groundings(static_preds, neg_static_preds)
        if self.effect is None:
            self.groundings = []
            return
        eff_groundings = set(self.effect.groundings)

        if self.precondition:
            self.precondition = self.precondition.link_groundings(static_preds, neg_static_preds)
            pre_groundings = set(self.precondition.groundings)

        new_groundings = []
        for grounding in self.groundings:
            eff_sub_grounding = tuple([grounding[self.var_indices[v]]\
                for v in self.effect.relevant_vars])
            if eff_sub_grounding in eff_groundings:
                self.ground_effects[grounding] = eff_sub_grounding
                new_groundings.append(grounding)

                if self.precondition:
                    pre_sub_grounding = tuple([grounding[self.var_indices[v]]\
                        for v in self.precondition.relevant_vars])
                    if pre_sub_grounding in pre_groundings:
                        self.ground_preconditions[grounding] = pre_sub_grounding

        self.groundings = new_groundings

    def make_flat_effects(self):
        """ Make the flat list of ground effects
            (Action) -> None
        """
        for grounding in self.groundings:
            flat_effs = []
            self.effect.make_flat_effects(flat_effs, self.ground_effects[grounding])
            self.flat_ground_effects[grounding] = flat_effs

    def make_flat_preconditions(self):
        """ Make the flat list of ground preconditions
            (Action) -> None
        """
        for grounding in self.groundings:
            flat_precs = []
            if self.precondition:
                self.precondition.make_flat_preconditions(flat_precs,
                    self.ground_preconditions[grounding])
            self.flat_ground_preconditions[grounding] = flat_precs

    def get_encode_conds(self, encode_conds):
        """ Populate encode_conds with conditions that actually need to be
            properly encoded for invariants preprocessing and in SAT.
            (Action, set([Condition])) -> None
        """
        self.precondition.get_encode_conds(encode_conds, False)
        self.effect.get_encode_conds(encode_conds, False)

    def make_strips_conditions(self):
        """ Make pre and post-conditions for each grounding which link directly
            to the predicates involved. Assumes strips with negaitve precs.
            (Action) -> None
        """
        self.strips_preconditions = {}
        self.strips_effects = {}
        for grounding in self.groundings:
            precs = set()
            for prec in self.flat_ground_preconditions[grounding]:
                assert isinstance(prec[0], PredicateCondition)
                precs.add((prec[0].pred, prec[0].ground_conditions[prec[1]], prec[2]))
            self.strips_preconditions[grounding] = precs
            effs = set()
            for eff in self.flat_ground_effects[grounding]:
                if isinstance(eff[0], PredicateCondition):
                    effs.add((eff[0].pred, eff[0].ground_conditions[eff[1]], eff[2]))
            self.strips_effects[grounding] = effs
    def __lt__(self, other) :
        return str(self) < str(other)

class Problem:
    """ An instance of a ADL planning problem. After parsing this class also
        represents a PDDL planning problem. """

    default_type = Type(default_type_name, None)

    def __init__(self, name):
        """ Make a new problem instance with the given name.

            (Problem, str) -> None
        """
        self.name = name
        self.problem = None
        self.requirements = []

        self.types = { self.default_type.name : self.default_type }
        self.predicates = {}
        self.functions = {}
        self.actions = {}
        self.derived_predicates = {}

        self.objects = {}
        self.initial_state = []
        self.initial_state_set = None
        self.goal = None

        self.inequalities = []
        self.inequality_set = None
        self.neg_initial_state = []
        self.neg_initial_state_set = None

        self.neg_precs = set()

        self.conditions = []
        self.conditional_effects = []

        #A map from condition codes to conditions
        self.code_conds = {}

        self.state_mutexes = None
        self.first_layer_fluents = None
        self.first_layer_actions = None

    def __str__(self):
        """ Return a short string representation of the problem
            (Problem) -> str
        """
        return self.name

    def simplify(self):
        """ Convert to NNF and flatten conjunctions and disjunctions.
            (Problem) -> None
        """
        neg_precs = {}
        for action in list(self.actions.values()):
            if self.derived_predicates:
                action.substitute_derived_predicates(self.derived_predicates)
            action.nnf()
            action.flatten()
            action.collect_neg_precs(neg_precs, action.param_types)
            action.compute_relevant_vars()

        if self.derived_predicates:
            self.goal = self.goal.substitute_derived_predicates(self.derived_predicates, [])

        self.derived_predicates = None

        self.goal = self.goal.nnf()
        self.goal.flatten()
        self.goal.collect_neg_precs(neg_precs, {})
        self.goal.compute_relevant_vars({})

        #Make lists of the negative fluents and inequalities
        for pred in list(neg_precs.values()):
           if isinstance(pred, list):
               for t1, t2 in pred:
                   for v1, v2 in itertools.product(t1.objects, t2.objects):
                       if v1 != v2:
                           self.inequalities.append((v1.name, v2.name))
           else:
               self.neg_precs.add(pred)
               if not pred.types:
                   if (pred, ()) not in self.initial_state_set:
                       self.neg_initial_state.append((pred, ()))
               else:
                   for tvars in itertools.product(*[[o.name for o in t.objects] for t in pred.types]):
                       tvars = tuple(tvars)
                       if (pred, tvars) not in self.initial_state_set:
                           self.neg_initial_state.append((pred, tvars))

        self.inequality_set = set(self.inequalities)
        self.neg_initial_state_set = set(self.neg_initial_state)


    def assign_cond_codes(self):
        """ Assign condition codes to the conditions in the problem.
            (Problem) -> None
        """
        cond_index = [0]
        self.goal.assign_cond_code(cond_index, self.code_conds)
        for action in list(self.actions.values()):
            if action.precondition:
                action.precondition.assign_cond_code(cond_index, self.code_conds)
                action.effect.assign_cond_code(cond_index, self.code_conds)

    def compute_static_preds(self):
        """ Compute the static predicates.
            (Problem) -> None
        """
        self.static_preds = set(self.initial_state_set)
        self.neg_static_preds = set(self.neg_initial_state_set)

        for action in list(self.actions.values()):
            if self.static_preds or self.neg_static_preds:
                action.detect_statics(self.static_preds, self.neg_static_preds)
            else: break

    def link_groundings(self):
        """ Link the groundings between all of the conditions and actions and
            predicates. Also do the goal.

            (Problem) -> None
        """
        #Remove statics from the initial state
        if self.static_preds:
            new_initial = []
            for init in self.initial_state:
                if init not in self.static_preds:
                    new_initial.append(init)
            self.initial_state = new_initial
            self.initial_state_set = set(self.initial_state)

        if self.neg_static_preds:
            #This should never occur - basically negative statics just dont exist
            assert False
            new_neg_initial = []
            for init in self.neg_initial_state:
                if init not in self.neg_static_preds:
                    new_neg_initial.append(init)
            self.neg_initial_state = new_neg_initial
            self.neg_initial_state_set = set(self.neg_initial_state)

        #Remove static groundings from predicates
        for pred in list(self.predicates.values()):
            new_groundings = []
            for grounding in pred.groundings:
                if (pred, grounding) not in self.static_preds:
                    new_groundings.append(grounding)
            pred.groundings = new_groundings

        new_actions = []
        for action in list(self.actions.values()):
            action.link_groundings(self.static_preds, self.neg_static_preds)
            if action.groundings:
                new_actions.append(action)
        self.actions = dict([(a.name, a) for a in new_actions])

        self.goal = self.goal.link_groundings(self.static_preds, self.neg_static_preds)


    def make_flat_effects(self):
        """ Make the flat list of ground effects
            (Problem) -> None
        """
        for action in list(self.actions.values()):
            action.make_flat_effects()

    def make_flat_preconditions(self):
        """ Make the flat list of ground preconditions (we only flatten up
            until we hit disjunctions or existential quantifiers.
            (Problem) -> None
        """
        for action in list(self.actions.values()):
            action.make_flat_preconditions()

        flat_goal_precs = []
        self.goal.make_flat_preconditions(flat_goal_precs, ())
        self.flat_ground_goal_preconditions = flat_goal_precs

    def get_encode_conds(self):
        """ Populate encode_conds with conditions that actually need to be
            properly encoded for invariants preprocessing and in SAT.
            (Problem, set([Condition])) -> None
        """
        self.encode_conds = set()
        for action in list(self.actions.values()):
            action.get_encode_conds(self.encode_conds)

        self.goal.get_encode_conds(self.encode_conds, False)

    def make_cond_and_cond_eff_lists(self):
        """ Make seperate lists of conditions and conditional effects that will
            actually be encoded.
            (Problem) -> None
        """
        for cond in list(self.code_conds.values()):
            if cond in self.encode_conds:
                if isinstance(cond, ConditionalEffect):
                    self.conditional_effects.append(cond)
                else:
                    self.conditions.append(cond)

    def link_conditions_to_actions(self):
        """ Make links from the groundings of conditions to the groundings
            of actions, where these groundings represent the direct pre- and
            post conditions of actions. We use this for mutex and SSAs.

            (Problem) -> None
        """
        #FOR NOW THIS IS ASSUMING THAT WE HAVE STRIPS (with possible NPRECS)
        for cond in itertools.chain(self.conditions, self.conditional_effects):
            if cond.groundings:
                cond.ground_precs = {}
                cond.ground_nprecs = {}
                cond.ground_adds = {}
                cond.ground_dels = {}
            for grounding in cond.groundings:
                cond.ground_precs[grounding] = set()
                cond.ground_nprecs[grounding] = set()
                cond.ground_adds[grounding] = set()
                cond.ground_dels[grounding] = set()

        for pred in list(self.predicates.values()):
            if pred.groundings:
                pred.ground_precs = {}
                pred.ground_nprecs = {}
                pred.ground_adds = {}
                pred.ground_dels = {}
            for grounding in pred.groundings:
                pred.ground_precs[grounding] = set()
                pred.ground_nprecs[grounding] = set()
                pred.ground_adds[grounding] = set()
                pred.ground_dels[grounding] = set()

        for action in list(self.actions.values()):
            for grounding in action.groundings:
                ag_pair = (action, grounding)
                for prec in action.flat_ground_preconditions[grounding]:
                    if isinstance(prec[0], PredicateCondition):
                        if prec[2]:
                            prec[0].pred.ground_precs[prec[0].ground_conditions[prec[1]]].add(ag_pair)
                        else:
                            prec[0].pred.ground_nprecs[prec[0].ground_conditions[prec[1]]].add(ag_pair)
                    else:
                        prec[0].ground_precs[prec[1]].add(ag_pair)

                for eff in action.flat_ground_effects[grounding]:
                    if isinstance(eff[0], PredicateCondition):
                        if eff[2]:
                            eff[0].pred.ground_adds[eff[0].ground_conditions[eff[1]]].add(ag_pair)
                        else:
                            eff[0].pred.ground_dels[eff[0].ground_conditions[eff[1]]].add(ag_pair)
                    elif not isinstance(eff[0], IncreaseCondition):
                        eff[0].ground_adds[eff[1]].append(ag_pair)

    def make_strips_conditions(self):
        """ Make pre and post-conditions for each grounding which link directly
            to the predicates involved. Assumes strips with negaitve precs.
            (Problem) -> None
        """
        for action in list(self.actions.values()):
            action.make_strips_conditions()


    def compute_conflict_mutex(self):
        """ Compute conflict mutex relationships.
            (Problem) -> None
        """
        #Conflict mutex:
        self.conflicts = {}
        self.eff_eff_conflicts = {}
        self.pre_eff_conflicts = {}

        for action in list(self.actions.values()):
            for grounding in action.groundings:
                ag_pair = (action, grounding)
                self.conflicts[ag_pair] = set()
                self.eff_eff_conflicts[ag_pair] = set()
                self.pre_eff_conflicts[ag_pair] = set()

        for action1 in list(self.actions.values()):
            for grounding1 in action1.groundings:
                ag_pair1 = (action1, grounding1)
                for eff in action1.flat_ground_effects[grounding1]:
                    if isinstance(eff[0], IncreaseCondition): continue
                    #Assuming STRIPS
                    if eff[2]:
                        e_list = eff[0].pred.ground_dels[eff[0].ground_conditions[eff[1]]]
                        p_list = eff[0].pred.ground_nprecs[eff[0].ground_conditions[eff[1]]]
                    else:
                        e_list = eff[0].pred.ground_adds[eff[0].ground_conditions[eff[1]]]
                        p_list = eff[0].pred.ground_precs[eff[0].ground_conditions[eff[1]]]

                    #Eff - Eff
                    for ag_pair2 in e_list:
                        if ag_pair1 != ag_pair2:
                            self.conflicts[ag_pair1].add(ag_pair2)
                            self.eff_eff_conflicts[ag_pair1].add(ag_pair2)
                    #Pre - Eff
                    for ag_pair2 in p_list:
                        if ag_pair1 != ag_pair2:
                            self.conflicts[ag_pair1].add(ag_pair2)
                            self.conflicts[ag_pair2].add(ag_pair1)
                            self.pre_eff_conflicts[ag_pair1].add(ag_pair2)
                            self.pre_eff_conflicts[ag_pair2].add(ag_pair1)


    def simulate_plan(self, plan):
        """ Simulate the suplied plan and return its validity and cost
            (Problem, [[(Action, (str,))]]) -> bool, cost
        """
        ########### ASSUMING STRIPS (with n-precs)
        state = set(self.initial_state_set)
        cost = 0

        #The grounding might not just be enough to do this stuff because it
        #does not take into account constants - we need to look
        #inside the PredicateCondtions a bit deeper.
        for sid, step in enumerate(plan):
            step_pre = set()
            step_npre = set()
            step_add = set()
            step_del = set()
            for action, grounding in step:
                action_add = set()
                action_del = set()
                for eff in action.flat_ground_effects[grounding]:
                    if isinstance(eff[0], IncreaseCondition):
                        cost += eff[0].ground_conditions[eff[1]]
                    else:
                        assert isinstance(eff[0], PredicateCondition)
                        eff_pair = (eff[0].pred, eff[0].ground_conditions[eff[1]])
                        if eff[2]:
                            if eff_pair in action_del:
                                step_del.remove(eff_pair)
                            if eff_pair in step_npre or eff_pair in step_del:
                                print(("Error at step", sid, "mutex conflict on:",\
                                    eff_pair[0].name, eff_pair[1]))
                                return False, 0
                            step_add.add(eff_pair)
                            action_add.add(eff_pair)
                        else:
                            if eff_pair in action_add: continue
                            if eff_pair in step_pre or eff_pair in step_add:
                                print(("Error at step", sid, "mutex conflict on:",\
                                    eff_pair[0].name, eff_pair[1]))
                                return False, 0
                            step_del.add(eff_pair)
                            action_del.add(eff_pair)

                for pre in action.flat_ground_preconditions[grounding]:
                    assert isinstance(pre[0], PredicateCondition)
                    pre_pair = (pre[0].pred, pre[0].ground_conditions[pre[1]])
                    if pre[2]:
                        if pre_pair not in state:
                            print(("Error at step", sid, "invalid precondition:",\
                                pre_pair[0].name, pre_pair[1], "of action:", action.name, grounding))
                            return False, 0
                        step_pre.add(pre_pair)
                    else:
                        if pre_pair in state:
                            print(("Error at step", sid, "invalid neg precondition:",\
                                pre_pair[0].name, pre_pair[1], "of action:", action.name, grounding))
                            return False, 0
                        step_npre.add(pre_pair)
                for eff_pair in step_del:
                    state.discard(eff_pair)
                for eff_pair in step_add:
                    state.add(eff_pair)

        #check goal
        for pre in self.flat_ground_goal_preconditions:
            assert isinstance(pre[0], PredicateCondition)
            t_grounding = list(pre[0].variables)
            for vid, var in enumerate(pre[0].relevant_vars):
                for vi in pre[0].var_indices[var]:
                    t_grounding[vi] = pre[1][vid]
            t_grounding = tuple(t_grounding)
            pre_pair = (pre[0].pred, t_grounding)
            if pre[2]:
                if pre_pair not in state:
                    print(("Unsatisfied goal:", pre_pair[0].name, " ".join(pre_pair[1])))
                    return False, 0
            else:
                if pre_pair in state:
                    print(("Unsatisfied negative goal:", pre_pair[0].name, " ".join(pre_pair[1])))
                    return False, 0

        return True, cost

    def make_strips_problem(self):
        """ Return an instance of strips_problem.Problem made from this problem.
            (Problem) -> strips_problem.Problem
        """

        not_prefix = "not_"
        problem = strips_problem.Problem()

        #Objects
        problem.objects = dict(self.objects)

        #Propositions
        propositions = {}
        for predicate in list(self.predicates.values()):
            for grounding in predicate.groundings:
                 prop = strips_problem.Proposition(predicate.name, list(grounding))
                 propositions[(predicate, grounding)] = prop
                 problem.propositions.append(prop)

        neg_propositions = {}

        #Actions
        actions = {}
        for action in list(self.actions.values()):
            for grounding in action.groundings:
                strips_action = strips_problem.Action(action.name, list(grounding))
                problem.actions.append(strips_action)
                actions[(action, grounding)] = strips_action
                for prec in action.flat_ground_preconditions[grounding]:
                    if not isinstance(prec[0], PredicateCondition):
                        raise ProblemException("Error: complex precondition detected in action:" +\
                            action.name, "\nThis system does not allow disjunction or existential " +
                            "quantifiers in preconditions.")

                    fg_pair = (prec[0].pred, prec[0].ground_conditions[prec[1]])
                    prop = propositions[fg_pair]
                    if not prec[2]:
                        if fg_pair not in neg_propositions:
                            neg_pred = not_prefix+fg_pair[0].name
                            prop = strips_problem.Proposition(neg_pred, list(fg_pair[1]))
                            propositions[(neg_pred, grounding)] = prop
                            problem.propositions.append(prop)
                            neg_propositions[fg_pair] = prop
                        else:
                            prop = neg_propositions[fg_pair]

                    strips_action.preconditions.append(prop)
                    prop.preconditions.append(strips_action)

                for eff in action.flat_ground_effects[grounding]:
                    if isinstance(eff[0], ConditionalEffect):
                        raise ProblemException("Error: this system does not support " +\
                            "conditional effects.")

                    if isinstance(eff[0], PredicateCondition):
                        prop = propositions[(eff[0].pred, eff[0].ground_conditions[eff[1]])]
                        if eff[2]:
                            strips_action.pos_effects.append(prop)
                            prop.pos_effects.append(strips_action)
                        else:
                            strips_action.neg_effects.append(prop)
                            prop.neg_effects.append(strips_action)

        #Prune delete effects that are added by the same action
        for action in problem.actions:
            for prop in action.pos_effects:
                if prop in action.neg_effects:
                    action.neg_effects.remove(prop)
                    prop.neg_effects.remove(action)

        #Initial State
        for predicate in list(self.predicates.values()):
            for grounding in predicate.groundings:
                prop = (predicate, grounding)
                if prop in self.initial_state:
                    problem.pos_initial_state.append(propositions[prop])
                else:
                    problem.neg_initial_state.append(propositions[prop])

        #Goal
        for prec in self.flat_ground_goal_preconditions:
            if not isinstance(prec[0], PredicateCondition):
                raise ProblemException("Error: this system does not support " +\
                    "non-conjunctive goals.")
            fg_pair = (prec[0].pred, prec[0].ground_conditions[prec[1]])
            prop = propositions[fg_pair]
            if not prec[2]:
                if fg_pair not in neg_propositions:
                    neg_pred = not_prefix+fg_pair[0].name
                    prop = strips_problem.Proposition(neg_pred, list(fg_pair[1]))
                    propositions[(neg_pred, grounding)] = prop
                    problem.propositions.append(prop)
                    neg_propositions[fg_pair] = prop
                else:
                    prop = neg_propositions[fg_pair]

            problem.goal.append(prop)

        #If there are any negative preconditions, augment the effects of
        #actions to deal with them
        for (predicate, grounding), prop in list(neg_propositions.items()):
            #Effects
            for action in predicate.ground_adds[grounding]:
                strips_action = actions[action]
                strips_action.neg_effects.append(prop)
                prop.neg_effects.append(strips_action)
            for action in predicate.ground_dels[grounding]:
                strips_action = actions[action]
                strips_action.pos_effects.append(prop)
                prop.pos_effects.append(strips_action)
            #Initial State
            if (predicate, grounding) in self.initial_state:
                problem.neg_initial_state.append(prop)
            else:
                problem.pos_initial_state.append(prop)

        #Prune useless actions that don't add anything more than their precondititions
        actions_to_remove = [action for action in problem.actions if not\
            [prop for prop in action.pos_effects if prop not in action.preconditions]]

        for action in actions_to_remove:
            problem.actions.remove(action)
            for prop in action.preconditions:
                prop.preconditions.remove(action)
            for prop in action.pos_effects:
                prop.pos_effects.remove(action)
            for prop in action.neg_effects:
                prop.neg_effects.remove(action)

        #First layers
        if self.first_layer_actions is not None:
            problem.action_first_step = {}
            for action, step in list(self.first_layer_actions.items()):
                if action in actions and actions[action] in problem.actions:
                    problem.action_first_step[actions[action]] = step

        #State mutexes
        if self.state_mutexes is not None:
            problem.fluent_mutex = {}
            for step, mutexes in list(self.state_mutexes.items()):
                problem.fluent_mutex[step] = []
                for (prop1, grounding1, sign1), (prop2, grounding2, sign2) in mutexes:
                    if not sign1 or not sign2: continue
                    problem.fluent_mutex[step].append((propositions[(prop1, grounding1)],
                        propositions[(prop2, grounding2)]))

        return problem

    def make_plan_from_strips(self, plan):
        """ Return a plan made for this type of Problem from a plan made for
            strips_problem.Problem.
            (Problem, [[strips_problem.Action]]) -> [[(problem.Action, grounding)]]
        """
        new_plan = []
        for actions in plan:
            new_plan.append([(self.actions[a.name], tuple(a.parameters)) for a in actions])
        return new_plan

    def simulate_strips_plan(self, problem, plan):
        """ Simulate the suplied plan and return its validity and cost
            (Problem, [[(Action, (str,))]]) -> bool, cost
        """
        state = set(problem.pos_initial_state)
        success = True
        for sid, step in enumerate(plan):
            step_pre = set()
            step_add = set()
            step_del = set()
            for action in step:
                for pre in action.preconditions:
                    if pre not in state:
                        print(("Error at step", sid, "unsatisifed preconditon", pre, "of action", action))
                        success = False
                    if pre in step_del:
                        print(("Error at step", sid, "mutex conflict on:", pre))
                        success = False
                for eff in action.pos_effects:
                    if eff in step_del:
                        print(("Error at step", sid, "mutex conflict on:", eff))
                        success = False
                for eff in action.neg_effects:
                    if eff in step_pre or eff in step_add:
                        print(("Error at step", sid, "mutex conflict on:", eff))
                        success = False

                step_pre.update(action.preconditions)
                step_add.update(action.pos_effects)
                step_del.update(action.neg_effects)

            for prop in step_del:
                state.discard(prop)
            for prop in step_add:
                state.add(prop)

        for prop in problem.goal:
            if prop not in state:
                print(("Unsatisfied goal:", prop))
                success = False

        return success, 0
