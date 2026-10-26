<?php
/**
 * Pages & Co. Lab: TT4 Child functions (Session 5, Lesson 3.4, lab A: the starter).
 *
 * The reading corner wants Twenty Twenty-Four with four changes. Work through the TODOs (the first one is in
 * theme.json), and run test_tt4_child.sh after each. Twenty Twenty-Four is not Twenty Twenty-Five: open
 * wp-content/themes/twentytwentyfour/functions.php first and read what the parent does, and with which names.
 *
 * TODO 1 (theme.json): the shop's oxblood, #7a2e2e, in the place of Twenty Twenty-Four's orange accent-3
 *         (#d8613c). Keep every other color: copy the parent's whole palette (all ten slugs), change one value.
 *
 * TODO 2 (here): enqueue this child's style.css on wp_enqueue_scripts, in a function with the child's prefix
 *         pagesco_lab_tt4_child_ and the child's Version. Which parent handle does it depend on? Look in the
 *         parent's functions.php: is there one at all?
 *
 * TODO 3 (patterns/footer.php): it registers a NEW pattern instead of replacing the parent's footer. Give it the
 *         slug that makes it win (the parent's parts/footer.html shows which pattern it uses).
 *
 * TODO 4 (here): the reading corner wants only one of the parent's five block styles, the checkmark list.
 *         twentytwentyfour_block_styles() is pluggable (it is wrapped in function_exists()): define your own
 *         version here that registers only core/list "checkmark-list" (label: Checkmark; copy its inline_style
 *         from the parent, or leave the style out).
 *
 * @package pagesco-lab-tt4-child
 */
