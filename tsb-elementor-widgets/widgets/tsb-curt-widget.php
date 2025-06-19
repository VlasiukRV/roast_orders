<?php
if ( ! defined( 'ABSPATH' ) ) exit;

use Elementor\Widget_Base;
use Elementor\Controls_Manager;

class TSB_Elementor_Curt_Widget extends Widget_Base {

    public function get_name() {
        return 'tsb_curt';
    }

    public function get_title() {
        return __('TSB Curt', 'tsb-curt');
    }

    public function get_icon() {
        return 'eicon-code';
    }

    public function get_categories() {
        return ['general'];
    }

    protected function render() {
        ?>
        <div id="tsb-curt-container">
            <!-- Dynamic content will be loaded here -->
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', function () {
                function loadDynamicContent() {
                    fetch('/api/get-order-form')
                        .then(response => response.text())
                        .then(html => {
                            const container = document.getElementById('tsb-curt-container');
                            container.innerHTML = html;

                            const scripts = container.querySelectorAll('script');
                            scripts.forEach(script => {
                                const newScript = document.createElement('script');

                                if (script.src) {
                                    if (!document.querySelector(`script[src="${script.src}"]`)) {
                                        newScript.src = script.src;
                                    }
                                } else {
                                    newScript.textContent = script.textContent;
                                }

                                document.body.appendChild(newScript);
                            });
                        })
                        .catch(error => {
                            const container = document.getElementById('tsb-curt-container');
                            container.innerHTML = '<p>Error loading dynamic content</p>';
                            console.error('Error loading dynamic content:', error);
                        });
                }

                loadDynamicContent();
            });
        </script>

        <?php
    }

    protected function _content_template() {}
}
