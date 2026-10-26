# hook_finder_starter.sh: find hooks in core's source and on the running site (Session 3, Lesson 2.3, lab B)
# state: after:lesson_04
# expect: 2. TODO
#
# Lesson 2.3, "Finding the Hook You Need": read the source with grep, then ask the running site. The script runs
# in the WP-CLI container, in the WordPress root; from your project folder:
#     cp labs/module-03/l2_3-hooks/hook_finder_starter.sh wordpress/
#     docker compose run --rm wpcli sh hook_finder_starter.sh
# Replace each echo "N. TODO" line with one command, run again, compare with "Expected when done".
# Make each grep pattern exact (with the quotes and spaces core uses), so it finds the call and not a comment.
# When you are done: rm wordpress/hook_finder_starter.sh

echo "== 1. Where core fires wp_head =="
grep -rn "do_action( 'wp_head' )" wp-includes/          # done for you

echo "== 2. Who adds the generator tag =="
# TODO 2: the line of wp-includes/default-filters.php that attaches wp_generator to wp_head (grep -n).
echo "2. TODO"

echo "== 3. Where the excerpt length is filtered =="
# TODO 3: the file and line in wp-includes/ that call apply_filters( 'excerpt_length', ... ) (grep -rn).
echo "3. TODO"

echo "== 4. Asked of the running site =="
# TODO 4: wp eval that prints "wpautop on the_content: " and has_filter( "the_content", "wpautop" ) through
#         var_export( ..., true ). Inside the single quotes of wp eval, use double quotes for PHP strings.
echo "4. TODO"

echo "== 5. Callbacks on wp_head =="
# TODO 5: wp eval that prints how many callbacks hang on wp_head: $GLOBALS["wp_filter"]["wp_head"]->callbacks is
#         an array of priority => callbacks; array_map( "count", ... ) counts each group, array_sum() adds them.
echo "5. TODO"

# Expected when done (hook_finder_solution.sh, the course site; line numbers are WordPress 7.1.3's):
# == 1. Where core fires wp_head ==
# wp-includes/general-template.php:3441:	do_action( 'wp_head' );
# == 2. Who adds the generator tag ==
# 362:add_action( 'wp_head', 'wp_generator' );
# == 3. Where the excerpt length is filtered ==
# wp-includes/formatting.php:4081:		$excerpt_length = (int) apply_filters( 'excerpt_length', $excerpt_length );
# wp-includes/blocks/latest-posts.php:167:				$excerpt_length = (int) apply_filters( 'excerpt_length', $block_core_latest_posts_excerpt_length );
# == 4. Asked of the running site ==
# wpautop on the_content: 10
# == 5. Callbacks on wp_head ==
# 30
