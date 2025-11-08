# Icon Usage Guide

## How to Add New SVG Icons to the Sidebar

Your `_icon.html` template provides a reusable way to add SVG icons throughout your site. Here's how to use it:

### Template Structure

The `_icon.html` template accepts two parameters:
- `svg`: The path/shape data of your icon (everything inside the `<svg>` tags)
- `hover` (optional): Set to `True` to enable hover effects

### Default Icon Settings

The template automatically applies:
- `xmlns="http://www.w3.org/2000/svg"`
- `fill="none"`
- `viewBox="0 0 24 24"`
- `stroke="currentColor"`
- `stroke-width="2"`
- `stroke-linecap="round"`
- `stroke-linejoin="round"`
- `class="icon inline-block w-6 h-6 my-1.5"`

### Steps to Add a New Icon

1. **Find your SVG** (e.g., from Heroicons, Feather Icons, etc.)

2. **Extract only the path/shape data** (everything between `<svg>` and `</svg>`)

3. **Add to base.html** using this format:

```django
<li>
  <a href="{% url 'your-url-name' %}" class="is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Tooltip Text">
    {% include 'theme/_icon.html' with svg="<path d='YOUR_PATH_DATA_HERE'>" hover=True %}
    <span class="is-drawer-close:hidden">Link Text</span>
  </a>
</li>
```

## Examples

### Example 1: Heart Icon (Wishlist)
```django
<li>
  <a href="{% url 'antiques:wishlist-list' %}">
    {% include 'theme/_icon.html' with svg="<path stroke-linecap='round' stroke-linejoin='round' d='M4.318 6.318a4.5 4.5 0 0 0 0 6.364L12 20.364l7.682-7.682a4.5 4.5 0 0 0-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 0 0-6.364 0z'>" hover=True %}
    <span>My Wishlists</span>
  </a>
</li>
```

### Example 2: Storefront Icon
```django
<li>
  <a href="#">
    {% include 'theme/_icon.html' with svg="<path stroke-linecap='round' stroke-linejoin='round' d='M13.5 21v-7.5a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 .75.75V21m-4.5 0H2.36m11.14 0h3.75m-16.5 0h.008v.008H2.36V21Zm0 0h.008v.008H2.36V21Zm16.5 0h.008v.008h-.008V21Zm0 0h.008v.008h-.008V21ZM6.75 21v-4.5m0 0a2.993 2.993 0 0 0-1.875-2.776 2.993 2.993 0 0 0-1.875 2.776m3.75 0a2.993 2.993 0 0 1 1.875-2.776 2.993 2.993 0 0 1 1.875 2.776M6.75 18h3.75a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-3.75a.75.75 0 0 0-.75.75v1.5c0 .414.336.75.75.75Z'>" hover=True %}
    <span>Storefront</span>
  </a>
</li>
```

### Example 3: Home Icon
```django
<li>
  <a href="{% url 'dashboard' %}">
    {% include 'theme/_icon.html' with svg="<path d='M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8'></path><path d='M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'></path>" hover=True %}
    <span>Dashboard</span>
  </a>
</li>
```

## Converting Full SVG to Template Format

If you have a full SVG like this:
```html
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5..." />
</svg>
```

**Extract only the inner content:**
```django
{% include 'theme/_icon.html' with svg="<path stroke-linecap='round' stroke-linejoin='round' d='M13.5 21v-7.5...'>" hover=True %}
```

## Tips

1. **Use single quotes inside the path data** to avoid conflicts with Django template double quotes
2. **Always use `hover=True`** in the sidebar for consistent hover effects
3. **Keep viewBox at `0 0 24 24`** for consistent sizing (this is set by default in `_icon.html`)
4. **Multiple paths**: You can include multiple `<path>` or `<circle>` elements in the `svg` parameter
5. **Icon sources**: Heroicons, Feather Icons, and Lucide are great sources for clean SVG icons

## Customizing Icons

If you need to customize an icon beyond the defaults, you can:

1. **Change size**: Modify the `w-6 h-6` classes in `_icon.html`
2. **Change color**: The icon inherits color from `currentColor`, so it matches the link color
3. **Add fill**: Change `fill="none"` to `fill="currentColor"` in `_icon.html` for filled icons

## Current Sidebar Icons

- Dashboard: Home icon
- Browse Antiques: Shopping cart icon
- My Wishlists: Heart icon (authenticated users only)
- Storefront: Shop/storefront icon
- Settings: Sliders icon (authenticated users only)
