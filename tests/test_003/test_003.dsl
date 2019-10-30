project test_003

  output_directory "~/tests/test_003";

  type static_library;

  readme_title "test 003 title"
  readme_brief "test 003" & " brief"

  package a_first_package
    value_object basic_object
    end value_object basic_object;

    --    value_object element is abstract
    --      property owned_comment comment * unique ordered;
    --      property owned_element element 0..n unique ordered;
    --      property owner         element 0..1;
    --
    --      method all_owned_element return element * unique ordered
    --    end value_object;

    --    value_object named_element is abstract new element
    --      with some_dependance;
    --      property owned_comment comment * unique ordered;
    --      property owned_element element 0..n unique ordered;
    --      property owner         element 0..1;
    --
    --      method all_owned_element return element * unique ordered
    --    end value_object;
  end package a_first_package;

  package a_second_package
  end package a_second_package;

end project test_003;
