<?php
/**
 * Pages & Co. Lab: Reading Corner functions (Session 7, Lesson 4.3, lab A: the starter).
 *
 * The templates are finished and already print a menu location called "corner", a widget area called
 * "corner-footer" and a search form. Right now the page has no <title>, an old-style search form, no CSS and no
 * script. Write one prefixed function per job (pagesco_lab_corner_...), each on the right hook, and run
 * test_corner_theme.sh after each:
 *
 * TODO 1 (after_setup_theme): let WordPress print the <title> (title-tag), and HTML5 markup for the search form.
 * TODO 2 (wp_enqueue_scripts): enqueue style.css with the handle pagesco-lab-corner-style and the theme's own
 *         Version (2.0.0, read it with wp_get_theme( get_template() )->get( 'Version' ), never typed), and
 *         assets/corner.js with the handle pagesco-lab-corner-script, the same version, deferred, in the footer.
 * TODO 3 (after_setup_theme): register the menu location "corner" (label: Reading corner menu).
 * TODO 4 (widgets_init): register the widget area with the id "corner-footer" (name: Reading corner footer),
 *         each widget wrapped in <section id="%1$s" class="widget %2$s">.
 *
 * @package pagesco-lab-corner
 */
