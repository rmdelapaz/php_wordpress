<?php
/**
 * The only template of the Shelf lab theme (Session 6, Lesson 4.1, lab A: the starter).
 *
 * One file draws every page, because the Loop walks whatever the main query found (Lesson 4.1). Each list item
 * should read "<linked title> · <date as Y-m-d> · <author>". Work through the TODOs and run test_shelf_theme.sh
 * after each one. Use the theme's prefix for any variable you add: $pagesco_lab_shelf_...
 *
 * TODO 1: the Loop. Replace the TODO paragraph with if ( have_posts() ) { ... } and, inside it, a <ul> with one
 *         <li class="shelf-item"> per post: while ( have_posts() ) { the_post(); ... }.
 * TODO 2: in each item, the linked title with the_title( $before, $after ) and esc_url( get_permalink() ), then
 *         " · " and the date from get_the_date( 'Y-m-d' ), then " · " and get_the_author(): both escaped with
 *         esc_html(), because get_ functions return values you escape yourself.
 * TODO 3: give the link a title attribute with the_title_attribute() (the_title() is not escaped for attributes).
 * TODO 4: the heading. Use conditional tags: is_home() "Latest from the shop"; is_category() "Shelf: " and the
 *         category's name (single_cat_title( '', false )); is_search() "Found for: " and the search terms
 *         (get_search_query( false ), escaped); is_singular() the post's own title (single_post_title( '', false ));
 *         anything else "Archive".
 * TODO 5: when the main query found nothing (the else of TODO 1), print <p class="shelf-empty">Nothing on this
 *         shelf.</p> (translatable, with the theme's text domain).
 *
 * @package pagesco-lab-shelf
 */

?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<main>
	<h1>TODO</h1>
	<p class="todo">TODO: the Loop</p>
</main>
<?php wp_footer(); ?>
</body>
</html>
