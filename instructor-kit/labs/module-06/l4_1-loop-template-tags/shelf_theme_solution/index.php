<?php
/**
 * The only template of the Shelf lab theme (Session 6, Lesson 4.1, lab A: the reference solution).
 *
 * @package pagesco-lab-shelf
 */

if ( is_home() ) {
	$pagesco_lab_shelf_heading = __( 'Latest from the shop', 'pagesco-lab-shelf' );
} elseif ( is_category() ) {
	/* translators: %s: the category name. */
	$pagesco_lab_shelf_heading = sprintf( __( 'Shelf: %s', 'pagesco-lab-shelf' ), single_cat_title( '', false ) );
} elseif ( is_search() ) {
	/* translators: %s: the search terms. */
	$pagesco_lab_shelf_heading = sprintf( __( 'Found for: %s', 'pagesco-lab-shelf' ), get_search_query( false ) );
} elseif ( is_singular() ) {
	$pagesco_lab_shelf_heading = single_post_title( '', false );
} else {
	$pagesco_lab_shelf_heading = __( 'Archive', 'pagesco-lab-shelf' );
}
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
	<h1><?php echo esc_html( $pagesco_lab_shelf_heading ); ?></h1>
	<?php if ( have_posts() ) : ?>
		<ul>
			<?php
			while ( have_posts() ) {
				the_post();
				?>
				<li class="shelf-item">
					<?php the_title( '<a href="' . esc_url( get_permalink() ) . '" title="' . the_title_attribute( array( 'echo' => false ) ) . '">', '</a>' ); ?>
					· <?php echo esc_html( get_the_date( 'Y-m-d' ) ); ?>
					· <?php echo esc_html( get_the_author() ); ?>
				</li>
				<?php
			}
			?>
		</ul>
	<?php else : ?>
		<p class="shelf-empty"><?php esc_html_e( 'Nothing on this shelf.', 'pagesco-lab-shelf' ); ?></p>
	<?php endif; ?>
</main>
<?php wp_footer(); ?>
</body>
</html>
