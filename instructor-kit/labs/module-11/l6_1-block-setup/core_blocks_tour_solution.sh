# core_blocks_tour_solution.sh: WordPress's own blocks, built the way yours are (Session 11, Lesson 6.1, lab B, reference)
# state: after:lesson_18
# expect: 115
# expect: core/post-comments
#
# Core registers its blocks exactly as Lesson 6.1 registers the Book Card: a block.json per block and one PHP
# manifest of all of them. Five questions about wp-includes/blocks/, from the WP-CLI container.

echo "1. block.json files in wp-includes/blocks:"
find wp-includes/blocks -name block.json | wc -l
echo "2. blocks in core's manifest (blocks-json.php, the same idea as your blocks-manifest.php):"
grep -c "^	'" wp-includes/blocks/blocks-json.php
echo "3. apiVersion of every core block:"
grep -ho '"apiVersion": [0-9]' wp-includes/blocks/*/block.json | sort | uniq -c
echo "4. core/quote's folder (where is its JavaScript?):"
ls wp-includes/blocks/quote
echo "5. registered block types without a block.json:"
wp eval '$pagesco_json = array_map( fn( $pagesco_f ) => json_decode( file_get_contents( $pagesco_f ), true )["name"], glob( ABSPATH . WPINC . "/blocks/*/block.json" ) );
echo implode( ", ", array_diff( array_keys( WP_Block_Type_Registry::get_instance()->get_all_registered() ), $pagesco_json ) ), "\n";'
