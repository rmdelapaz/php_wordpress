<?php
/**
 * The header (done for you: it prints what functions.php registers).
 *
 * @package pagesco-lab-corner
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
<header class="corner-header">
	<p class="corner-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php bloginfo( 'name' ); ?></a></p>
	<?php
	if ( has_nav_menu( 'corner' ) ) {
		wp_nav_menu(
			array(
				'theme_location' => 'corner',
				'container'      => 'nav',
				'depth'          => 1,
			)
		);
	}
	get_search_form();
	?>
</header>
<main id="main">
