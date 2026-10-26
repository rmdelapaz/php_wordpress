# hook_finder_solution.sh: the instructor's reference for hook_finder_starter.sh (Session 3, Lesson 2.3, lab B)
# state: after:lesson_04
# expect: add_action( 'wp_head', 'wp_generator' );
# expect: wpautop on the_content: 10

echo "== 1. Where core fires wp_head =="
grep -rn "do_action( 'wp_head' )" wp-includes/

echo "== 2. Who adds the generator tag =="
grep -n "'wp_head', 'wp_generator'" wp-includes/default-filters.php

echo "== 3. Where the excerpt length is filtered =="
grep -rn "apply_filters( 'excerpt_length'" wp-includes/

echo "== 4. Asked of the running site =="
wp eval 'echo "wpautop on the_content: ", var_export( has_filter( "the_content", "wpautop" ), true ), "\n";'

echo "== 5. Callbacks on wp_head =="
wp eval 'echo array_sum( array_map( "count", $GLOBALS["wp_filter"]["wp_head"]->callbacks ) ), "\n";'
