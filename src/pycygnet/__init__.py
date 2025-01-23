import win32com
from pycygnet.com import PythonExecutor
from pycygnet.site import Site
from pycygnet.test_arrow import test_arrow
import win32com.server.register
import cProfile
import pstats
import io

site=Site(site='CENTRAL',domain='5420')

def get_sd_analysis():
    df_anal=site.odbc_nav.run_sd_failure_analysis()
    if df_anal is None:
        return
    return site.odbc_nav.get_df_xml(df_anal,title="TEST",user="test")

def oa_tables():
    profiler = cProfile.Profile()
    profiler.enable()
    df= site.odbc_nav.run_odbc_query(
    """
    Select * from oa_tables 
    """
    )
    profiler.disable()
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    return df

def oa_tables_pl():
    profiler = cProfile.Profile()
    profiler.enable()
    df= site.odbc_nav.run_odbc_query_pl(
    """
    Select * from oa_tables 
    """
    )
    profiler.disable()
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    return df

def oa_columns():
    return site.odbc_nav.run_odbc_query_pl(
    """
    Select * from oa_columns 
    """
    )
    

    
def register_com():
    win32com.server.register.RegisterClasses(PythonExecutor)
    
def unregister_com():
    win32com.server.register.UnregisterClasses(PythonExecutor)

def test_arr():
    test_arrow()