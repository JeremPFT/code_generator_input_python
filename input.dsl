project code_generator_model

  output_directory "d:/Users/jpiffret/AppData/Roaming/Dropbox/projets_perso/"
                   & "ada/code_generator_input/examples/model"

  --  TODO: implement the concatenation

  package model

    --------------------
    --  element
    --------------------

    value_object element is abstract
      --
      -- define packages model.element and model.types.element

      limited with model.comment
      use model.types.element
      use model.types.comment
      --
      --  dependances are the first printed lines
      --  "use" implies ada "with" clause

      initialize
      pre => comment_count = 0 and owned_element_count = 0
      post => pre
      implementation: "null;" end implementation
      --
      --  specific subprogram to initialize an instance
      --  no parameter
      --  xyz_count are defined by fields
      --  postconditions are to be copied from preconditions
      --
      --  implementation: inline implementation possible for any subprogram
      --  contains a list of strings (at least 1 if present)

      owned_comments : vector comment
      owned_elements : vector element
      --
      -- for each "abcde : vector xyz", generate queries:
      -- abcde_count, abcde_xyz (index), owns_abcde, add_abcde (object)

      owner : access class_t := null;

      query has_owner return boolean
      implementation "return self.owner /= null;" end implementation

      query get_owner return not null access constant object_t'class
      pre => self.has_owner
      implementation "return self.owner;" end implementation

      query is_owned_by ( object : not null access constant object_t'class )
      implementation
      "obj_access : constant access constant object_t'class;"
      "return self.owner = object;"
      end implementation
      --
      --  should be separate
      --  implementation separate
      --  separate close the implementation section
      --  implementation .. end implementation is implementation_inline
      --  implementation separate is implementation_separate

      query must_be_owned return boolean
      implementation "return true;" end implementation

    end value_object element

    --------------------
    --  comment
    --------------------

    value_object comment extends element

      initialize
      (Text   : in     String;
       Header : in     String := "";
       Footer : in     String := "";
       Prefix : in     String := "";
       Suffix : in     String := "")
      pre => Text /= ""
      post => pre
      implementation: "null;" end implementation
      --
      --  see if a Create can be created automatically (the object is not abstract)

    end value_object comment

  end package model

end project
