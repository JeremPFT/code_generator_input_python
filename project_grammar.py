import ply.yacc as yacc

'''
project_def              : PROJECT_START project_name output_directory package_list PROJECT_STOP;
project_name             : IDENTIFIER;
IDENTIFIER               : [a-z][a-z0-9_];
output_directory         : quoted_string;
package_list             : NULL | package_list package_def;
package_def              : PACKAGE_START package_name dependance_list packageable_element_list PACKAGE_STOP;
package_name             : IDENTIFIER;
dependance_list          : NULL | dependance_list dependance_def;
packageable_element_list : NULL | packageable_element_list packageable_element_def;
packageable_element_def  : type_def | subprogram_def
'''
