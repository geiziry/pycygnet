#usage: python pythoncyg.py --register / --unregister
import win32com.server.register
import io
import sys

class PythonExecutor:
    _reg_clsid_ = "{2d989d30-3dbf-4883-8f77-aa4648067237}"  # Replace with your own GUID
    _reg_desc_ = "Python Executor COM Server"
    _reg_progid_ = "PythonCOM.Executor"
    _public_methods_ = ['ExecuteCode']

    def ExecuteCode(self, code):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            exec(code)
            return sys.stdout.getvalue()
        except Exception as e:
            return str(e)
        finally:
            sys.stdout = old_stdout
            
            return "code executed successfully"

if __name__ == "__main__":
    win32com.server.register.UseCommandLine(PythonExecutor)
    
# %%
#print ("PythonExecutor")
# %%

# %%
