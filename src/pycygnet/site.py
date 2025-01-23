from typing import Self
import win32com.client
import warnings
from pycygnet.oa_tabs_nav import OATabsNav

warnings.simplefilter(action='ignore', category=UserWarning)

class Site:
    """
       singletone, initializes connections to com objects of different CygNet services,
    """
    _instance = None
    _site = ""
    _domain = ""

    def __new__(cls, site: str = 'CYGNET', domain: str = "5410") -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._site = site
            cls._instance._domain = domain

        return cls._instance

    @classmethod
    def destroy(cls):
        cls._instance = None

    def __init__(self, site: str = "", domain: str = "") -> None:
        self.global_funcs = None
        self.dds_client = None
        self.uis_client = None
        self.fac_client = None
        self.pnt_client = None
        self.odbc_nav = OATabsNav(site=self._site, domain=self._domain)
        self._init_clients(self._site)

    def _init_clients(self, site: str):
        """
        connect clients for DSS, FAC and PNT services
        params:
        site --> the CygNet site to connect to
        """
        self.global_funcs = win32com.client.Dispatch(
            "CxScript.GlobalFunctions")
        self.dds_client = win32com.client.Dispatch("CxDds.DdsClient")
        self.dds_client.Connect(f"[{self._domain}]{site}.DDS")
        self.uis_client = win32com.client.Dispatch("CxUis.UisClient")
        self.uis_client.Connect(f"[{self._domain}]{site}.UIS")
        self.fac_client = win32com.client.Dispatch('CxFac.FacClient')
        self.fac_client.Connect(f'[{self._domain}]{site}.FAC')
        self.pnt_client = win32com.client.Dispatch('CxPnt.PntClient')
        self.pnt_client.Connect(f'[{self._domain}]{site}.PNT')
        self.grp_client = win32com.client.Dispatch("CxGrp.GrpClient")
        self.grp_client.Connect(f'[{self._domain}]{site}.STORAGE')
