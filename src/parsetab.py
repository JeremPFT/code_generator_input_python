
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ABSTRACT AMP AND COLON COLONEQ COMMAND COMMENT END EQUAL EXCEPTIONS FIELD IDENTIFIER IMPLEMENTATION IN INFERIOR INOUT INTEGER_VALUE IS LIMITED LPAREN OPERATION OR OUT OUTPUT_DIRECTORY PACKAGE POST PRE PROJECT QUERY RETURN RPAREN SEMICOLON STRING_VALUE SUBPROGRAM SUPERIOR TYPE USE VALUE VALUE_OBJECT VECTOR WITH\n    project : PROJECT OUTPUT_DIRECTORY\n    \n    project : project_init project_content project_close\n    \n    project_init : PROJECT IDENTIFIER\n    \n    project_content : output_directory project_type package_list\n    \n    project_close : END PROJECT IDENTIFIER SEMICOLON\n    \n    project_close : END PROJECT SEMICOLON\n    \n    package_list :\n    \n    package_list : package_list package\n    \n    package : package_init package_content package_close\n    \n    package_init : PACKAGE IDENTIFIER\n    \n    package_content : dependance_list packageable_element_list\n    \n    package_close : END PACKAGE IDENTIFIER SEMICOLON\n    \n    package_close : END PACKAGE SEMICOLON\n    \n    dependance_list :\n    \n    dependance_list : dependance_list dependance\n    \n    dependance : WITH IDENTIFIER\n    \n    dependance : USE IDENTIFIER\n    \n    dependance : LIMITED WITH IDENTIFIER\n    \n    packageable_element_list :\n    \n    packageable_element_list : packageable_element_list packageable_element\n    \n    packageable_element : operation\n                        | type_item\n    \n    type_item : value_object\n              | exception_block\n    \n    exception_block : EXCEPTIONS exception_list exception_item END EXCEPTIONS SEMICOLON\n    \n    exception_list :\n    \n    exception_list : exception_list exception_item\n    \n    exception_item : IDENTIFIER\n    \n    value_object : value_object_init value_object_content value_object_close\n    \n    value_object_init : value_object_init_abstract_inherit\n                      | value_object_init_abstract\n                      | value_object_init_inherit\n                      | value_object_init_simple\n    \n    value_object_init_abstract_inherit : ABSTRACT VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN\n    \n    value_object_init_abstract : ABSTRACT VALUE_OBJECT IDENTIFIER\n    \n    value_object_init_inherit : VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN\n    \n    value_object_init_simple : VALUE_OBJECT IDENTIFIER\n    \n    value_object_content : dependance_list feature_list\n    \n    value_object_close : END VALUE_OBJECT IDENTIFIER SEMICOLON\n    \n    value_object_close : END VALUE_OBJECT SEMICOLON\n    \n    feature_list :\n    \n    feature_list : feature_list feature\n    \n    feature : property SEMICOLON\n            | operation SEMICOLON\n    \n    operation : operation_init parameter_list operation_return\n    \n    operation_init : OPERATION IDENTIFIER\n    \n    operation_return :\n    \n    operation_return : RETURN IDENTIFIER\n    \n    parameter_list :\n    \n    parameter_list : LPAREN parameter_item RPAREN\n    \n    parameter_list : LPAREN parameter_item_list parameter_item RPAREN\n    \n    parameter_item_list : parameter_item SEMICOLON\n    \n    parameter_item_list : parameter_item_list parameter_item\n    \n    parameter_item : IDENTIFIER COLON direction IDENTIFIER\n    \n    direction : INOUT\n              | OUT\n              | IN\n    \n    property : IDENTIFIER COLON IDENTIFIER\n    \n    project_type : TYPE IDENTIFIER SEMICOLON\n    \n    output_directory : OUTPUT_DIRECTORY string SEMICOLON\n    \n    string : string AMP STRING_VALUE\n    \n    string : STRING_VALUE\n    '
    
_lr_action_items = {'PROJECT':([0,10,],[2,15,]),'$end':([1,4,9,21,27,],[0,-1,-2,-6,-5,]),'OUTPUT_DIRECTORY':([2,3,5,],[4,8,-3,]),'IDENTIFIER':([2,12,15,24,34,35,36,38,45,46,47,48,49,50,51,53,54,55,56,60,63,64,65,66,67,70,72,76,77,78,79,80,83,84,86,87,92,95,96,97,98,101,102,103,106,107,111,],[5,17,20,30,-15,54,55,57,61,-14,-26,-30,-31,-32,-33,66,-16,-17,67,73,-41,78,79,-37,-18,81,73,90,-27,-28,-35,93,-52,-53,99,-42,105,107,-55,-56,-57,-43,-44,109,-36,-54,-34,]),'END':([6,11,16,22,23,25,28,29,30,31,33,34,39,40,41,42,43,44,46,48,49,50,51,54,55,58,59,61,62,63,66,67,68,69,74,76,77,78,79,81,82,87,94,100,101,102,106,108,110,111,],[10,-7,-4,-8,-14,-59,32,-19,-10,-9,-11,-15,-20,-21,-22,-49,-23,-24,-14,-30,-31,-32,-33,-16,-17,-13,-47,-46,75,-41,-37,-18,-12,-45,-29,-38,91,-28,-35,-48,-50,-42,-51,-40,-43,-44,-36,-39,-25,-34,]),'TYPE':([7,18,],[12,-60,]),'STRING_VALUE':([8,19,],[14,26,]),'PACKAGE':([11,16,22,25,31,32,58,68,],[-7,24,-8,-59,-9,38,-13,-12,]),'SEMICOLON':([13,14,15,17,20,26,38,42,57,59,61,69,71,81,82,86,88,89,94,99,104,107,109,],[18,-62,21,25,27,-61,58,-49,68,-47,-46,-45,83,-48,-50,100,101,102,-51,108,110,-54,-58,]),'AMP':([13,14,26,],[19,-62,-61,]),'WITH':([23,29,30,34,37,46,48,49,50,51,54,55,63,66,67,79,106,111,],[-14,35,-10,-15,56,-14,-30,-31,-32,-33,-16,-17,35,-37,-18,-35,-36,-34,]),'USE':([23,29,30,34,46,48,49,50,51,54,55,63,66,67,79,106,111,],[-14,36,-10,-15,-14,-30,-31,-32,-33,-16,-17,36,-37,-18,-35,-36,-34,]),'LIMITED':([23,29,30,34,46,48,49,50,51,54,55,63,66,67,79,106,111,],[-14,37,-10,-15,-14,-30,-31,-32,-33,-16,-17,37,-37,-18,-35,-36,-34,]),'OPERATION':([23,29,30,33,34,39,40,41,42,43,44,46,48,49,50,51,54,55,59,61,63,66,67,69,74,76,79,81,82,87,94,100,101,102,106,108,110,111,],[-14,-19,-10,45,-15,-20,-21,-22,-49,-23,-24,-14,-30,-31,-32,-33,-16,-17,-47,-46,-41,-37,-18,-45,-29,45,-35,-48,-50,-42,-51,-40,-43,-44,-36,-39,-25,-34,]),'EXCEPTIONS':([23,29,30,33,34,39,40,41,42,43,44,54,55,59,61,67,69,74,81,82,91,94,100,108,110,],[-14,-19,-10,47,-15,-20,-21,-22,-49,-23,-24,-16,-17,-47,-46,-18,-45,-29,-48,-50,104,-51,-40,-39,-25,]),'ABSTRACT':([23,29,30,33,34,39,40,41,42,43,44,54,55,59,61,67,69,74,81,82,94,100,108,110,],[-14,-19,-10,52,-15,-20,-21,-22,-49,-23,-24,-16,-17,-47,-46,-18,-45,-29,-48,-50,-51,-40,-39,-25,]),'VALUE_OBJECT':([23,29,30,33,34,39,40,41,42,43,44,52,54,55,59,61,67,69,74,75,81,82,94,100,108,110,],[-14,-19,-10,53,-15,-20,-21,-22,-49,-23,-24,65,-16,-17,-47,-46,-18,-45,-29,86,-48,-50,-51,-40,-39,-25,]),'RETURN':([42,59,61,82,94,],[-49,70,-46,-50,-51,]),'LPAREN':([42,61,66,79,],[60,-46,80,92,]),'RPAREN':([71,84,93,105,107,],[82,94,106,111,-54,]),'COLON':([73,90,],[85,103,]),'INOUT':([85,],[96,]),'OUT':([85,],[97,]),'IN':([85,],[98,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'project':([0,],[1,]),'project_init':([0,],[3,]),'project_content':([3,],[6,]),'output_directory':([3,],[7,]),'project_close':([6,],[9,]),'project_type':([7,],[11,]),'string':([8,],[13,]),'package_list':([11,],[16,]),'package':([16,],[22,]),'package_init':([16,],[23,]),'package_content':([23,],[28,]),'dependance_list':([23,46,],[29,63,]),'package_close':([28,],[31,]),'packageable_element_list':([29,],[33,]),'dependance':([29,63,],[34,34,]),'packageable_element':([33,],[39,]),'operation':([33,76,],[40,89,]),'type_item':([33,],[41,]),'operation_init':([33,76,],[42,42,]),'value_object':([33,],[43,]),'exception_block':([33,],[44,]),'value_object_init':([33,],[46,]),'value_object_init_abstract_inherit':([33,],[48,]),'value_object_init_abstract':([33,],[49,]),'value_object_init_inherit':([33,],[50,]),'value_object_init_simple':([33,],[51,]),'parameter_list':([42,],[59,]),'value_object_content':([46,],[62,]),'exception_list':([47,],[64,]),'operation_return':([59,],[69,]),'parameter_item':([60,72,],[71,84,]),'parameter_item_list':([60,],[72,]),'value_object_close':([62,],[74,]),'feature_list':([63,],[76,]),'exception_item':([64,],[77,]),'feature':([76,],[87,]),'property':([76,],[88,]),'direction':([85,],[95,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> project","S'",1,None,None,None),
  ('project -> PROJECT OUTPUT_DIRECTORY','project',2,'p_project_item_no_named','dsl_grammar.py',88),
  ('project -> project_init project_content project_close','project',3,'p_project_item','dsl_grammar.py',94),
  ('project_init -> PROJECT IDENTIFIER','project_init',2,'p_project_init','dsl_grammar.py',100),
  ('project_content -> output_directory project_type package_list','project_content',3,'p_project_content','dsl_grammar.py',116),
  ('project_close -> END PROJECT IDENTIFIER SEMICOLON','project_close',4,'p_project_close_named','dsl_grammar.py',126),
  ('project_close -> END PROJECT SEMICOLON','project_close',3,'p_project_close','dsl_grammar.py',132),
  ('package_list -> <empty>','package_list',0,'p_package_list_empty','dsl_grammar.py',142),
  ('package_list -> package_list package','package_list',2,'p_package_list_more','dsl_grammar.py',148),
  ('package -> package_init package_content package_close','package',3,'p_package_item','dsl_grammar.py',155),
  ('package_init -> PACKAGE IDENTIFIER','package_init',2,'p_package_init','dsl_grammar.py',162),
  ('package_content -> dependance_list packageable_element_list','package_content',2,'p_package_content','dsl_grammar.py',169),
  ('package_close -> END PACKAGE IDENTIFIER SEMICOLON','package_close',4,'p_package_close_named','dsl_grammar.py',176),
  ('package_close -> END PACKAGE SEMICOLON','package_close',3,'p_package_close','dsl_grammar.py',182),
  ('dependance_list -> <empty>','dependance_list',0,'p_dependance_list_empty','dsl_grammar.py',192),
  ('dependance_list -> dependance_list dependance','dependance_list',2,'p_dependance_list_more','dsl_grammar.py',198),
  ('dependance -> WITH IDENTIFIER','dependance',2,'p_dependance_with','dsl_grammar.py',205),
  ('dependance -> USE IDENTIFIER','dependance',2,'p_dependance_use','dsl_grammar.py',211),
  ('dependance -> LIMITED WITH IDENTIFIER','dependance',3,'p_dependance_limited_with','dsl_grammar.py',217),
  ('packageable_element_list -> <empty>','packageable_element_list',0,'p_packageable_element_list_empty','dsl_grammar.py',227),
  ('packageable_element_list -> packageable_element_list packageable_element','packageable_element_list',2,'p_packageable_element_list_more','dsl_grammar.py',233),
  ('packageable_element -> operation','packageable_element',1,'p_packageable_element_item','dsl_grammar.py',240),
  ('packageable_element -> type_item','packageable_element',1,'p_packageable_element_item','dsl_grammar.py',241),
  ('type_item -> value_object','type_item',1,'p_type_item','dsl_grammar.py',249),
  ('type_item -> exception_block','type_item',1,'p_type_item','dsl_grammar.py',250),
  ('exception_block -> EXCEPTIONS exception_list exception_item END EXCEPTIONS SEMICOLON','exception_block',6,'p_exception_block','dsl_grammar.py',256),
  ('exception_list -> <empty>','exception_list',0,'p_exception_list_empty','dsl_grammar.py',261),
  ('exception_list -> exception_list exception_item','exception_list',2,'p_exception_list_more','dsl_grammar.py',267),
  ('exception_item -> IDENTIFIER','exception_item',1,'p_exception_item','dsl_grammar.py',274),
  ('value_object -> value_object_init value_object_content value_object_close','value_object',3,'p_value_object_item','dsl_grammar.py',284),
  ('value_object_init -> value_object_init_abstract_inherit','value_object_init',1,'p_value_object_init','dsl_grammar.py',290),
  ('value_object_init -> value_object_init_abstract','value_object_init',1,'p_value_object_init','dsl_grammar.py',291),
  ('value_object_init -> value_object_init_inherit','value_object_init',1,'p_value_object_init','dsl_grammar.py',292),
  ('value_object_init -> value_object_init_simple','value_object_init',1,'p_value_object_init','dsl_grammar.py',293),
  ('value_object_init_abstract_inherit -> ABSTRACT VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN','value_object_init_abstract_inherit',6,'p_value_object_init_abstract_inherit','dsl_grammar.py',300),
  ('value_object_init_abstract -> ABSTRACT VALUE_OBJECT IDENTIFIER','value_object_init_abstract',3,'p_value_object_init_abstract','dsl_grammar.py',313),
  ('value_object_init_inherit -> VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN','value_object_init_inherit',5,'p_value_object_init_inherit','dsl_grammar.py',324),
  ('value_object_init_simple -> VALUE_OBJECT IDENTIFIER','value_object_init_simple',2,'p_value_object_init_simple','dsl_grammar.py',335),
  ('value_object_content -> dependance_list feature_list','value_object_content',2,'p_value_object_content','dsl_grammar.py',343),
  ('value_object_close -> END VALUE_OBJECT IDENTIFIER SEMICOLON','value_object_close',4,'p_value_object_close_named','dsl_grammar.py',355),
  ('value_object_close -> END VALUE_OBJECT SEMICOLON','value_object_close',3,'p_value_object_close','dsl_grammar.py',361),
  ('feature_list -> <empty>','feature_list',0,'p_feature_list_none','dsl_grammar.py',371),
  ('feature_list -> feature_list feature','feature_list',2,'p_feature_list_more','dsl_grammar.py',377),
  ('feature -> property SEMICOLON','feature',2,'p_feature_item','dsl_grammar.py',384),
  ('feature -> operation SEMICOLON','feature',2,'p_feature_item','dsl_grammar.py',385),
  ('operation -> operation_init parameter_list operation_return','operation',3,'p_operation_item','dsl_grammar.py',395),
  ('operation_init -> OPERATION IDENTIFIER','operation_init',2,'p_operation_init','dsl_grammar.py',411),
  ('operation_return -> <empty>','operation_return',0,'p_operation_return_none','dsl_grammar.py',417),
  ('operation_return -> RETURN IDENTIFIER','operation_return',2,'p_operation_return_one','dsl_grammar.py',423),
  ('parameter_list -> <empty>','parameter_list',0,'p_parameter_list','dsl_grammar.py',431),
  ('parameter_list -> LPAREN parameter_item RPAREN','parameter_list',3,'p_parameter_list_one','dsl_grammar.py',437),
  ('parameter_list -> LPAREN parameter_item_list parameter_item RPAREN','parameter_list',4,'p_parameter_list_more','dsl_grammar.py',443),
  ('parameter_item_list -> parameter_item SEMICOLON','parameter_item_list',2,'p_parameter_item_list_one','dsl_grammar.py',450),
  ('parameter_item_list -> parameter_item_list parameter_item','parameter_item_list',2,'p_parameter_item_list_more','dsl_grammar.py',456),
  ('parameter_item -> IDENTIFIER COLON direction IDENTIFIER','parameter_item',4,'p_parameter_item','dsl_grammar.py',463),
  ('direction -> INOUT','direction',1,'p_direction','dsl_grammar.py',469),
  ('direction -> OUT','direction',1,'p_direction','dsl_grammar.py',470),
  ('direction -> IN','direction',1,'p_direction','dsl_grammar.py',471),
  ('property -> IDENTIFIER COLON IDENTIFIER','property',3,'p_property_item','dsl_grammar.py',513),
  ('project_type -> TYPE IDENTIFIER SEMICOLON','project_type',3,'p_project_type','dsl_grammar.py',523),
  ('output_directory -> OUTPUT_DIRECTORY string SEMICOLON','output_directory',3,'p_output_directory','dsl_grammar.py',535),
  ('string -> string AMP STRING_VALUE','string',3,'p_string_one_or_more','dsl_grammar.py',541),
  ('string -> STRING_VALUE','string',1,'p_string_one','dsl_grammar.py',549),
]
