<?php
/**
 * signup_form_starter.php: sanitize early, escape late, on a book club sign-up form (Session 2, Lesson 1.3, lab A)
 * state: fresh
 * expect: email: TODO
 *
 * Lesson 1.3, "Sanitize Early, Escape Late", on data you have not seen yet. From your project folder:
 *     cp labs/module-02/l1_3-php-the-wordpress-way/signup_form_starter.php wordpress/
 *     wp eval-file --use-include signup_form_starter.php
 * Replace each 'TODO' with the WordPress function its comment names, run again after each one, and compare with
 * "Expected when done" at the end. When you are done: rm wordpress/signup_form_starter.php
 */
// The book club sign-up form, as WordPress hands it to your code: every quote already has a backslash
// (wp_magic_quotes(), Lesson 1.3). wp_slash() plays that part here, because no real form was sent.
$pagesco_post = wp_slash(
	array(
		'name'    => "  Siobhan O'Neil <b>VIP</b>\n ",
		'email'   => ' Siobhan.ONeil@Example.COM ',
		'seats'   => '-3',
		'shelf'   => 'poetry',
		'website' => 'javascript:alert(document.cookie)',
	)
);

// 1. Sanitize early: unslash first, then clean each field for what it should be.
$pagesco_name  = 'TODO'; // TODO 1: one line of plain text: sanitize_text_field( wp_unslash( ... ) )
$pagesco_email = 'TODO'; // TODO 2: sanitize_email(), also unslashed
$pagesco_seats = 'TODO'; // TODO 3: a non-negative whole number
$pagesco_shelf = 'TODO'; // TODO 4: VALIDATE: one of fiction, classics, children (in_array( ..., true )), else 'fiction'

echo 'name:  ';
var_dump( $pagesco_name );
// TODO 5: after the address, print whether it is valid: (valid: yes) or (valid: no), with is_email().
echo 'email: ', $pagesco_email, "\n";
echo 'seats: ', $pagesco_seats, "\n";
echo 'shelf: ', $pagesco_shelf, "\n";

// 2. Escape late, for the place each value is printed into.
// TODO 6: the name inside the value="..." attribute.
echo 'field: <input name="name" value="' . $pagesco_name . '">', "\n";
// TODO 7: the website as the link (unslashed, then the escaper for URLs), the name as the link text.
echo 'link:  <a href="TODO">' . $pagesco_name . '</a>', "\n";

// Expected when done (signup_form_solution.php, the course site):
// name:  string(18) "Siobhan O'Neil VIP"
// email: Siobhan.ONeil@Example.COM (valid: yes)
// seats: 3
// shelf: fiction
// field: <input name="name" value="Siobhan O&#039;Neil VIP">
// link:  <a href="">Siobhan O&#039;Neil VIP</a>
