"use strict";
/**
 * Blog Filter Module
 * Handles search, topic filtering, and status filtering for blog post listings
 * Uses the reusable ListFilter class
 */
import ListFilter from '../../static/js/listFilter.js';

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ListFilter({
            searchInputId: 'searchInput',
            filters: [
                { id: 'topicFilter', type: 'select', param: 'topic' },
                { id: 'statusFilter', type: 'select', param: 'status' }
            ]
        });
    });
} else {
    new ListFilter({
        searchInputId: 'searchInput',
        filters: [
            { id: 'topicFilter', type: 'select', param: 'topic' },
            { id: 'statusFilter', type: 'select', param: 'status' }
        ]
    });
}
