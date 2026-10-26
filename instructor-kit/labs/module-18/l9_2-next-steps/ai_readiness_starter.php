<?php
/**
 * ai_readiness_starter.php: what this site can do with AI today, for a client meeting (Session 18, Lesson 9.2, lab B)
 * state: after:lesson_30
 * expect: A text model available: TODO
 *
 * Five honest lines before anyone promises an AI feature (Lesson 9.2, "AI in Core, as It Really Is"), and a
 * helper that asks a model only when one can answer, and otherwise gives the shop's own fallback. Nothing is
 * installed or saved. From your project folder:
 *     cp labs/module-18/l9_2-next-steps/ai_readiness_starter.php wordpress/
 *     wp eval-file --use-include ai_readiness_starter.php
 * Do TODOs 1 to 4, run again, compare with "Expected when done".
 * When you are done: rm wordpress/ai_readiness_starter.php
 */

/**
 * A model's one-line answer when a model is available, else the fallback. Never an error on the page.
 *
 * @param string $question The question.
 * @param string $fallback What the page shows without a model.
 */
function pagesco_lab_ask( string $question, string $fallback ): string {
	// TODO 1: three guards, in this order, each returning $fallback: the function wp_ai_client_prompt does not
	// exist (WordPress 6.9); the prompt's is_supported_for_text_generation() says no; generate_text() returned
	// a WP_Error. Only then return the model's text, through sanitize_text_field() (model output is input).
	return 'TODO';
}

// TODO 2: the connectors whose 'type' is 'ai_provider' (array_filter() on wp_get_connectors()), and of those the
// ones whose plugin is active (each connector's ['plugin']['is_active'] is a function: call it).
$pagesco_providers = array();
$pagesco_active    = array();

printf( "AI client in this WordPress: %s\n", function_exists( 'wp_ai_client_prompt' ) ? 'yes' : 'no' );
printf( "AI allowed on this site: %s\n", wp_supports_ai() ? 'yes' : 'no' );
printf( "AI providers listed: %s (active: %d)\n", implode( ', ', array_keys( $pagesco_providers ) ), count( $pagesco_active ) );
// TODO 3: ask a prompt builder for 'Hello' whether a model supports text generation; print yes or no.
echo "A text model available: TODO\n";
printf( "Answer: %s\n", pagesco_lab_ask( 'In one sentence, why read Dune?', 'Ask us at the counter about Dune.' ) );

// The client's "no AI" policy for one request: the wp_supports_ai filter. Nothing may break.
// TODO 4: add_filter() 'wp_supports_ai' with '__return_false' here (and the remove_filter() below stays).
printf( "With AI switched off: allowed %s, answer: %s\n", wp_supports_ai() ? 'yes' : 'no', pagesco_lab_ask( 'In one sentence, why read Dune?', 'Ask us at the counter about Dune.' ) );
remove_filter( 'wp_supports_ai', '__return_false' );

// Expected when done (ai_readiness_solution.php, the course site after Lesson 9.1, no AI provider set up):
// AI client in this WordPress: yes
// AI allowed on this site: yes
// AI providers listed: anthropic, google, openai (active: 0)
// A text model available: no
// Answer: Ask us at the counter about Dune.
// With AI switched off: allowed no, answer: Ask us at the counter about Dune.
