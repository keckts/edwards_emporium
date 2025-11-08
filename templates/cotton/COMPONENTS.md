# Django Cotton Components Library

A collection of reusable UI components built with Django Cotton, Tailwind CSS, Alpine.js, and HTMX.

## Table of Contents
1. [Toast Notifications](#toast-notifications) ⭐ NEW
2. [Card](#card)
3. [Gradient Button](#gradient-button)
4. [Alert](#alert)
5. [Badge](#badge)
6. [Modal](#modal)
7. [Input](#input)
8. [Navbar](#navbar)
9. [Accordion](#accordion)
10. [Loading Button](#loading-button)

---

## Toast Notifications

A beautiful toast notification system that automatically displays Django messages in the bottom-right corner with smooth animations.

**Requires:** Alpine.js

### Features
- Smooth slide-in/fade animations
- Auto-dismiss after 5 seconds (customizable)
- Multiple types: success, error, warning, info
- Automatic Django messages integration
- Manual dismiss button
- Programmatic JavaScript API

### Components

#### `<c-notifications />`
Main container that automatically displays Django messages as toasts.

**Usage in base.html:**
```html
<body>
    <c-notifications />
    <!-- rest of your content -->
</body>
```

#### `<c-toast />`
Individual toast notification.

**Props:**
- `type` - Toast type: 'success', 'error', 'warning', 'info' (default: 'info')
- `title` - Toast title (optional)
- `message` - Toast message (required)
- `duration` - Duration in ms before auto-dismiss (default: 5000)

### Usage Examples

**In Django Views:**
```python
from django.contrib import messages

messages.success(request, "Profile updated successfully!")
messages.error(request, "Something went wrong.")
messages.warning(request, "Please review your settings.")
messages.info(request, "Your session expires in 5 minutes.")
```

**Programmatically (JavaScript):**
```javascript
// Basic
showToast('success', 'Operation completed!');

// With title
showToast('error', 'Unable to save.', 'Error');

// Custom duration
showToast('info', 'Loading...', '', 3000);
```

**Manual Component:**
```html
<c-toast type="success" message="Your changes have been saved." />
<c-toast type="error" title="Error" message="Something went wrong." />
<c-toast type="warning" duration="10000">Custom message with slot</c-toast>
```

For full documentation, see `NOTIFICATION_SYSTEM.md`.

---

## Card

A flexible card component with optional image, title, subtitle, content, and action button.

### Props
- `title` - Card title (optional)
- `subtitle` - Card subtitle (optional)
- `image` - Image URL (optional)
- `button_text` - Text for the action button (optional)
- `button_url` - URL for the action button (default: '#')
- `class` - Additional CSS classes

### Usage
```html
<c-card
    title="Amazing Product"
    subtitle="New Arrival"
    image="/static/images/product.jpg"
    button_text="Learn More"
    button_url="/products/1"
    class="max-w-sm">
    This is an amazing product that will change your life!
</c-card>
```

---

## Gradient Button

A beautiful gradient button with customizable colors and hover effects.

### Props
- `text` - Button text (optional, can use slot)
- `href` - Link URL (default: '#')
- `gradient_from` - Starting gradient color (default: 'from-purple-400')
- `gradient_to` - Ending gradient color (default: 'to-pink-600')
- `class` - Additional CSS classes

### Usage
```html
<c-gradient_button
    text="Get Started"
    href="/signup"
    gradient_from="from-blue-500"
    gradient_to="to-green-500"
    class="shadow-lg hover:scale-105 transition-transform" />
```

---

## Alert

A notification component with different types (info, success, warning, error) and optional dismiss functionality.

**Requires:** Alpine.js for dismissible alerts

### Props
- `type` - Alert type: 'info', 'success', 'warning', 'error' (default: 'info')
- `title` - Alert title (optional)
- `dismissible` - Enable dismiss button (default: false)
- `class` - Additional CSS classes

### Usage
```html
<!-- Info Alert -->
<c-alert type="info" title="Information">
    This is an informational message.
</c-alert>

<!-- Success Alert with Dismiss -->
<c-alert type="success" title="Success!" dismissible="true">
    Your changes have been saved successfully!
</c-alert>

<!-- Warning Alert -->
<c-alert type="warning" title="Warning">
    Please review your settings before continuing.
</c-alert>

<!-- Error Alert -->
<c-alert type="error" title="Error">
    Something went wrong. Please try again.
</c-alert>
```

---

## Badge

A small status indicator or label with color variants.

### Props
- `text` - Badge text (optional, can use slot)
- `variant` - Color variant: 'success', 'error', 'warning', 'info', 'purple', or default gray
- `icon` - Show icon (default: false)
- `class` - Additional CSS classes

### Usage
```html
<c-badge text="New" variant="success" />
<c-badge text="In Progress" variant="info" icon="true" />
<c-badge text="Urgent" variant="error" />
<c-badge text="Beta" variant="purple" />
```

---

## Modal

A modal dialog with customizable content, powered by Alpine.js.

**Requires:** Alpine.js

### Props
- `trigger_text` - Text for the button that opens the modal (default: 'Open Modal')
- `title` - Modal title (default: 'Modal Title')
- `confirm_text` - Text for confirm button (optional, hides button if not provided)
- `class` - Additional CSS classes

### Usage
```html
<c-modal
    trigger_text="View Details"
    title="Product Information"
    confirm_text="Add to Cart">
    <p>This is the modal content. You can put anything here!</p>
    <ul class="list-disc list-inside mt-2">
        <li>Feature 1</li>
        <li>Feature 2</li>
        <li>Feature 3</li>
    </ul>
</c-modal>
```

---

## Input

A styled form input component with label, validation, and error states.

### Props
- `name` - Input name attribute (required)
- `label` - Input label (optional)
- `type` - Input type (default: 'text')
- `placeholder` - Placeholder text (optional)
- `value` - Default value (optional)
- `required` - Mark as required (default: false)
- `help_text` - Helper text below input (optional)
- `error` - Error message (optional, shows red border)
- `class` - Additional CSS classes

### Usage
```html
<c-input
    name="email"
    label="Email Address"
    type="email"
    placeholder="you@example.com"
    required="true"
    help_text="We'll never share your email." />

<!-- With Error -->
<c-input
    name="password"
    label="Password"
    type="password"
    error="Password must be at least 8 characters"
    required="true" />
```

---

## Navbar

A responsive navigation bar with mobile menu support.

**Requires:** Alpine.js

### Props
- `logo_text` - Logo text (default: 'Logo')
- `logo_url` - Logo link URL (default: '/')
- `class` - Additional CSS classes

### Usage
```html
<c-navbar logo_text="My App" logo_url="/">
    <a href="/about" class="text-gray-600 hover:text-gray-900">About</a>
    <a href="/services" class="text-gray-600 hover:text-gray-900">Services</a>
    <a href="/contact" class="text-gray-600 hover:text-gray-900">Contact</a>
    <a href="/login" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Login</a>
</c-navbar>
```

---

## Accordion

An expandable/collapsible content section.

**Requires:** Alpine.js

### Props
- `title` - Accordion title (required)
- `open` - Initially open (default: false)
- `class` - Additional CSS classes

### Usage
```html
<c-accordion title="What is Django Cotton?">
    Django Cotton is a library that provides reusable,
    component-based templates for Django projects.
</c-accordion>

<c-accordion title="How do I install it?" open="true">
    Simply run: pip install django-cotton
</c-accordion>
```

---

## Loading Button

A button with HTMX integration that shows a loading spinner during requests.

**Requires:** HTMX

### Props
- `text` - Button text (optional, can use slot)
- `hx_url` - HTMX request URL (required)
- `hx_method` - HTTP method: 'get', 'post', 'put', 'delete' (default: 'post')
- `hx_target` - HTMX target selector (optional)
- `hx_swap` - HTMX swap strategy (optional)
- `id` - Unique ID for the spinner (default: 'loading')
- `class` - Additional CSS classes

### Usage
```html
<!-- Simple POST -->
<c-loading_button
    text="Save Changes"
    hx_url="/api/save"
    hx_target="#result"
    hx_swap="innerHTML" />

<!-- GET Request -->
<c-loading_button
    text="Load More"
    hx_url="/api/posts?page=2"
    hx_method="get"
    hx_target="#posts"
    hx_swap="beforeend"
    id="load-more" />
```

---

## Installation & Setup

### 1. Install Dependencies
```bash
pip install django-cotton
npm install -D tailwindcss @tailwindcss/postcss daisyui
```

### 2. Add to INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ...
    'django_cotton',
]
```

### 3. Configure Template Loaders
```python
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': False,
    'OPTIONS': {
        'loaders': [
            'django_cotton.cotton_loader.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        'builtins': ['django_cotton.templatetags.cotton'],
    },
}]
```

### 4. Add CDN Links to base.html
```html
<!-- Alpine.js -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- HTMX -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

### 5. Place Components
Put all component `.html` files in `templates/cotton/` directory.

---

## Tips & Best Practices

1. **Combine Components** - Components can be nested inside each other
2. **Use Slots** - Pass complex content using the slot syntax
3. **Extend with Classes** - Add custom Tailwind classes via the `class` attribute
4. **Keep It Simple** - Don't over-engineer components; create new ones when needed
5. **Test Interactivity** - Always test Alpine.js and HTMX features in the browser

## Examples

### Nested Components
```html
<c-card title="User Profile" class="max-w-md">
    <div class="flex items-center space-x-2 mb-4">
        <c-badge text="Premium" variant="purple" />
        <c-badge text="Verified" variant="success" icon="true" />
    </div>

    <c-alert type="info" title="Welcome!">
        Thanks for joining our platform!
    </c-alert>

    <c-gradient_button
        text="Edit Profile"
        href="/profile/edit"
        class="mt-4" />
</c-card>
```

### Dynamic Form
```html
<form hx-post="/api/contact" hx-target="#form-result">
    <c-input name="name" label="Full Name" required="true" />
    <c-input name="email" label="Email" type="email" required="true" />
    <c-input name="message" label="Message" type="textarea" />

    <c-loading_button
        text="Send Message"
        hx_url="/api/contact"
        hx_target="#form-result" />
</form>
<div id="form-result"></div>
```

---

**Happy Building!** 🚀
