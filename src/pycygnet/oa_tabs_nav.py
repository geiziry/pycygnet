from datetime import datetime
import polars as pl
import xml.etree.ElementTree as ET
import pyodbc
import pandas as pd

class OATabsNav:
    """
    ODBC tables navigator using the tables indexing in the oa_tables odbc table
    will be instantiated with the Connection object
    """

    def __init__(self,  domain: str = "5420",site:str="CYGNET"):
        self._site=site.lower()
        self.conn_str='Driver={CygNet ODBC Driver};'+f'port={domain}'+';Servicename=OpenAccess_CygNet;Warnings=0;EditWarnings=0'
        self.odbc = pyodbc.connect(f'DSN=CygNet;ConnectDomain={domain};Warnings=0;EditWarnings=0')


    def run_odbc_query(self, querystr: str) -> pd.DataFrame :
        """
        runs Cygnet ODBC query
        """
        return pd.read_sql_query(querystr, self.odbc)

    def run_odbc_query_pl(self, querystr: str) -> pl.DataFrame :
        """
        runs Cygnet ODBC query
        """
        return pl.read_database(querystr, self.conn_str)

    def run_sd_failure_analysis(self)->pl.DataFrame|None:
        df=self.run_odbc_query_pl(
        """
        Select PointIdLong,Value,RecordTime From central_vhsrep.Historicalvalues t1
        where PointIdLong Like '%WL_STFLOW' AND YEAR(RecordTime)=YEAR(CURDATE()) AND MONTH(RecordTime)=MONTH(CURDATE())
        """)
        results=[]
        for name,grp in df.group_by('PointIdLong'):
            grp = grp.with_columns([
            pl.col('Value').shift(1).alias('previous_values')])
            grp = grp.with_columns([
            ((pl.col('Value') == '0') &
            ((pl.col('previous_values') != '0') | pl.col('previous_values').is_null())).alias('start_of_interval')])
            interval_count = grp["start_of_interval"].sum()
            results.append({"well": str(name[0])[:-7], "shut-down": interval_count})

        return pl.DataFrame(results)


    def run_sql_query(self,querystr:str):
        cursor=self.odbc.cursor()
        cursor.execute(querystr)
        num_updates=cursor.rowcount
        cursor.close()
        return num_updates

    def replace_udcs(self,ref_df:pl.DataFrame,old_udc_col:str,new_udc_col:str):
        ref_df=ref_df.unique(subset=[old_udc_col],maintain_order=True)
        no_udcs=len(ref_df[old_udc_col])
        n_trs,n_pnt,n_dds=0,0,0
        errors,updated,not_updated='','',''
        for row in ref_df.iter_rows(named=True):
            old_udc=row[old_udc_col]
            new_udc=row[new_udc_col]
            # 1 - update TRS table with new udc
            try:
                trs_query=f"UPDATE {self._site}_trs.table_header_record SET table_entry='{new_udc}' WHERE table_entry='{old_udc}'"
                n_trs_updates=self.run_sql_query(trs_query)
                if n_trs_updates==0:
                    not_updated+=f'{old_udc}\n'
                updated+=f'{n_trs_updates} - {old_udc}\n'
                n_trs+=n_trs_updates
            except Exception as e:
                errors+=f'TRS Error with {old_udc} --- {e.args}\n'
                try:
                    self.run_sql_query(f"DELETE FROM {self._site}_trs.table_header_record WHERE table_entry='{old_udc}'")
                except Exception as e:
                    errors+=f'TRS DELETE Error with {old_udc} --- {e.args}\n'

                # 2 - update pnt with new udc
            try:
                pnt_query=f"UPDATE {self._site}_pnt.pnt_header_record SET  uniformdatacode=REPLACE(uniformdatacode,'{old_udc}','{new_udc}'), pointidlong=REPLACE(pointidlong,'{old_udc}','{new_udc}') WHERE uniformdatacode='{old_udc}'"
                n_pnt_updates=self.run_sql_query(pnt_query)
                n_pnt+=n_pnt_updates
            except Exception as e:
                errors+=f'PNT Error with {old_udc} --- {e.args}\n'

                # 3 - update udc mapping with new udc
            try:
                dds_query=f"UPDATE {self._site}_dds.dds_data_element_header SET  uniform_data_code='{new_udc}' WHERE uniform_data_code='{old_udc}'"
                n_dds_updates=self.run_sql_query(dds_query)
                n_dds+=n_dds_updates
            except Exception as e:
                errors+=f'DDS Error with {old_udc} --- {e.args}\n'

        self.odbc.commit()
        return f'number of udcs = {no_udcs} \nTRS updates = {n_trs} \nPNT updates = {n_pnt} \nDDS updates = {n_dds} \nErrors : {errors} \n==> Updated UDCs:\n{updated} \n==>Not updated UDCs:\n{not_updated}'


    def get_df_xml(self,df: pl.DataFrame,title:str,user:str)-> str:
        # create the root element
        root = ET.Element("ReportData")
        # add title, created, type, user, services, range start, and range end elements
        titleel = ET.SubElement(root, "Title")
        titleel.text = title

        created = ET.SubElement(root, "Created")
        created.text = datetime.now().strftime("%A, %B %d, %Y %I:%M:%S %p")

        type = ET.SubElement(root, "Type")
        type.text = "SourceType"

        userel = ET.SubElement(root, "User")
        userel.text = user

        range_start = ET.SubElement(root, "RangeStart")
        range_start.text = "2023-01-01"

        range_end = ET.SubElement(root, "RangeEnd")
        range_end.text = "2023-12-31"

        # add header element
        header = ET.SubElement(root, "Header")
        header.set("sub_section", "true")

        # add column header elements
        for i, col in enumerate(df.columns):
            col_header = ET.SubElement(header, f"Column{i}_Header")
            col_header.text = col

        # add row elements
        for row in df.rows():
            row_element = ET.SubElement(root, "Row")
            row_element.set("sub_section", "true")

            for i, val in enumerate(row):
                col_element = ET.SubElement(row_element, f"Column{i}")
                col_element.set("datatype", "0")
                col_element.text = str(val)

        # create an ElementTree object
        return ET.tostring(root, encoding='unicode')
