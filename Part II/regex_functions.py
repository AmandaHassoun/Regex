"""
# Copyright 2013 Nick Cheng, Brian Harrington, Danny Heap, 2013, 2014
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regex_tree import RegexTree, Leaf, StarTree, DotTree, BarTree

# Do not change any of the class declarations above this comment
# Student code below this comment.


def is_regex(s: str) -> bool:
    """Return True iff s is a valid Regex, else return False.

    >>> is_regex('(1.((1.2).(1|2)))')
    True
    >>> is_regex('(1.2)')
    True
    >>> is_regex('2*****')
    True
    >>> is_regex('(1.)')
    False
    """
    if len(s) == 1 and (s in ['0', '1', '2', 'e']):
        return True
    elif s == '':
        return True
    elif len(s) == 2 and s[1] == '*' and is_regex(s[0]):
        return True
    elif (len(s) == 5 and s[0] == '(' and s[4] == ')' and (s[2] == '|' or '.')
          and is_regex(s[1]) and is_regex(s[3]) and s[2] != '*'):
        return True
    elif s[0] in '120e' and (s[1:] == '*' * len(s[1:])):
        return True
    elif len(s) > 5:
        if s[-1] != '*':
            for i in range(len(s)):
                if (s.startswith('(')) and s[-1] == ')' and\
                   (s[i] == '.' or s[i] == '|') and ((s[i + 1] and
                                                      s[i - 1]) in '012e*()'):
                    n = s[1:i].count('(')
                    m = s[1:i].count(')')
                    if n == m:
                        return (is_regex(s[1:i]) and is_regex(s[i + 1:-1]))
        else:
            if s.startswith('('):
                return is_regex(s[:-1])
            else:
                if (s[0] in '012e') and (s[1:] == '*' * len(s[1:])):
                    return True

    return False

#helper function from week 4 slides
#Link http://www.cdf.toronto.edu/~heap/148/W14/Lectures/danny/W4/perm.py


def perm(s: str) -> {str, ...}:
    """Return set of all permutations of s.
    
    >>> perm("a") == {"a"}
    True
    >>> perm("ab") == {"ab", "ba"}
    True
    >>> perm("abc") == {"abc", "acb", "bac", "bca", "cab", "cba"}
    True
    """
    return (set(sum([[s[i] + p for p in perm(s[:i] + s[i + 1:])]
                     for i in range(len(s))], [])) if len(s) > 1 else {s})


def all_regex_permutations(s: str) -> bool:
    """Takes s and produces the set of permutations of s that are
    valid Regexes.

    >>> all_regex_permutations('1*') == {'1*'}
    True
    >>> all_regex_permutations('(1|2)') == {'(1|2)', '(2|1)'}
    True
    >>> all_regex_permutations('((1.2*).2)') == {'((1.2)*.2)', '(1*.(2.2))',\
    '(2.(2.1))*', '((1.2).2*)', '(2.(1.2))*', '(2*.(2.1))', '(2*.(1.2))', \
    '((2.1*).2)', '((2.2).1)*', '(1.(2.2)*)', '((2.1)*.2)', '((1.2*).2)', \
    '((2*.1).2)', '(2.(1*.2))', '(2.(2.1*))', '((1.2).2)*', '((2.1).2*)', \
    '(2.(1.2*))', '((2*.2).1)', '(2.(2.1)*)', '((2.2*).1)', '(2.(2*.1))', \
    '(1.(2.2*))', '(2.(1.2)*)', '((2.2).1*)', '(1.(2.2))*', '((2.2)*.1)', \
    '((2.1).2)*', '(1.(2*.2))', '((1*.2).2)'}
    True
    >>> all_regex_permutations('((1.2).1)') == {'((1.1).2)', '(1.(2.1))', \
    '(2.(1.1))', '(1.(1.2))', '((2.1).1)', '((1.2).1)'}
    True
    """
    
    set_regex = perm(s)
    new_set = set()
    for perms in set_regex:
        if is_regex(perms):
            new_set.add(perms)

    return new_set
  

def regex_match(r: 'RegexTree', s: str) -> bool:
    """Return True iff s matches the Regex tree rooted at r.

    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '111110')
    True
    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '1')
    False
    >>> regex_match(StarTree(BarTree(Leaf('1'), Leaf('2'))), '111111')
    True
    >>> regex_match(StarTree(DotTree(Leaf('0'), Leaf('2'))), '0202')
    True
    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('e')), '1111')
    True 
    """
    if isinstance(r, Leaf):
        if r.symbol == 'e':
            return s == '' or (s == len(s) * '1' or s == len(s) * '2' or
                               s == len(s) * '0')
        else:
            return s == r.symbol
        
    elif isinstance(r, StarTree):
        if isinstance(r.children[0], Leaf):
            if r.children[0].symbol == 'e' and (s == len(s) * '1'
                                                or s == len(s) * '2' or
                                                s == len(s) * '0'):
                return True
            elif s == '':
                return True
            else:
                for i in range(len(s)):
                    if s[i] != r.children[0].symbol:
                        return False
                return True
            
        else:
            for i in range(len(s)):
                if regex_match(r.children[0], s[:i]):
                    L = []
                    if i == 0:
                        for char in s:
                            L.append(regex_match(r.children[0], char))
                    else:
                        for n in range(len(s) // i):
                            L.append(regex_match(r.children[0],
                                                 s[n * i: (n + 1) * i]))
            return not False in L
    elif isinstance(r, DotTree):
        for i in range(len(s)):
            if (regex_match(r.children[0], s[: i]) and
                    regex_match(r.children[1], s[i:])):
                return True
        return False
    elif isinstance(r, BarTree):
        return regex_match(r.children[0], s) or regex_match(r.children[1], s)


def build_regex_tree(regex: str) -> 'RegexTree':
    """Takes a valid regular expression regex, builds the corresponding regular
    expression tree, and returns its root.

    >>> build_regex_tree('((1.(0|1)*).0)')
    DotTree(DotTree(Leaf('1'), StarTree(BarTree(Leaf('0'), Leaf('1')))), \
    Leaf('0'))
    >>> build_regex_tree('((0.1).0)')
    DotTree(DotTree(Leaf('0'), Leaf('1')), Leaf('0'))
    >>> build_regex_tree('2******')
    StarTree(StarTree(StarTree(StarTree(StarTree(StarTree(Leaf('2')))))))
    >>> build_regex_tree('(2**.((1.2)**|(0.1*)))')
    DotTree(StarTree(StarTree(Leaf('2'))), BarTree(StarTree(StarTree(
    DotTree(Leaf('1'), Leaf('2')))), DotTree(Leaf('0'), StarTree(Leaf('1')))))
    """

    if len(regex) == 1:
        return Leaf(regex)
    elif len(regex) == 2:
        return StarTree(build_regex_tree(regex[0]))
    elif '*' in regex and '|' not in regex and '.' not in regex:
        return StarTree(build_regex_tree(regex[:-1]))
    elif len(regex) == 5:
        if regex[2] == '|':
            return BarTree(build_regex_tree(regex[1]),
                           build_regex_tree(regex[3]))
        else:
            return DotTree(build_regex_tree(regex[1]),
                           build_regex_tree(regex[3]))
    elif len(regex) > 5:
        if regex[-1] != '*':
            for i in range(len(regex)):
                if regex[i] == '.' or regex[i] == '|':
                    n = regex[1:i].count('(')
                    m = regex[1:i].count(')')
                    head = regex[i]
                    if n == m:
                        if head == '|':
                            return BarTree(build_regex_tree(regex[1:i]),
                                           build_regex_tree(regex[i + 1:-1]))
                        else:
                            return DotTree(build_regex_tree(regex[1:i]),
                                           build_regex_tree(regex[i + 1:-1]))              
        else:
            if regex[-2] != '*':
                for i in range(len(regex[:-1])):
                    if regex[i] == '.' or regex[i] == '|':
                        n = regex[1:i].count('(')
                        m = regex[1:i].count(')')
                        if n == m:
                            head2 = regex[i]
                            if head2 == '|':
                                return StarTree(BarTree(build_regex_tree(
                                    regex[1:i]), build_regex_tree(
                                        regex[i + 1:-2])))
                            else:
                                return StarTree(DotTree(build_regex_tree(
                                    regex[1:i]), build_regex_tree(
                                        regex[i + 1:-2])))
            else:
                return StarTree(build_regex_tree(regex[:-1]))

