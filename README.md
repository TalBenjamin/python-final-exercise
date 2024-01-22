# python-final-exercise
Python final exercise - complicated calculator

This is a pretty complex calculator with the following operators:
# Operator      Description      Precedence
    +           addition          1
    -           subtraction       1
    /           division          2  
    *           multiplication    2  
    ^           power             3  
    %           modulu            4  
    @           average           5  
    &           minimum           5
    $           maximum           5
    ! (unary)   factorial         6
    # (unary)   digit sum         6
    ~ (unary)   negative          6

# The calculator follows this logic:
  go over elements of expression
  - if operand, push to operand stack
  - if ( push to operators stack
  - if ) do all operations in operator stack until you reach (
  - if operator, do all operations in operator stack that are stronger or equal to current operator, add results to operand stack and current operator to operator stack
 
  As long as there are operators in stack, perform all remaining operations.

# Some things to note 
  - the calculator completely disregards whitespaces
  - automatically interprets decimal point: so .9 is 0.9, 8. is 8.0, and . is 0.0
  - tilda ~ can't be applied to the same operand more than once.
  - a minus - that comes after any operator other than unary minus is interpreted as "part of the number", meaning the sign of the number. 
  
