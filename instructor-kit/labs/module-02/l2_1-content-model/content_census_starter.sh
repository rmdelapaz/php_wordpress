# content_census_starter.sh: what is on your site, counted the way Lesson 2.1 sees it (Session 2, Lesson 2.1, lab A)
# state: fresh
# expect: Draft pages: TODO
#
# Every line is one WP-CLI command inside "$( )": the shell runs it and puts its answer into the echo. The script
# runs in the WP-CLI container, where wp needs no shortcut. From your project folder:
#     cp labs/module-02/l2_1-content-model/content_census_starter.sh wordpress/
#     docker compose run --rm wpcli sh content_census_starter.sh
# Replace each TODO with the command its comment describes (try it alone first: wp help post list), run the
# script again, and compare with "Expected when done". Run it BEFORE you start the lesson project (afterwards
# the counts grow). When you are done: rm wordpress/content_census_starter.sh

echo "== Pages & Co. content census =="
echo "Post types: $(wp post-type list --format=count)"                  # done for you
# TODO 1: the number of PUBLISHED posts of type post (wp post list with --post_type, --post_status, --format=count)
echo "Published posts: TODO"
# TODO 2: the number of pages in ANY status (what does wp post list count when you leave --post_status out?)
echo "Pages, any status: TODO"
# TODO 3: the number of draft pages
echo "Draft pages: TODO"
# TODO 4: the names of the categories, one per line (wp term list category --field=...)
echo "Categories: TODO"
# TODO 5: what the home page shows: the option behind Settings > Reading, "Your homepage displays"
echo "Home page shows: TODO"
# TODO 6: how many capabilities the editor role has (wp cap list ... --format=count)
echo "Editor capabilities: TODO"
# TODO 7: the block types in post 1, counted: its post_content (wp post get 1 --field=...), then
#         | grep -o '<!-- wp:[a-z/-]*' | sort | uniq -c
echo "Blocks in post 1: TODO"

# Expected when done (content_census_solution.sh, a fresh course site):
# == Pages & Co. content census ==
# Post types: 16
# Published posts: 1
# Pages, any status: 2
# Draft pages: 1
# Categories: Uncategorized
# Home page shows: posts
# Editor capabilities: 34
# Blocks in post 1:
#       1 <!-- wp:paragraph
