"use strict";
/**
 * Antique Filter Module
 * Handles search, type filtering, and sold item toggle for antique listings
 * Uses the reusable ListFilter class
 */
import ListFilter from './listFilter.js';

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ListFilter({
            searchInputId: 'searchInput',
            filters: [
                { id: 'typeFilter', type: 'select', param: 'type' },
                { id: 'showSoldToggle', type: 'toggle', param: 'show_sold' }
            ]
        });
    });
} else {
    new ListFilter({
        searchInputId: 'searchInput',
        filters: [
            { id: 'typeFilter', type: 'select', param: 'type' },
            { id: 'showSoldToggle', type: 'toggle', param: 'show_sold' }
        ]
    });
}