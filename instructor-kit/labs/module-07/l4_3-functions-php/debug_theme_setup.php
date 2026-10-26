<?php
/**
 * debug_theme_setup.php: three theme-setup calls copied from a forum post (Session 7, Lesson 4.3, find-the-bug handout)
 * state: after:lesson_13
 * expect-error: doing_it_wrong
 *
 * Each block below is one job from Lesson 4.3, typed straight into a script so you can see what WordPress makes
 * of it (WordPress is loaded, so it is already past init, the moment such calls normally happen). From your
 * project folder:
 *     cp labs/module-07/l4_3-functions-php/debug_theme_setup.php wordpress/
 *     wp eval-file --use-include debug_theme_setup.php
 * Two calls announce themselves with "called incorrectly" notices (read each from the left); WordPress then
 * carries on with a default or ignores the call. The third is SILENT: compare its line with what the comment above
 * it wanted. Fixed, the three lines say: footer-shop, a list that still includes search-form, and ?ver= with the
 * active theme's own version. When you are done:
 * rm wordpress/debug_theme_setup.php
 */

// 1. A widget area for the shop's footer.
register_sidebar( array( 'name' => 'Shop footer' ) );   // its id should be footer-shop
echo 'widget area id: ', array_key_last( $GLOBALS['wp_registered_sidebars'] ), "\n";

// 2. HTML5 markup for the search form.
add_theme_support( 'html5', 'search-form' );
echo 'html5 for: ', implode( ', ', (array) ( get_theme_support( 'html5' )[0] ?? array() ) ), "\n";

// 3. A stylesheet whose URL changes with every release of the active theme (its Version in style.css).
wp_enqueue_style( 'pagesco-lab-extra', get_parent_theme_file_uri( 'extra.css' ) );
ob_start();
wp_print_styles( array( 'pagesco-lab-extra' ) );
preg_match( "#\\?ver=[^']*#", ob_get_clean(), $pagesco_ver );
echo 'stylesheet: ', $pagesco_ver[0] ?? '(none)', ' (the theme is at ', wp_get_theme( get_template() )->get( 'Version' ), ")\n";
