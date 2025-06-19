<?php
/**
 * Plugin Name: TSB Dynamic Content Loader
 * Description: Custom Elementor widget to load dynamic HTML from API.
 * Version: 1.0
 * Author: TSB
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Hook into Elementor
add_action('elementor/widgets/register', function($widgets_manager) {
    require_once __DIR__ . '/widgets/tsb-curt-widget.php';
    $widgets_manager->register( new \TSB_Elementor_Curt_Widget() );
});
