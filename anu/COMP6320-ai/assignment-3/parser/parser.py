# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" This file parses the PDDL file and creates a Problem as defined in problem.py """

from pyparsing import OneOrMore, nestedExpr

from problem import (Action, AndCondition, ConditionalEffect, EqualsCondition,
                     ExistsCondition, ForAllCondition, Function,
                     IncreaseCondition, NotCondition, Object, OrCondition,
                     Predicate, PredicateCondition, Problem, Type)
from utilities import (AND_CONDITION, CONDITIONAL_EFFECT, EQUALS_CONDITION,
                       EXISTS_CONDITION, FORALL_CONDITION, IMPLY_CONDITION,
                       INCREASE_CONDITION, NOT_CONDITION, NOT_EQUALS_CONDITION,
                       OR_CONDITION, CodeException, parsing_error_code,
                       valid_requirements)


class ParsingException(CodeException):
    """ An exception to be raised in the even that something goes wrong with
        the parser process. """

class Parser:
    """ Used to parse PDDL domains and problems. """

    def __init__(self, domain_file_name, problem_file_name):
        """ Set parser parameters

            (Parser, str, str, str) -> None
        """
        self.domain_file_name = domain_file_name
        self.problem_file_name = problem_file_name
        if not self.problem_file_name:
            self.problem_file_name = self.domain_file_name
        self.problem = None

    def parse_domain(self):
        """Parse the domain file and create a problem instance. In case of an
           error, raise a ParsingException with the appropriate code from above.

           (Parser) -> Problem
        """
        #Parse the domain file
        try:
            with open(self.domain_file_name) as domain_file:
                domain_lines = domain_file.readlines()
        except IOError:
            raise ParsingException("Error: could not open the doman file: " +\
                self.domain_file_name, parsing_error_code)

        #Strip comments and turn into a single string
        domain_str = ''
        for line in domain_lines:
            line = line.strip().lower()
            if line:
                try:
                    c_index = line.index(";")
                    line = line[:c_index]
                except ValueError: pass
            if not line: continue
            domain_str += line + " "

        domain_list = OneOrMore(nestedExpr()).parseString(domain_str).asList()
        if not domain_list:
            raise ParsingException("Error: empty domain file: " +\
                 self.domain_file_name, parsing_error_code)

        domain_list = domain_list[0]
        if domain_list[0] != "define":
            raise ParsingException("Error: define expected at beginning of file",
                parsing_error_code)
        for line in domain_list[1:]:
            #print "LINE:", line

            if line[0] == "domain":
                try:
                    self.problem = Problem(line[1])
                except IndexError:
                    raise ParsingException("Error: badly formed domain name",
                        parsing_error_code)
            elif line[0] == ":requirements":
                self.parse_requirements(line[1:])

            elif line[0] == ":types":
                self.parse_types(line[1:])

            elif line[0] == ":constants":
                self.parse_constants(line[1:])

            elif line[0] == ":predicates":
                self.parse_predicates(line[1:])

            elif line[0] == ":functions":
                self.parse_functions(line[1:])

            elif line[0] == ":action":
                self.parse_action(line[1:])

            elif line[0] == ":derived":
                self.parse_derived(line[1:])


    def parse_problem(self):
        """Parse the problem file and add the details to self.problem.
           In case of an error, raise a ParsingException with the appropriate
           code from above.

           (Parser) -> None
        """
        if not self.problem:
            raise ParsingException("Error: must parse the domain file first.",
                parsing_error_code)

        #Parse the problem file
        try:
            with open(self.problem_file_name) as problem_file:
                problem_lines = problem_file.readlines()
        except IOError:
            raise ParsingException("Error: could not open the problem file: " +\
                self.problem_file_name, parsing_error_code)

        #Strip comments and turn into a single string
        problem_str = ''
        for line in problem_lines:
            line = line.strip().lower()
            if line:
                try:
                    c_index = line.index(";")
                    line = line[:c_index]
                except ValueError: pass
            if not line: continue
            problem_str += line + " "

        problem_list = OneOrMore(nestedExpr()).parseString(problem_str).asList()
        if not problem_list:
            raise ParsingException("Error: empty problem file: " +\
                 self.problem_file_name, parsing_error_code)

        problem_list = problem_list[0]
        if problem_list[0] != "define":
            raise ParsingException("Error: define expected at beginning of file",
                parsing_error_code)
        for line in problem_list[1:]:

            if line[0] == "problem":
                try:
                    self.problem.problem_name = line[1]
                except IndexError:
                    raise ParsingException("Error: badly formed problem name",
                        parsing_error_code)

            elif line[0] == ":domain":
                try:
                    if self.problem.name != line[1]:
                        raise ParsingException("Error: problem not for domain",
                            parsing_error_code)
                except IndexError:
                    raise ParsingException("Error: badly formed problem domain line",
                        parsing_error_code)

            elif line[0] == ":objects":
                self.parse_objects(line[1:])

            elif line[0] == ":init":
                self.parse_init(line[1:])

            elif line[0] == ":goal":
                self.parse_goal(line[1:])

            elif line[0] == ":metric":
                self.parse_metric(line[1:])

            else:
                print("Unknown line:", line)


    def parse_requirements(self, requirements):
        """ parse the requiremenets strings. If we have something other
            than typing, action-costs, or adl, complain.

            (Parser, [str]) -> None
        """
        if not self.problem:
            raise ParsingException("Error: must parse domain first.", parsing_error_code)
        for requirement in requirements:
            if requirement not in valid_requirements:
                raise ParsingException("Error: unsupported requirement: " + requirement,
                    parsing_error_code)
            self.problem.requirements.append(requirement)


    def parse_types(self, types):
        """ Parse the types strings. We assume that the type graph is acyclic.

            (Parser, [str]) -> None
        """
        if not self.problem:
            raise ParsingException("Error: must parse domain first.", parsing_error_code)

        current_types = []
        tokens = iter(types)
        for token in tokens:
            if token == "-":
                try:
                    token = next(tokens)
                    if token not in self.problem.types:
                        #Until we know better, we make the default_type its parent
                        self.problem.types[token] = Type(token, self.problem.default_type)
                    for type_name in current_types:
                        if type_name in self.problem.types:
                            raise ParsingException("Error: type " + type_name +\
                                " has multiple parents.", parsing_error_code)
                        self.problem.types[type_name] = Type(type_name, self.problem.types[token])
                    current_types = []
                except StopIteration:
                    raise ParsingException("Error: badly formed types.",
                        parsing_error_code)
            else:
                current_types.append(token)
        for type_name in current_types:
            if type_name in self.problem.types:
                raise ParsingException("Error: type " + type_name +\
                    " has multiple parents.", parsing_error_code)
            self.problem.types[type_name] = Type(type_name, self.problem.default_type)

    def parse_constants(self, constants):
        """ Parse the constants into the constants dictionary

            (Parser, [str]) -> None
        """
        current_constants = []
        tokens = iter(constants)
        for token in tokens:
            if token == "-":
                try:
                    type_name = next(tokens)
                    if type_name not in self.problem.types:
                         raise ParsingException("Error: type " + type_name +\
                                " for constants.", parsing_error_code)
                    for constant_name in current_constants:
                        self.problem.objects[constant_name] =\
                            Object(constant_name, self.problem.types[type_name], True)
                    current_constants = []
                except StopIteration:
                    raise ParsingException("Error: badly formed constants.",
                        parsing_error_code)
            else:
                current_constants.append(token)

        for constant_name in current_constants:
            self.problem.objects[constant_name] = \
                Object(constant_name, self.problem.default_type, True)


    def parse_predicates(self, definition):
        """ Parse the definition list into the predicates dict.

            (Parser, [str]) -> None
        """
        for pred in definition:
            name = pred[0]
            if name in self.problem.predicates:
                raise ParsingException("Error: duplicate predicate " + name,
                    parsing_error_code)

            variables = []
            types = []

            current_args = []
            tokens = iter(pred[1:])
            for token in tokens:
                if token == "-":
                    try:
                        token = next(tokens)
                        if token not in self.problem.types:
                            raise ParsingException("Error: unknown type: " + token +\
                                " in predicate " + name, parsing_error_code)
                        for arg in current_args:
                            variables.append(arg)
                            types.append(self.problem.types[token])
                        current_args = []
                    except StopIteration:
                        raise ParsingException("Error: badly formed predicate " + name,
                            parsing_error_code)
                else:
                    if token[0] != "?":
                        raise ParsingException("Error: constant " + token +\
                            " in predicate " + name, parsing_error_code)
                    current_args.append(token)
            for arg in current_args:
                variables.append(arg)
                types.append(self.problem.default_type)

            self.problem.predicates[name] = Predicate(name, variables, types)



    def parse_functions(self, functions):
        """ Parse a the list of functions and store in the function dict.

            (Parser, [str]) -> None
        """

        tokens = iter(functions)
        for function in tokens:
            try:
                token = next(tokens)
                if token != '-':
                    raise ParsingException("Error: badly formed function: " + function,
                        parsing_error_code)
                token = next(tokens)
                if token != 'number':
                    raise ParsingException("Error: we only support numeric functions: " + function,
                        parsing_error_code)

                name = function[0]
                if name in self.problem.functions:
                    raise ParsingException("Error: duplicate function " + name,
                        parsing_error_code)

                variables = []
                types = []
                current_args = []
                ftokens = iter(function[1:])
                for token in ftokens:
                    if token == "-":
                        try:
                            token = next(ftokens)
                            if token not in self.problem.types:
                                raise ParsingException("Error: unknown type: " + token +\
                                    " in function " + name, parsing_error_code)
                            for arg in current_args:
                                variables.append(arg)
                                types.append(self.problem.types[token])
                            current_args = []
                        except StopIteration:
                            raise ParsingException("Error: badly formed function " + name,
                                parsing_error_code)
                    else:
                        if token[0] != "?":
                            raise ParsingException("Error: constant " + token +\
                                " in function " + name, parsing_error_code)
                        current_args.append(token)
                for arg in current_args:
                    variables.append(arg)
                    types.append(self.problem.default_type)

                self.problem.functions[name] = Function(name, variables, types)
            except StopIteration:
                raise ParsingException("Error: badly formed function: " + function,
                    parsing_error_code)

    def parse_condition(self, definition, scope, context, check_consts):
        """ Parse the definition list into a Condition. The scope contains the
            variables that are currently in scope. Context tells us if we are
            parsing conditions for a preconditon (pre), effect (eff), or
            anything (any)

            (Parser, [str, [str, ...] ], [str], str, bool) -> Condition
        """
        cond_type = definition[0]
        if cond_type == NOT_CONDITION:
            if len(definition) != 2:
                raise ParsingException("Badly formed not condition",
                    parsing_error_code)
            condition = definition[1]
            return NotCondition(self.parse_condition(condition, scope, context, check_consts))

        elif cond_type == AND_CONDITION:
            conditions = definition[1:]
            if len(conditions) < 1:
                raise ParsingException("Empty and condition",
                    parsing_error_code)
            return AndCondition([self.parse_condition(x, scope, context, check_consts) for x in conditions])

        elif cond_type == OR_CONDITION:
            if context != "pre":
                raise ParsingException("or condition not allowed in effect",
                    parsing_error_code)

            conditions = definition[1:]
            if len(conditions) < 1:
                raise ParsingException("Empty or condition",
                    parsing_error_code)
            return OrCondition([self.parse_condition(x, scope, context, check_consts) for x in conditions])

        elif cond_type == IMPLY_CONDITION:
            if context != "pre":
                raise ParsingException("imply condition not allowed in effect",
                    parsing_error_code)

            conditions = definition[1:]
            if len(conditions) != 2:
                raise ParsingException("Badly formed imply condition",
                    parsing_error_code)

            #Convert to a disjunction
            return OrCondition(\
                [NotCondition(self.parse_condition(conditions[0], scope, context, check_consts)),
                self.parse_condition(conditions[1], scope, context, check_consts)])

        elif cond_type == FORALL_CONDITION:
            conditions = definition[1:]
            if len(conditions) != 2:
                raise ParsingException("Badly formed forall condition",
                    parsing_error_code)
            quant_var = conditions[0]
            if len(quant_var) == 3:
                if quant_var[1] != '-':
                    raise ParsingException("Badly formed forall condition var",
                        parsing_error_code)
                if quant_var[2] not in self.problem.types:
                    raise ParsingException("Unknown type: " + quant_var[2],
                        parsing_error_code)
                scope = list(scope)
                scope.append(quant_var[0])
                return ForAllCondition(quant_var[0], self.problem.types[quant_var[2]],
                    self.parse_condition(conditions[1], scope, context, check_consts))
            elif len(quant_var) == 1:
                scope = list(scope)
                scope.append(quant_var[0])
                return ForAllCondition(quant_var[0], None,
                    self.parse_condition(conditions[1], scope, context, check_consts))
            raise ParsingException("Badly formed forall condition var",
                    parsing_error_code)

        elif cond_type == EXISTS_CONDITION:
            if context != "pre":
                raise ParsingException("exists condition not allowed in effect",
                    parsing_error_code)

            conditions = definition[1:]
            if len(conditions) != 2:
                raise ParsingException("Badly formed exists condition",
                    parsing_error_code)
            quant_var = conditions[0]
            if len(quant_var) == 3:
                if quant_var[1] != '-':
                    raise ParsingException("Badly formed exists condition var",
                        parsing_error_code)
                if quant_var[2] not in self.problem.types:
                    raise ParsingException("Unknown type: " + quant_var[2],
                        parsing_error_code)
                scope = list(scope)
                scope.append(quant_var[0])
                return ExistsCondition(quant_var[0], self.problem.types[quant_var[2]],
                    self.parse_condition(conditions[1], scope, context, check_consts))
            elif len(quant_var) == 1:
                scope = list(scope)
                scope.append(quant_var[0])
                return ExistsCondition(quant_var[0], None,
                    self.parse_condition(conditions[1], scope, context, check_consts))
            raise ParsingException("Badly formed exists condition var",
                        parsing_error_code)

        elif cond_type == INCREASE_CONDITION:
            if context == "pre":
                raise ParsingException("increase condition only allowed in effect",
                    parsing_error_code)

            conditions = definition[1:]
            if len(conditions) != 2:
                raise ParsingException("Badly formed increase condition",
                    parsing_error_code)
            var, value = conditions
            if not var or not isinstance(var, list):
                raise ParsingException("Badly formed increase condition",
                    parsing_error_code)
            var = var[0]
            if var not in self.problem.functions:
                raise ParsingException("Unknown function: " + var,
                    parsing_error_code)
            if var != "total-cost":
                raise ParsingException("We do not support metric planning." +
                    " Can only increase total-cost.", parsing_error_code)

            var = self.problem.functions[var]

            if not value:
                raise ParsingException("Badly formed increase condition",
                    parsing_error_code)
            value_args = []

            if isinstance(value, list):
                value_args = value[1:]
                value = value[0]
                for arg in value_args:
                    if arg[0] == '?' and arg not in scope:
                        raise ParsingException("Variable out of scope: " + arg,
                            parsing_error_code)
                    elif arg[0] != '?' and check_consts:
                        if arg not in self.problem.objects:
                            raise ParsingException("Unknown constant: " + arg, parsing_error_code)
                        if not self.problem.objects[arg].constant:
                            raise ParsingException(arg + " is an object not a constant.", parsing_error_code)
            try:
                value = int(value)
            except ValueError:
                if value not in self.problem.functions:
                    raise ParsingException("Unknown function: " + value,
                        parsing_error_code)
                value = self.problem.functions[value]
            return IncreaseCondition(var, value, value_args)

        elif cond_type == EQUALS_CONDITION:
            if context != "pre":
                raise ParsingException("Equality only allowed in preconditions",
                    parsing_error_code)
            conditions = definition[1:]
            if len(conditions) != 2:
                raise ParsingException("Badly formed equality condition",
                    parsing_error_code)
            var1, var2 = conditions
            if var1[0] != '?':
                if check_consts:
                    if var1 not in self.problem.objects:
                        raise ParsingException("Unknown constant: " + var1, parsing_error_code)
                    if not self.problem.objects[var1].constant:
                        raise ParsingException(var1 + " is an object not a constant.", parsing_error_code)

            elif var1 not in scope:
                raise ParsingException("Variable out of scope: " + var1, parsing_error_code)
            if var2[0] != '?':
                if check_consts:
                    if var2 not in self.problem.objects:
                        raise ParsingException("Unknown constant: " + var2, parsing_error_code)
                    if not self.problem.objects[var2].constant:
                        raise ParsingException(var2 + " is an object not a constant.", parsing_error_code)
            elif var2 not in scope:
                raise ParsingException("Variable out of scope: " + var2,
                    parsing_error_code)

            return EqualsCondition([var1, var2])

        elif cond_type == NOT_EQUALS_CONDITION:
            if context != "pre":
                raise ParsingException("Inequality only allowed in preconditions",
                    parsing_error_code)
            conditions = definition[1:]
            if len(conditions) != 2:
                raise ParsingException("Badly formed inequality condition",
                    parsing_error_code)
            var1, var2 = conditions
            if var1[0] != '?':
                if check_consts:
                    if var1 not in self.problem.objects:
                        raise ParsingException("Unknown constant: " + var1, parsing_error_code)
                    if not self.problem.objects[var1].constant:
                        raise ParsingException(var1 + " is an object not a constant.", parsing_error_code)
            elif var1 not in scope:
                raise ParsingException("Variable out of scope: " + var1,
                    parsing_error_code)
            if var2[0] != '?':
                if check_consts:
                    if var2 not in self.problem.objects:
                        raise ParsingException("Unknown constant: " + var2, parsing_error_code)
                    if not self.problem.objects[var2].constant:
                        raise ParsingException(var2 + " is an object not a constant.", parsing_error_code)
            elif var2 not in scope:
                raise ParsingException("Variable out of scope: " + var2,
                    parsing_error_code)

            return NotCondition(EqualsCondition([var1, var2]))

        elif cond_type == CONDITIONAL_EFFECT:
            if context != "eff":
                raise ParsingException("conditional effects only allowed in action effects",
                    parsing_error_code)
            conditions = definition[1:]
            if len(conditions) != 2:
                raise ParsingException("Badly formed conditional effect",
                    parsing_error_code)
            return ConditionalEffect(self.parse_condition(conditions[0], scope,
                "pre", check_consts),self.parse_condition(conditions[1],
                scope, "sim", check_consts))

        elif cond_type in self.problem.predicates:
            conditions = definition[1:]
            n_conditions = []
            for cond in conditions:
                if cond[0] != '?':
                    if check_consts:
                        if cond not in self.problem.objects:
                            raise ParsingException("Unknown constant: " + cond,
                                parsing_error_code)
                        if not self.problem.objects[cond].constant:
                            raise ParsingException(cond + " is an object not a constant.",
                                parsing_error_code)
                elif cond not in scope:
                    raise ParsingException("Variable out of scope: " + cond,
                        parsing_error_code)
                n_conditions.append(cond)
            return PredicateCondition(self.problem.predicates[cond_type], n_conditions)

        else:
            raise ParsingException("Invalid condition " + cond_type +\
                " " + str(definition[1:]), parsing_error_code)


    def parse_action(self, definition):
        """ Parse the action described by definition and store in the action
            dict.

            (Parser, [str]) -> None
        """
        name = definition[0]
        if name in self.problem.actions:
            raise ParsingException("Error: duplicate action " + name, parsing_error_code)

        try:
            params = definition[definition.index(":parameters")+1]
        except ValueError as IndexError:
            params = []
        try:
            precondition = definition[definition.index(":precondition")+1]
        except ValueError as IndexError:
            raise ParsingException("Error: action " + name + " has no precondition",
                    parsing_error_code)
        try:
            effect = definition[definition.index(":effect")+1]
        except ValueError as IndexError:
            raise ParsingException("Error: action " + name + " has no effect",
                    parsing_error_code)

        variables = []
        types = []
        current_args = []
        tokens = iter(params)
        for token in tokens:
            if token == "-":
                try:
                    token = next(tokens)
                    if token not in self.problem.types:
                        raise ParsingException("Error: unknown type: " + token +\
                            " in action " + name, parsing_error_code)
                    for arg in current_args:
                        variables.append(arg)
                        types.append(self.problem.types[token])
                    current_args = []
                except StopIteration:
                    raise ParsingException("Error: badly formed action parameters "\
                        + name, parsing_error_code)
            else:
                if token[0] != "?":
                    raise ParsingException("Error: constant " + token +\
                        " in action parameters" + name, parsing_error_code)
                current_args.append(token)
        for arg in current_args:
            variables.append(arg)
            types.append(self.problem.default_type)

        try:
            scope = list(variables)
            precondition = self.parse_condition(precondition, scope, 'pre', True)
            if not isinstance(precondition, AndCondition):
                precondition = AndCondition([precondition])
        except ParsingException as e:
            raise ParsingException("Error parsing precondition of action: " + name +\
                "\n" + e.message, parsing_error_code)

        try:
            scope = list(variables)
            effect = self.parse_condition(effect, scope, 'eff', True)
            if not isinstance(effect, AndCondition):
                raise ParsingException("Expected conjunctive effect",
                    parsing_error_code)
        except ParsingException as e:
            raise ParsingException("Error parsing effects of action: " + name +\
                "\n" + e.message, parsing_error_code)

        self.problem.actions[name] = Action(name, variables, types, precondition, effect, False)


    def parse_derived(self, definition):
        """ Parse the derived predicate described by definition and store in the
            derived dict.

            (Parser, [str]) -> None
        """

        if len(definition) != 2:
            raise ParsingException("Error: ill-formed derived predicate",
                parsing_error_code)

        predicate = definition[0]
        name = predicate[0]
        condition = definition[1]

        variables = []
        types = []
        current_args = []

        tokens = iter(predicate[1:])
        for token in tokens:
            if token == "-":
                try:
                    token = next(tokens)
                    if token not in self.problem.types:
                        raise ParsingException("Error: unknown type: " + token +\
                            " in derived predicate " + name, parsing_error_code)
                    for arg in current_args:
                        variables.append(arg)
                        types.append(self.problem.types[token])
                    current_args = []
                except StopIteration:
                    raise ParsingException("Error: badly formed derived predicate parameters: " +
                        name, parsing_error_code)
            else:
                if token[0] != "?":
                    raise ParsingException("Error: constant " + token +\
                        " in derived predicate parameters: " + name, parsing_error_code)
                current_args.append(token)
        for arg in current_args:
            variables.append(arg)
            types.append(self.problem.default_type)

        predicate = self.problem.predicates[name]
        for tid, ttype in enumerate(types):
            if ttype != predicate.types[tid]:
                raise ParsingException("Error: derived predicate type mismatch: " +\
                    name, parsing_error_code)
        pred_cond = PredicateCondition(self.problem.predicates[name], variables)
        try:
            scope = list(variables)
            condition = self.parse_condition(condition, scope, 'pre', True)
        except ParsingException as e:
            raise ParsingException("Error parsing effects of derived predicate: " + name +\
                "\n" + e.message, parsing_error_code)

        if pred_cond.pred not in self.problem.derived_predicates:
            self.problem.derived_predicates[pred_cond.pred] = []
        self.problem.derived_predicates[pred_cond.pred].append(Action(\
            pred_cond.pred.name, pred_cond.variables, pred_cond.pred.types,
            condition, pred_cond, True))

    def parse_objects(self, objects):
        """ Parse the object strings into typed objects.

            (Parser, [str]) -> None
        """
        current_objects = []
        tokens = iter(objects)
        for token in tokens:
            if token == "-":
                try:
                    token = next(tokens)
                    if token not in self.problem.types:
                        raise ParsingException("Error: unknown object type " + token,
                            parsing_error_code)
                    for obj_str in current_objects:
                        obj = Object(obj_str, self.problem.types[token], False)
                        self.problem.objects[obj.name] = obj
                    current_objects = []
                except StopIteration:
                    raise ParsingException("Error: badly formed object description.",
                        parsing_error_code)
            else:
                current_objects.append(token)
        for obj_str in current_objects:
            obj = Object(obj_str, self.problem.default_type, False)
            self.problem.objects[obj.name] = obj

        for obj in list(self.problem.objects.values()):
            obj.otype.add_object(obj)


    def parse_init(self, init):
        """ Parse the init strings into the initial state.

            (Parser, [str]) -> None
        """
        for init_fact in init:
            if init_fact[0] == '=':
                init_fact = init_fact[1:]
                try:
                    function, function_value = init_fact
                    function_name = function[0]
                    function_args = function[1:]
                    if function_name not in self.problem.functions:
                        raise ParsingException("Error: unknown function name in"\
                        + " initial state: " + function_name, parsing_error_code)
                    function = self.problem.functions[function_name]
                    function.values[tuple(function_args)] = int(function_value)
                except IndexError:
                    raise ParsingException("Error: badly formed function value"\
                        + " assignment in initial state", parsing_error_code)
                except ValueError:
                    raise ParsingException("Error: invalid function value in"\
                        + " initial state: " + init_fact[1], parsing_error_code)
            else:
                try:
                    fact_name = init_fact[0]
                    fact_args = init_fact[1:]
                    if fact_name not in self.problem.predicates:
                        raise ParsingException("Error: unknown fact name in"\
                        + " initial state: " + fact_name, parsing_error_code)
                    for arg in fact_args:
                        if arg not in self.problem.objects:
                             raise ParsingException("Error: unknown object in initial state: ",
                                 parsing_error_code)
                    self.problem.initial_state.append((self.problem.predicates[fact_name],
                        tuple(fact_args)))
                except IndexError:
                    raise ParsingException("Error: badly formed start state fact",
                        parsing_error_code)
        self.problem.initial_state_set = set(self.problem.initial_state)

    def parse_goal(self, goal):
        """ Parse the goal strings into the goal.

            (Parser, [str]) -> None
        """
        try:
            self.problem.goal = self.parse_condition(goal[0], [], 'pre', False)
        except ParsingException as e:
            raise ParsingException("Error: badly formed goal.\n" + e.message,
                parsing_error_code)


    def parse_metric(self, metric):
        """ Parse the metric strings into the problem metric.

            (Parser, [str]) -> None
        """
        try:
            if metric[0] not in ["minimize", "minimise"]:
                raise ParsingException("Error: we only support minimi(s/z)ing metrics",
                    parsing_error_code)
            if metric[1][0] != "total-cost":
                raise ParsingException("Error: we only support minimi(s/z)ing total-cost"\
                    + " not: " + str(metric[1][0]),
                    parsing_error_code)
        except IndexError:
            raise ParsingException("Error: badly formed metric.\n" +\
                    "We only support minimi(s/z)ing total-cost", parsing_error_code)
