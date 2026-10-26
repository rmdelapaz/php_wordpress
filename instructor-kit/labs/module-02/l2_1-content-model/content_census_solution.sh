# content_census_solution.sh: the instructor's reference for content_census_starter.sh (Session 2, Lesson 2.1, lab A)
# state: fresh
# expect: Draft pages: 1
# expect: Editor capabilities: 34

echo "== Pages & Co. content census =="
echo "Post types: $(wp post-type list --format=count)"
echo "Published posts: $(wp post list --post_type=post --post_status=publish --format=count)"
echo "Pages, any status: $(wp post list --post_type=page --format=count)"
echo "Draft pages: $(wp post list --post_type=page --post_status=draft --format=count)"
echo "Categories: $(wp term list category --field=name)"
echo "Home page shows: $(wp option get show_on_front)"
echo "Editor capabilities: $(wp cap list editor --format=count)"
echo "Blocks in post 1:"
wp post get 1 --field=post_content | grep -o '<!-- wp:[a-z/-]*' | sort | uniq -c
