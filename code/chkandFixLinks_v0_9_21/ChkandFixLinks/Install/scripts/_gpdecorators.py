"""
---------------------------------------------------------------------------
 _gpdecorators.py ---- tool:  A decorator to wrap error handling.
 Created: 2011; modified May 12 2015
 args:  none
------------------------------------------------------------------------------
 Author: Rebecca Strauch - ADFG-DWC-GIS
 Purpose: Helps to simplify the handling and display of errors by
   wrapping in a   "main"   function

   Call with:  
     from _gpdecorators import *  

   To use in a .py file, for example:
   
# Import modules
import arcpy
import os
from _miscUtils import *
from _gpdecorators import *

# catch_errors decorator must preceed a function using the @ notation.
@catch_errors
def main():
    
    # Add your program here
    #
    #
    #  end with...
    
    myMsgs('!!! Success !!!  ')

# End main function

if __name__ == '__main__':
    main()

---------------------------------------------------------------------------
"""
import sys as _sys
import traceback as _traceback
import arcpy

def catch_errors(func):
    """
    Decorator function to support error handling
    """
    def decorator(*args, **kwargs):
        """
        Decorator function
        """
        try:
            f = func(*args, **kwargs)
            return f
        except Exception:
            tb = _sys.exc_info()[2]
            tbInfo = _traceback.format_tb(tb)[-1]
            arcpy.AddError('PYTHON ERRORS:\n%s\n%s: %s\n' %
                             (tbInfo, _sys.exc_type, _sys.exc_value))
            print('PYTHON ERRORS:\n%s\n%s: %s\n' %
                             (tbInfo, _sys.exc_type, _sys.exc_value))
            gp_errors = arcpy.GetMessages(2)
            if gp_errors:
                arcpy.AddError('GP ERRORS:\n%s\n' % gp_errors)
                print('GP ERRORS:\n%s\n' % gp_errors)
    # End decorator function
    return decorator
# End catch_errors function

if __name__ == '__main__':
    pass
