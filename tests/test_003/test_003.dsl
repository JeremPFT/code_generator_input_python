project test_003

  output_directory "~/tests/test_003";

  type static_library;

  readme_title "test 003 title"
  readme_brief "test 003" & " brief"

  package a_first_package
    value_object element is abstract
      property comment : [0-n] ordered
    end value_object;
  end package a_first_package;

end project test_003;
