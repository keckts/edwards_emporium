/**
 * Antique Filter Module
 * Handles search, type filtering, and sold item toggle for antique listings
 */

interface FilterElements {
  searchInput: HTMLInputElement;
  typeFilter: HTMLSelectElement;
  showSoldToggle: HTMLInputElement;
}

class AntiqueFilter {
  private elements: FilterElements;
  private searchTimeout: number | null = null;
  private readonly DEBOUNCE_DELAY = 500; // milliseconds

  constructor() {
    this.elements = this.getElements();
    this.init();
  }

  /**
   * Get DOM elements
   */
  private getElements(): FilterElements {
    const searchInput = document.getElementById('searchInput') as HTMLInputElement;
    const typeFilter = document.getElementById('typeFilter') as HTMLSelectElement;
    const showSoldToggle = document.getElementById('showSoldToggle') as HTMLInputElement;

    if (!searchInput || !typeFilter || !showSoldToggle) {
      throw new Error('Required filter elements not found in DOM');
    }

    return { searchInput, typeFilter, showSoldToggle };
  }

  /**
   * Initialize event listeners
   */
  private init(): void {
    // Type filter - immediate update
    this.elements.typeFilter.addEventListener('change', () => this.updateFilters());

    // Sold toggle - immediate update
    this.elements.showSoldToggle.addEventListener('change', () => this.updateFilters());

    // Search input - debounced update
    this.elements.searchInput.addEventListener('input', () => this.debouncedSearch());
  }

  /**
   * Debounced search to avoid excessive requests
   */
  private debouncedSearch(): void {
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
  private updateFilters(): void {
    const params = new URLSearchParams(window.location.search);

    // Handle search parameter
    const searchValue = this.elements.searchInput.value.trim();
    if (searchValue) {
      params.set('search', searchValue);
    } else {
      params.delete('search');
    }

    // Handle type filter parameter
    const typeValue = this.elements.typeFilter.value;
    if (typeValue) {
      params.set('type', typeValue);
    } else {
      params.delete('type');
    }

    // Handle show sold parameter
    if (this.elements.showSoldToggle.checked) {
      params.set('show_sold', 'true');
    } else {
      params.delete('show_sold');
    }

    // Update URL and reload
    window.location.search = params.toString();
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new AntiqueFilter();
  });
} else {
  new AntiqueFilter();
}
