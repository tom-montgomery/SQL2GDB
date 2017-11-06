import numpy

import arcpy
import pyodbc


def sql2gdb(datadict, cnxn_string, workspace, sqltbl, target_tbl="output_table"):
    """ Converts a SQL table to a esri geodatabase table. Uses pyodbc cursor to fetch the records from SQL and passes
    them to a numpy array. Uses arcpy numpy array to table to create output. Parameters examples include the following:

      Dictionary datadict:
    Dictionary for numpy to map the field names followed their numpy types/lengths for the output table. Example:
    dts = {'names': (
        'txtSAPNo', 'txtProjectName', 'memProjectScope', 'txtProjectStatus', 'txtProjectManager',
        'txtCapitalProjectsOfficer',
        'txtManagingDivision', 'txtManagingDept', 'txtBenefittingDept', 'txtProjectAuthorization', 'txtProjectProgram',
        'txtProjectFunction', 'txtConsultant', 'txtContractor', 'EstimatedProjectAdvertisement',
        'EstimatedConstructionStart', 'EstimatedProjectCompletion', 'dblPRojectBudget',
        'dblProjectAppropriations', 'dblProjectExpenditures', 'hypQuadSheet', 'Junk4', 'Junk5'), 'formats': (
        'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255',
        'S255',
        'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255', 'S255')}

      String cnxn_string:
    String literal for pyodbc database connection:
    cnxn_string = r"Driver={SQL Server};SERVER=ssvs8;DATABASE=CIMSGIS_PROD;Trusted_Connection=yes;"

      String workspace:
    Location of destination geodatabase for the table.

       String sqltbl:
    Name of table in SQL server to copy to ESRI table.

      String target_tbl:
    Oprtional parameter to name output table in file geodatabase. Default name is output_table."""
    print "Converting SQL table {0} to ESRI Geodatabase table".format(sqltbl)
    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()
    cursor.execute(r"select * from {0}".format(sqltbl))
    rows = cursor.fetchall()
    array = numpy.rec.fromrecords(rows, datadict)
    arcpy.da.NumPyArrayToTable(array, "{0}\{1}".format(workspace, target_tbl))


