#!/usr/bin/env node

/**
 * Batch Update Script for Module 1 HTML Files
 * This script updates all Module 1 lesson files to use the new template structure
 */

const fs = require('fs');
const path = require('path');

// Module 1 lesson structure
const module1Structure = {
    session1: {
        title: "Introduction to Web Development & Setup",
        lessons: [
            { file: "course_introduction.html", title: "Course Introduction and Expectations", duration: "30 minutes", completed: true },
            { file: "how_web_works.html", title: "How the Web Works: Servers, Browsers, HTTP", duration: "45 minutes", completed: true },
            { file: "development_environment.html", title: "Setting Up Your Development Environment", duration: "60 minutes", completed: true },
            { file: "first_html_page.html", title: "Creating Your First HTML Page", duration: "45 minutes", completed: true },
            { file: "homework_setup.html", title: "Homework: Setup GitHub and Docker", duration: "30 minutes" }
        ]
    },
    session2: {
        title: "HTML Fundamentals", 
        lessons: [
            { file: "html_structure_syntax.html", title: "HTML Document Structure and Syntax", duration: "45 minutes", completed: true },
            { file: "essential_html_tags.html", title: "Essential HTML Tags", duration: "60 minutes" },
            { file: "html_forms_inputs.html", title: "HTML Forms and Inputs", duration: "45 minutes" },
            { file: "html_validation_practices.html", title: "HTML Validation and Best Practices", duration: "30 minutes" },
            { file: "homework_html_profile.html", title: "Homework: Create a Personal Profile Page", duration: "60 minutes" }
        ]
    },
    session3: {
        title: "CSS Basics",
        lessons: [
            { file: "introduction_to_css.html", title: "Introduction to CSS and Its Purpose", duration: "45 minutes" },
            { file: "css_syntax_and_selectors.html", title: "CSS Syntax and Selectors", duration: "45 minutes" },
            { file: "css_implementation_methods.html", title: "Inline, Internal, and External CSS", duration: "30 minutes" },
            { file: "css_colors_fonts_text.html", title: "Working with Colors, Fonts, and Text", duration: "45 minutes" },
            { file: "css_box_model.html", title: "The CSS Box Model", duration: "45 minutes" },
            { file: "homework_css_profile.html", title: "Homework: Style Your Profile Page", duration: "60 minutes" }
        ]
    },
    session4: {
        title: "CSS Layout & Responsive Design",
        lessons: [
            { file: "css_layout_tech.html", title: "CSS Layout Techniques", duration: "60 minutes" },
            { file: "responsive_design.html", title: "Introduction to Responsive Design", duration: "45 minutes" },
            { file: "media_queries.html", title: "Media Queries", duration: "45 minutes" },
            { file: "mobile_first.html", title: "Mobile-First Approach", duration: "30 minutes" },
            { file: "homework_responsive_profile.html", title: "Homework: Make Your Profile Responsive", duration: "60 minutes" }
        ]
    },
    session5: {
        title: "CSS Frameworks & Best Practices",
        lessons: [
            { file: "bootstrap.html", title: "Introduction to Bootstrap", duration: "45 minutes" },
            { file: "bootstrap_grid.html", title: "Using Bootstrap Grid System", duration: "45 minutes" },
            { file: "bootstrap_components.html", title: "Bootstrap Components", duration: "45 minutes" },
            { file: "bootstrap_utilities.html", title: "Bootstrap Utilities", duration: "30 minutes" },
            { file: "css_organization_best_practices.html", title: "CSS Organization and Best Practices", duration: "30 minutes" },
            { file: "css_preprocessors.html", title: "CSS Preprocessors Overview (SASS/SCSS)", duration: "30 minutes" },
            { file: "homework_bootstrap_profile.html", title: "Homework: Recreate Profile with Bootstrap", duration: "60 minutes" }
        ]
    },
    session6: {
        title: "JavaScript Fundamentals",
        lessons: [
            { file: "js_intro.html", title: "Introduction to JavaScript", duration: "45 minutes" },
            { file: "js_syntax_fundamentals.html", title: "JavaScript Syntax, Variables, and Data Types", duration: "45 minutes" },
            { file: "js_operators_and_expressions.html", title: "Operators and Expressions", duration: "30 minutes" },
            { file: "js_control_flow.html", title: "Control Flow (Conditionals, Loops)", duration: "45 minutes" },
            { file: "js_functions_and_scope.html", title: "Functions and Scope", duration: "45 minutes" },
            { file: "homework_simple_js_programs.html", title: "Homework: Create Simple JavaScript Programs", duration: "60 minutes" }
        ]
    },
    session7: {
        title: "DOM Manipulation with JavaScript",
        lessons: [
            { file: "understanding_dom.html", title: "Understanding the Document Object Model (DOM)", duration: "45 minutes" },
            { file: "dom_selection_manipulation.html", title: "Selecting and Manipulating DOM Elements", duration: "45 minutes" },
            { file: "event_handling.html", title: "Event Handling", duration: "45 minutes" },
            { file: "creating_removing_elements.html", title: "Creating and Removing Elements", duration: "30 minutes" },
            { file: "form_validation.html", title: "Form Validation with JavaScript", duration: "45 minutes" },
            { file: "homework_interactive.html", title: "Homework: Add Interactivity to Your Page", duration: "60 minutes" }
        ]
    },
    session8: {
        title: "Modern JavaScript & jQuery",
        lessons: [
            { file: "es6_overview.html", title: "ES6+ Features Overview", duration: "45 minutes" },
            { file: "jquery_intro.html", title: "Introduction to jQuery", duration: "45 minutes" },
            { file: "jquery_dom_manipulation.html", title: "DOM Manipulation with jQuery", duration: "45 minutes" },
            { file: "jquery_animations_and_effects.html", title: "jQuery Animations and Effects", duration: "30 minutes" },
            { file: "jquery_ajax.html", title: "AJAX Basics with jQuery", duration: "45 minutes" },
            { file: "homework_jquery_refactor.html", title: "Homework: Refactor Your Code Using jQuery", duration: "60 minutes" }
        ]
    },
    session9: {
        title: "Introduction to PHP",
        lessons: [
            { file: "php_and_wordpress.html", title: "What is PHP and Why It's Important for WordPress", duration: "45 minutes" },
            { file: "php_setup_xampp_mamp.html", title: "Setting Up a Local Server (XAMPP/MAMP)", duration: "45 minutes" },
            { file: "php_syntax.html", title: "PHP Syntax and Basic Constructs", duration: "45 minutes" },
            { file: "php_variables_data_and_operators.html", title: "Variables, Data Types, and Operators", duration: "45 minutes" },
            { file: "php_includes.html", title: "Including Files and PHP in HTML", duration: "30 minutes" },
            { file: "homework_simple_php.html", title: "Homework: Create a Simple PHP Script", duration: "60 minutes" }
        ]
    },
    session10: {
        title: "Mini-Project: Static Website",
        lessons: [
            { file: "planning_website.html", title: "Planning a Multi-Page Website", duration: "45 minutes" },
            { file: "creating_layout.html", title: "Creating a Consistent Layout", duration: "60 minutes" },
            { file: "adding_interactivity_with_js.html", title: "Adding Interactivity with JavaScript", duration: "60 minutes" },
            { file: "php_header_footer.html", title: "Basic PHP Includes for Header and Footer", duration: "45 minutes" },
            { file: "project_static_site.html", title: "Final Project: 5-Page Static Website", duration: "180 minutes" }
        ]
    }
};

// Function to get navigation for a lesson
function getLessonNavigation(sessionKey, lessonIndex) {
    const sessions = Object.keys(module1Structure);
    const currentSession = module1Structure[sessionKey];
    const currentSessionIndex = sessions.indexOf(sessionKey);
    
    let prevLesson = null;
    let nextLesson = null;
    
    // Previous lesson
    if (lessonIndex > 0) {
        prevLesson = currentSession.lessons[lessonIndex - 1];
    } else if (currentSessionIndex > 0) {
        const prevSession = module1Structure[sessions[currentSessionIndex - 1]];
        prevLesson = prevSession.lessons[prevSession.lessons.length - 1];
    }
    
    // Next lesson 
    if (lessonIndex < currentSession.lessons.length - 1) {
        nextLesson = currentSession.lessons[lessonIndex + 1];
    } else if (currentSessionIndex < sessions.length - 1) {
        const nextSession = module1Structure[sessions[currentSessionIndex + 1]];
        nextLesson = nextSession.lessons[0];
    }
    
    return { prevLesson, nextLesson };
}

// Function to generate sidebar HTML
function generateSidebar(sessionKey, lessonIndex) {
    const session = module1Structure[sessionKey];
    const currentLesson = session.lessons[lessonIndex];
    
    let sidebarHTML = `
                    <!-- Sidebar -->
                    <aside class="sidebar">
                        <div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 1: ${session.title}</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Lessons</h4>`;
    
    session.lessons.forEach((lesson, index) => {
        const isActive = index === lessonIndex ? ' active' : '';
        sidebarHTML += `
                                <a href="/01module/${lesson.file}" class="sidebar-link${isActive}">${lesson.title}</a>`;
    });
    
    sidebarHTML += `
                            </div>
                        </div>
                    </aside>`;
    
    return sidebarHTML;
}

// Function to generate lesson navigation HTML
function generateLessonNav(prevLesson, nextLesson) {
    let navHTML = `
                        <!-- Lesson Navigation -->
                        <div class="lesson-navigation">`;
    
    if (prevLesson) {
        navHTML += `
                            <a href="/01module/${prevLesson.file}" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Previous</small><br>
                                    ${prevLesson.title}
                                </span>
                            </a>`;
    } else {
        navHTML += `
                            <a href="/module1.html" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Back to</small><br>
                                    Module 1 Overview
                                </span>
                            </a>`;
    }
    
    navHTML += `
                            
                            <button class="complete-lesson-btn">
                                Mark as Complete
                            </button>`;
    
    if (nextLesson) {
        navHTML += `
                            
                            <a href="/01module/${nextLesson.file}" class="lesson-nav-button next">
                                <span>
                                    <small>Next Lesson</small><br>
                                    ${nextLesson.title}
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>`;
    } else {
        navHTML += `
                            
                            <a href="/module2.html" class="lesson-nav-button next">
                                <span>
                                    <small>Next Module</small><br>
                                    Module 2: PHP Fundamentals
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010-1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>`;
    }
    
    navHTML += `
                        </div>`;
    
    return navHTML;
}

// Export functions for use in the update process
module.exports = {
    module1Structure,
    getLessonNavigation,
    generateSidebar,
    generateLessonNav
};