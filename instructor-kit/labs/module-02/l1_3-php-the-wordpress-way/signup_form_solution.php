<?php
/**
 * signup_form_solution.php: the instructor's reference for signup_form_starter.php (Session 2, Lesson 1.3, lab A)
 * state: fresh
 * expect: name:  string(18) "Siobhan O'Neil VIP"
 * expect: link:  <a href="">Siobhan O&#039;Neil VIP</a>
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
$pagesco_name  = sanitize_text_field( wp_unslash( $pagesco_post['name'] ) );
$pagesco_email = sanitize_email( wp_unslash( $pagesco_post['email'] ) );
$pagesco_seats = absint( $pagesco_post['seats'] );
$pagesco_shelf = in_array( $pagesco_post['shelf'], array( 'fiction', 'classics', 'children' ), true ) ? $pagesco_post['shelf'] : 'fiction';

echo 'name:  ';
var_dump( $pagesco_name );
echo 'email: ', $pagesco_email, ' (valid: ', is_email( $pagesco_email ) ? 'yes' : 'no', ")\n";
echo 'seats: ', $pagesco_seats, "\n";
echo 'shelf: ', $pagesco_shelf, "\n";

// 2. Escape late, for the place each value is printed into.
echo 'field: <input name="name" value="' . esc_attr( $pagesco_name ) . '">', "\n";
echo 'link:  <a href="' . esc_url( wp_unslash( $pagesco_post['website'] ) ) . '">' . esc_html( $pagesco_name ) . '</a>', "\n";
