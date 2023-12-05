scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# package attributes used in `test` must 
#  go above the `test` import
from .gamesheet import test

__ALL__ = ['test']