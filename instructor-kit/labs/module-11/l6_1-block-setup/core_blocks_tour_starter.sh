# core_blocks_tour_starter.sh: WordPress's own blocks, built the way yours are (Session 11, Lesson 6.1, lab B)
# state: after:lesson_18
# expect: 115
# expect: TODO
#
# Core registers its blocks exactly as Lesson 6.1 registers the Book Card: a block.json per block and one PHP
# manifest of all of them. Five questions about wp-includes/blocks/, from the WP-CLI container. From your project
# folder:
#     cp labs/module-11/l6_1-block-setup/core_blocks_tour_starter.sh wordpress/
#     docker compose run --rm wpcli sh core_blocks_tour_starter.sh
# Replace each echo "TODO" with the command its comment describes, run again, compare with "Expected when done".
# When you are done: rm wordpress/core_blocks_tour_starter.sh

echo "1. block.json files in wp-includes/blocks:"
find wp-includes/blocks -name block.json | wc -l          # done for you

echo "2. blocks in core's manifest (blocks-json.php, the same idea as your blocks-manifest.php):"
# TODO 2: count the manifest's top-level keys: the lines that start with ONE tab and a quote (grep -c with a
# real tab in the pattern, "^	'").
echo "TODO"

echo "3. apiVersion of every core block:"
# TODO 3: grep -ho the "apiVersion": N text out of every wp-includes/blocks/*/block.json, then sort | uniq -c.
echo "TODO"

echo "4. core/quote's folder (where is its JavaScript?):"
# TODO 4: list wp-includes/blocks/quote. (Core's editor JavaScript for ALL its blocks is one bundle,
# wp-includes/js/dist/block-library.js: no per-block index.js.)
echo "TODO"

echo "5. registered block types without a block.json:"
# TODO 5: one wp eval: the names in every block.json (glob() + json_decode()) against the keys of
# WP_Block_Type_Registry::get_instance()->get_all_registered(); print array_diff() of the two.
echo "TODO"

# Expected when done (core_blocks_tour_solution.sh):
# 1. block.json files in wp-includes/blocks:
# 115
# 2. blocks in core's manifest (blocks-json.php, the same idea as your blocks-manifest.php):
# 115
# 3. apiVersion of every core block:
#     115 "apiVersion": 3
# 4. core/quote's folder (where is its JavaScript?):
# block.json         style-rtl.css      style-rtl.min.css  style.css          style.min.css      theme-rtl.css      theme-rtl.min.css  theme.css          theme.min.css
# 5. registered block types without a block.json:
# core/post-comments
