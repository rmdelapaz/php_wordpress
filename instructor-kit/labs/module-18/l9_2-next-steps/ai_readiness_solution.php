<?php
/**
 * ai_readiness_solution.php: what this site can do with AI today, for a client meeting (Session 18, Lesson 9.2, lab B)
 * state: after:lesson_30
 * expect: A text model available: no
 * expect: Answer: Ask us at the counter about Dune.
 *
 * The reference for ai_readiness_starter.php. Five honest lines before anyone promises an AI feature, and a
 * helper that asks a model only when one can answer, and otherwise gives the shop's own fallback.
 */

/**
 * A model's one-line answer when a model is available, else the fallback. Never an error on the page.
 *
 * @param string $question The question.
 * @param string $fallback What the page shows without a model.
 */
function pagesco_lab_ask( string $question, string $fallback ): string {
	if ( ! function_exists( 'wp_ai_client_prompt' ) ) {   // WordPress 6.9: no AI client at all
		return $fallback;
	}
	$pagesco_prompt = wp_ai_client_prompt( $question );
	if ( ! $pagesco_prompt->is_supported_for_text_generation() ) {   // no provider, no key, or AI switched off
		return $fallback;
	}
	$pagesco_text = $pagesco_prompt->generate_text();

	// Model output is input from outside: plain text only.
	return is_wp_error( $pagesco_text ) ? $fallback : sanitize_text_field( $pagesco_text );
}

$pagesco_providers = array_filter( wp_get_connectors(), fn( $connector ) => 'ai_provider' === $connector['type'] );
$pagesco_active    = array_filter( $pagesco_providers, fn( $connector ) => $connector['plugin']['is_active']() );

printf( "AI client in this WordPress: %s\n", function_exists( 'wp_ai_client_prompt' ) ? 'yes' : 'no' );
printf( "AI allowed on this site: %s\n", wp_supports_ai() ? 'yes' : 'no' );
printf( "AI providers listed: %s (active: %d)\n", implode( ', ', array_keys( $pagesco_providers ) ), count( $pagesco_active ) );
printf( "A text model available: %s\n", wp_ai_client_prompt( 'Hello' )->is_supported_for_text_generation() ? 'yes' : 'no' );
printf( "Answer: %s\n", pagesco_lab_ask( 'In one sentence, why read Dune?', 'Ask us at the counter about Dune.' ) );

// The client's "no AI" policy for one request: the wp_supports_ai filter. Nothing breaks.
add_filter( 'wp_supports_ai', '__return_false' );
printf( "With AI switched off: allowed %s, answer: %s\n", wp_supports_ai() ? 'yes' : 'no', pagesco_lab_ask( 'In one sentence, why read Dune?', 'Ask us at the counter about Dune.' ) );
remove_filter( 'wp_supports_ai', '__return_false' );
