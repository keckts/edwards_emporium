"use strict";
/**
 * Generic List Filter Module
 * Reusable filter handling for list views with search and select/toggle filters
 */
class ListFilter {
    constructor(config = {}) {
        this.searchTimeout = null;
        this.DEBOUNCE_DELAY = config.debounceDelay || 500; // milliseconds
        this.searchInputId = config.searchInputId || 'searchInput';
        this.filterElements = config.filters || [];
        this.elements = this.getElements();
        this.init();
    }

    /**
     * Get DOM elements
     */
    getElements() {
        const searchInput = document.getElementById(this.searchInputId);

        if (!searchInput) {
            console.warn(`Search input with id '${this.searchInputId}' not found`);
        }

        const filters = {};
        for (const filter of this.filterElements) {
            const element = document.getElementById(filter.id);
            if (element) {
                filters[filter.id] = { element, type: filter.type, param: filter.param };
            } else {
                console.warn(`Filter element with id '${filter.id}' not found`);
            }
        }

        return { searchInput, filters };
    }

    /**
     * Initialize event listeners
     */
    init() {
        // Search input - debounced update
        if (this.elements.searchInput) {
            this.elements.searchInput.addEventListener('input', () => this.debouncedSearch());
        }

        // Filter elements - immediate update
        for (const [id, filter] of Object.entries(this.elements.filters)) {
            filter.element.addEventListener('change', () => this.updateFilters());
        }
    }

    /**
     * Debounced search to avoid excessive requests
     */
    debouncedSearch() {
        if (this.searchTimeout !== null) {
            clearTimeout(this.searchTimeout);
        }
        this.searchTimeout = window.setTimeout(() => {
            this.updateFilters();
        }, this.DEBOUNCE_DELAY);
    }

    /**
     * Update URL parameters and reload page with filters
     */
    updateFilters() {
        const params = new URLSearchParams(window.location.search);

        // Handle search parameter
        if (this.elements.searchInput) {
            const searchValue = this.elements.searchInput.value.trim();
            if (searchValue) {
                params.set('search', searchValue);
            } else {
                params.delete('search');
            }
        }

        // Handle filter parameters
        for (const [id, filter] of Object.entries(this.elements.filters)) {
            const param = filter.param;

            if (filter.type === 'select') {
                const value = filter.element.value;
                if (value) {
                    params.set(param, value);
                } else {
                    params.delete(param);
                }
            } else if (filter.type === 'toggle') {
                if (filter.element.checked) {
                    params.set(param, 'true');
                } else {
                    params.delete(param);
                }
            }
        }

        // Reset to page 1 when filters change
        params.delete('page');

        // Update URL and reload
        window.location.search = params.toString();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ListFilter;
}
