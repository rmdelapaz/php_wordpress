<?php
/**
 * The header: the document head and the top of every page.
 *
 * @package pagesco-classic
 */

?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip-link screen-reader-text" href="#main"><?php esc_html_e( 'Skip to content', 'pagesco-classic' ); ?></a>
<header class="site-header">
	<p class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php bloginfo( 'name' ); ?></a></p>
	<?php if ( has_nav_menu( 'primary' ) ) : ?>
		<nav class="site-nav" aria-label="<?php esc_attr_e( 'Primary', 'pagesco-classic' ); ?>">
			<button type="button" class="menu-toggle" aria-controls="primary-menu" aria-expanded="false"><?php esc_html_e( 'Menu', 'pagesco-classic' ); ?></button>
			<?php
			wp_nav_menu(
				array(
					'theme_location' => 'primary',
					'menu_id'        => 'primary-menu',
					'container'      => false,
					'depth'          => 1,
				)
			);
			?>
		</nav>
	<?php endif; ?>
</header>
<main id="main" class="site-main">
