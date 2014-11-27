class IllegalValueError(Exception):
    pass


class Regex:
    """A tree representation of a regex expression."""

    def __init__(self: 'Regex', child1: str=None,
                 child2: str=None):
        """Initilizes a Regex.
        """       
        self.child1 = child1
        self.child2 = child2

    def __repr__(self: 'Regex') -> str:
        """Return representation of a Regex tree as a string.
        """
        if not self.child1:
            return self.classname + '(' + repr(self.value) + ')'
        elif not self.child2:
            return (self.classname + '(' + repr(self.value) + ',' +
                    repr(self.child1) + ')')               
        else:
            return (self.classname + '(' + repr(self.value) + ',' +
                    repr([self.child1, self.child2]) + ')')
    
    def __eq__(self: 'Regex', other: 'Regex') -> bool:
        """Return True iff other matches Regex.
        """
        if isinstance(other, Regex) and self.value == other.value:
            if not self.child1:
                return True
            elif not self.child2:
                return self.child1 == other.child1
            else:
                return ((self.child1 == other.child1) and
                        (self.child2 == other.child2))                                             

        return False


class Leaf(Regex):
    """A Tree of one string value."""

    def __init__(self, value: str=None) -> None:
        """Initializes a Leaf.
        """
        super().__init__()
        self.classname = 'Leaf'
        
        if 'e' == value:
            self.value = ''
        elif value in ['0', '1', '2']:
            self.value = value
        else:
            raise IllegalValueError('Invalid Value')
                                            
                                                    
class RegexStar(Regex):
    """A Regex Tree of one value with one child."""
    
    def __init__(self, child: str=None) -> None:
        """Initilizes a RegexStar.
        """
        super().__init__(child)
        self.value = '*'
        self.classname = 'RegexStar'


class RegexBar(Regex):
    """A Regex tree of one value with two children."""

    def __init__(self, child1: str=None, child2: str=None) -> None:
        """Initilizes a RegexBar.
        """
        super().__init__(child1, child2)
        self.value = '|'
        self.classname = 'RegexBar'


class RegexDot(Regex):
    """A Regex tree of one value with two children."""
    
    def __init__(self, child1: str=None, child2: str=None) -> None:
        """Initilizes a RegexDot.
        """
        super().__init__(child1, child2)
        self.value = '.'
        self.classname = 'RegexDot'
