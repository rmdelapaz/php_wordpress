<?php
/**
 * debug_card_report.php: a report of the Book Cards in some stored content, with three bugs (Session 12, Lesson 6.2, find-the-bug handout)
 * state: after:lesson_19
 * expect-error: Warning, Deprecated
 *
 * A colleague wants one line per Book Card: its title, its heading level and how long its HTML is. The content
 * below is what the editor stores for two cards of Lesson 6.2's block (the second one at the default level).
 * From your project folder:
 *     cp labs/module-12/l6_2-static-blocks/debug_card_report.php wordpress/
 *     wp eval-file --use-include debug_card_report.php
 * Two bugs announce themselves with Warnings (one brings a Deprecated along; read each message from the left:
 * level, message, file, line). The third is SILENT: no message, just a wrong answer for the second card.
 * Find all three, fix them one at a time, run again after each fix. When you are done: rm wordpress/debug_card_report.php
 */
$pagesco_content = '<!-- wp:pagesco/book-card {"headingLevel":2} -->
<div class="wp-block-pagesco-book-card"><h2 class="wp-block-pagesco-book-card__title">Dune</h2><p class="wp-block-pagesco-book-card__author">Frank Herbert</p></div>
<!-- /wp:pagesco/book-card -->

<!-- wp:pagesco/book-card -->
<div class="wp-block-pagesco-book-card"><h3 class="wp-block-pagesco-book-card__title">Emma</h3><p class="wp-block-pagesco-book-card__author">Jane Austen</p></div>
<!-- /wp:pagesco/book-card -->';

foreach ( parse_blocks( $pagesco_content ) as $pagesco_block ) {
	if ( 'pagesco/book-card' !== $pagesco_block['blockName'] ) {
		continue;
	}
	$pagesco_title = $pagesco_block['attrs']['title'];
	$pagesco_level = $pagesco_block['attrs']['headingLevel'] ?? 2;
	$pagesco_size  = strlen( $pagesco_block['innerHtml'] );

	printf( "%s: h%d, %d characters of HTML\n", $pagesco_title, $pagesco_level, $pagesco_size );
}
