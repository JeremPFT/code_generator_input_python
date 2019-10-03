project code_generator_model

  output_directory "d:/Users/jpiffret/AppData/Roaming/Dropbox/projets_perso/"
                   & "ada/code_generator_input/examples/model"

  package truc
  end package truc

  package model

    --------------------
    --  element
    --------------------

    abstract value_object element
      --
      -- define packages model.element and model.types.element

      limited with model.comment
      use model.types.element
      use model.types.comment
      --
      --  dependances are the first printed lines
      --  "use" implies ada "with" clause

      owned_comments : comment_vector

    end value_object element

    abstract value_object named_element (element)
      name : string
      xxx : yyy
    end value_object named_element

--jpi    abstract value_object element
--jpi
--jpi      initialize
--jpi      ;; pre "comment_count = 0 and then owned_element_count = 0"
--jpi      ;; post "comment_count = 0 and then owned_element_count = 0"
--jpi      ;; implementation "null;" end implementation
--jpi      --
--jpi      --  specific subprogram to initialize an instance
--jpi      --  no parameter
--jpi      --  xyz_count are defined by fields
--jpi      --  postconditions are to be copied from preconditions
--jpi      --
--jpi      --  implementation: inline implementation possible for any subprogram
--jpi      --  contains a list of strings (at least 1 if present)
--jpi
--jpi      owned_comments : vector comment
--jpi      owned_elements : vector element
--jpi      --
--jpi      -- for each "abcde : vector xyz", generate queries:
--jpi      -- abcde_count, abcde_xyz (index), owns_abcde, add_abcde (object)
--jpi
--jpi      owner : access class_t := null;
--jpi
--jpi      query has_owner return boolean
--jpi      implementation "return self.owner /= null;" end implementation
--jpi
--jpi      query get_owner return not null access constant object_t'class
--jpi      pre => self.has_owner
--jpi      implementation "return self.owner;" end implementation
--jpi
--jpi      query is_owned_by ( object : not null access constant object_t'class )
--jpi      implementation
--jpi      "obj_access : constant access constant object_t'class;"
--jpi      "return self.owner = object;"
--jpi      end implementation
--jpi      --
--jpi      --  should be separate
--jpi      --  implementation separate
--jpi      --  separate close the implementation section
--jpi      --  implementation .. end implementation is implementation_inline
--jpi      --  implementation separate is implementation_separate
--jpi
--jpi      query must_be_owned return boolean
--jpi      implementation "return true;" end implementation
--jpi
--jpi      command command_for_test
--jpi
--jpi    end value_object element

    --------------------
    --  comment
    --------------------

   -- value_object comment extends element

   --   initialize
   --   (Text   : in     String;
   --    Header : in     String := "";
   --    Footer : in     String := "";
   --    Prefix : in     String := "";
   --    Suffix : in     String := "")
   --   pre => Text /= ""
   --   post => pre
   --   implementation: "null;" end implementation
   --   --
   --   --  see if a Create can be created automatically (the object is not abstract)

   -- end value_object comment

  end package model

--  end project code_generator_modelx
--  end project code_generator_model
end project
