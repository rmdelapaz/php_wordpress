// Batch Update Script for Module 1 HTML Files
// This script provides the template and structure for updating all Module 1 lesson files

const module1Lessons = {
    session1: {
        title: "Session 1: Introduction to Web Development & Setup",
        lessons: [
            { file: "course_introduction.html", title: "Course Introduction", completed: true },
            { file: "how_web_works.html", title: "How the Web Works", completed: true },
            { file: "development_environment.html", title: "Development Environment", completed: true },
            { file: "first_html_page.html", title: "Your First HTML Page", completed: true },
            { file: "homework_setup.html", title: "Homework: Setup" }
        ]
    },
    session2: {
        title: "Session 2: HTML Fundamentals",
        lessons: [
            { file: "html_structure_syntax.html", title: "HTML Structure & Syntax", completed: true },
            { file: "essential_html_tags.html", title: "Essential HTML Tags" },
            { file: "html_forms_inputs.html", title: "Forms & Inputs" },
            { file: "html_validation_practices.html", title: "Validation & Best Practices" },
            { file: "homework_html_profile.html", title: "Homework: Profile Page" }
        ]
    },
    session3: {
        title: "Session 3: CSS Basics",
        lessons: [
            { file: "introduction_to_css.html", title: "Introduction to CSS" },
            { file: "css_syntax_and_selectors.html", title: "CSS Syntax and Selectors" },
            { file: "css_implementation_methods.html", title: "CSS Implementation Methods" },
            { file: "css_colors_fonts_text.html", title: "Colors, Fonts, and Text" },
            { file: "css_box_model.html", title: "The CSS Box Model" },
            { file: "homework_css_profile.html", title: "Homework: Style Your Profile" }
        ]
    },
    session4: {
        title: "Session 4: CSS Layout & Responsive Design",
        lessons: [
            { file: "css_layout_tech.html", title: "CSS Layout Techniques" },
            { file: "responsive_design.html", title: "Responsive Design" },
            { file: "media_queries.html", title: "Media Queries" },
            { file: "mobile_first.html", title: "Mobile-First Approach" },
            { file: "homework_responsive_profile.html", title: "Homework: Responsive Profile" }
        ]
    },
    session5: {
        title: "Session 5: CSS Frameworks & Best Practices",
        lessons: [
            { file: "bootstrap.html", title: "Introduction to Bootstrap" },
            { file: "bootstrap_grid.html", title: "Bootstrap Grid System" },
            { file: "bootstrap_components.html", title: "Bootstrap Components" },
            { file: "bootstrap_utilities.html", title: "Bootstrap Utilities" },
            { file: "css_organization_best_practices.html", title: "CSS Organization" },
            { file: "css_preprocessors.html", title: "CSS Preprocessors" },
            { file: "homework_bootstrap_profile.html", title: "Homework: Bootstrap Profile" }
        ]
    },
    session6: {
        title: "Session 6: JavaScript Fundamentals",
        lessons: [
            { file: "js_intro.html", title: "Introduction to JavaScript" },
            { file: "js_syntax_fundamentals.html", title: "JavaScript Syntax" },
            { file: "js_operators_and_expressions.html", title: "Operators and Expressions" },
            { file: "js_control_flow.html", title: "Control Flow" },
            { file: "js_functions_and_scope.html", title: "Functions and Scope" },
            { file: "homework_simple_js_programs.html", title: "Homework: Simple Programs" }
        ]
    },
    session7: {
        title: "Session 7: DOM Manipulation",
        lessons: [
            { file: "understanding_dom.html", title: "Understanding the DOM" },
            { file: "dom_selection_manipulation.html", title: "DOM Selection & Manipulation" },
            { file: "event_handling.html", title: "Event Handling" },
            { file: "creating_removing_elements.html", title: "Creating & Removing Elements" },
            { file: "form_validation.html", title: "Form Validation" },
            { file: "homework_interactive.html", title: "Homework: Add Interactivity" }
        ]
    },
    session8: {
        title: "Session 8: Modern JavaScript & jQuery",
        lessons: [
            { file: "es6_overview.html", title: "ES6+ Features Overview" },
            { file: "jquery_intro.html", title: "Introduction to jQuery" },
            { file: "jquery_dom_manipulation.html", title: "jQuery DOM Manipulation" },
            { file: "jquery_animations_and_effects.html", title: "jQuery Animations" },
            { file: "jquery_ajax.html", title: "AJAX with jQuery" },
            { file: "homework_jquery_refactor.html", title: "Homework: jQuery Refactor" }
        ]
    },
    session9: {
        title: "Session 9: Introduction to PHP",
        lessons: [
            { file: "php_and_wordpress.html", title: "PHP and WordPress" },
            { file: "php_setup_xampp_mamp.html", title: "Setting up XAMPP/MAMP" },
            { file: "php_syntax.html", title: "PHP Syntax" },
            { file: "php_variables_data_and_operators.html", title: "Variables and Operators" },
            { file: "php_includes.html", title: "PHP Includes" },
            { file: "homework_simple_php.html", title: "Homework: Simple PHP" }
        ]
    },
    session10: {
        title: "Session 10: Mini-Project",
        lessons: [
            { file: "planning_website.html", title: "Planning a Website" },
            { file: "creating_layout.html", title: "Creating Layout" },
            { file: "adding_interactivity_with_js.html", title: "Adding Interactivity" },
            { file: "php_header_footer.html", title: "PHP Header & Footer" },
            { file: "project_static_site.html", title: "Final Project: Static Site" }
        ]
    }
};

// Function to get lesson navigation
function getLessonNavigation(sessionKey, lessonIndex) {
    const sessions = Object.keys(module1Lessons);
    const currentSession = module1Lessons[sessionKey];
    const lessons = currentSession.lessons;
    
    let prevLesson = null;
    let nextLesson = null;
    
    // Previous lesson
    if (lessonIndex > 0) {
        prevLesson = lessons[lessonIndex - 1];
    } else if (sessionKey !== 'session1') {
        // Get last lesson from previous session
        const prevSessionIndex = sessions.indexOf(sessionKey) - 1;
        const prevSession = module1Lessons[sessions[prevSessionIndex]];
        prevLesson = prevSession.lessons[prevSession.lessons.length - 1];
    }
    
    // Next lesson
    if (lessonIndex < lessons.length - 1) {
        nextLesson = lessons[lessonIndex + 1];
    } else if (sessionKey !== 'session10') {
        // Get first lesson from next session
        const nextSessionIndex = sessions.indexOf(sessionKey) + 1;
        const nextSession = module1Lessons[sessions[nextSessionIndex]];
        nextLesson = nextSession.lessons[0];
    }
    
    return { prevLesson, nextLesson };
}

// HTML Template Generator
function generateHTMLTemplate(sessionKey, lessonIndex, lessonData) {
    const session = module1Lessons[sessionKey];
    const { prevLesson, nextLesson } = getLessonNavigation(sessionKey, lessonIndex);
    
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>${lessonData.title} - PHP WordPress Course</title>
    <meta name="description" content="${lessonData.description || 'Learn ' + lessonData.title + ' in this comprehensive lesson from the PHP WordPress Development course.'}">
    <meta name="keywords" content="${lessonData.keywords || 'PHP, WordPress, web development, ' + lessonData.title}">
    <meta name="author" content="PHP WordPress Course">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/favicon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
    <!-- Skip to main content -->
    <a href="#main-content" class="sr-only">Skip to main content</a>
    
    <div class="page-wrapper">
        ${generateHeader()}
        ${generateProgressBar()}
        ${generateBreadcrumb(lessonData.title)}
        
        <!-- Main Content -->
        <main id="main-content" class="main-content" role="main">
            <div class="container">
                <div class="content-with-sidebar">
                    ${generateSidebar(sessionKey, lessonIndex)}
                    
                    <!-- Main Lesson Content -->
                    <article class="lesson-content">
                        <header class="lesson-header">
                            <h1>${lessonData.title}</h1>
                            <div class="lesson-meta">
                                <div class="lesson-meta-item">
                                    <svg width="20" height="20" fill="currentColor">
                                        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                    </svg>
                                    <span>Duration: ${lessonData.duration || '30-45 minutes'}</span>
                                </div>
                                <div class="lesson-meta-item">
                                    <svg width="20" height="20" fill="currentColor">
                                        <path d="M12 14l9-5-9-5-9 5 9 5z"/>
                                    </svg>
                                    <span>Module 1, ${session.title.split(':')[0]}</span>
                                </div>
                            </div>
                        </header>

                        ${generateLessonContent(lessonData)}
                        
                        ${generateLessonNavigation(prevLesson, nextLesson)}
                    </article>
                </div>
            </div>
        </main>

        ${generateFooter(sessionKey, lessonIndex)}
    </div>

    <!-- Back to Top -->
    <button id="back-to-top" class="back-to-top" aria-label="Back to top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 19V5M12 5l-7 7M12 5l7 7"/>
        </svg>
    </button>

    <!-- JavaScript -->
    <script src="/assets/js/navigation.js"></script>
    <script src="/assets/js/site-config.js"></script>
</body>
</html>`;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { module1Lessons, generateHTMLTemplate };
}