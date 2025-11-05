# UnoCSS Migration Guide for Komodo Hub

This guide provides step-by-step instructions for migrating the Komodo Hub frontend from custom CSS to UnoCSS.

## Overview

The migration involves:
1. Setting up UnoCSS build pipeline
2. Creating UnoCSS versions of templates
3. Converting CSS classes to UnoCSS utilities
4. Preserving the conservation-themed design system
5. Testing and validation

## Setup Instructions

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Or run the setup script
./setup-unocss.sh
```

### 2. Build UnoCSS

```bash
# Development mode (watch for changes)
npm run dev

# Production build
npm run build
```

## Migration Strategy

### Phase 1: Core Templates (Priority)
1. `base.html` → `base-uno.html` ✅
2. `main_menu.html` → `main_menu-uno.html` ✅
3. `login.html` → `login-uno.html`
4. `register.html` → `register-uno.html`

### Phase 2: Form Templates
5. `create_organization.html` → `create_organization-uno.html`
6. `join_organization.html` → `join_organization-uno.html`
7. `create_class.html` → `create_class-uno.html`
8. `create_program.html` → `create_program-uno.html`

### Phase 3: Feature Templates
9. `user_center.html` → `user_center-uno.html`
10. `submit_assignment.html` → `submit_assignment-uno.html`
11. `grade_submission.html` → `grade_submission-uno.html`
12. `report_sighting.html` → `report_sighting-uno.html`

### Phase 4: Remaining Templates
13. All other templates

## CSS to UnoCSS Conversion Mapping

### Layout & Containers
```css
/* Original CSS */
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

/* UnoCSS Equivalent */
max-w-7xl mx-auto px-4 sm:px-6 lg:px-8
```

### Colors (Conservation Theme)
```css
/* Original CSS */
background: linear-gradient(135deg, #2c5530, #4a7c59);

/* UnoCSS Equivalent */
bg-gradient-to-r from-conservation-500 to-conservation-600
```

### Typography
```css
/* Original CSS */
font-size: 2rem; font-weight: bold; color: #2c5530;

/* UnoCSS Equivalent */
text-2xl font-bold text-conservation-800
```

### Spacing
```css
/* Original CSS */
padding: 1rem; margin-bottom: 1.5rem;

/* UnoCSS Equivalent */
p-4 mb-6
```

### Cards & Containers
```css
/* Original CSS */
background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);

/* UnoCSS Equivalent */
bg-white p-8 rounded-lg shadow-md
```

### Buttons
```css
/* Original CSS */
.btn { padding: 0.75rem 1.5rem; background: #4a7c59; border-radius: 6px; }

/* UnoCSS Equivalent */
inline-flex items-center justify-center px-4 py-2 bg-conservation-600 hover:bg-conservation-700 rounded-md text-white font-medium transition-colors duration-200
```

### Grid Layouts
```css
/* Original CSS */
display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;

/* UnoCSS Equivalent */
grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6
```

## Custom Components Created

### Button Variants
```html
<!-- Primary Button -->
<button class="inline-flex items-center justify-center px-4 py-2 bg-conservation-600 hover:bg-conservation-700 rounded-md text-white font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-conservation-500">
  Primary Button
</button>

<!-- Secondary Button -->
<button class="inline-flex items-center justify-center px-4 py-2 bg-earth-600 hover:bg-earth-700 rounded-md text-white font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-earth-500">
  Secondary Button
</button>
```

### Card Components
```html
<!-- Basic Card -->
<div class="bg-white rounded-lg shadow-md p-6">
  Card content
</div>

<!-- Card with Header -->
<div class="bg-white rounded-lg shadow-md overflow-hidden">
  <div class="px-6 py-4 bg-conservation-50 border-b border-conservation-200">
    Card Header
  </div>
  <div class="p-6">
    Card Body
  </div>
</div>
```

### Form Components
```html
<!-- Form Group -->
<div class="mb-4">
  <label class="block text-sm font-medium text-gray-700 mb-1">Label</label>
  <input type="text" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-conservation-500 focus:border-conservation-500 sm:text-sm">
</div>
```

### Alert Components
```html
<!-- Success Alert -->
<div class="p-4 rounded-md border-l-4 bg-green-50 text-green-800 border-green-500 animate-fade-in">
  Success message
</div>

<!-- Error Alert -->
<div class="p-4 rounded-md border-l-4 bg-red-50 text-red-800 border-red-500 animate-fade-in">
  Error message
</div>
```

## Migration Checklist

### Template Migration
- [ ] Update DOCTYPE and html tags
- [ ] Replace CSS links with UnoCSS
- [ ] Convert all class names to UnoCSS utilities
- [ ] Preserve Jinja2 template syntax
- [ ] Test responsive breakpoints
- [ ] Verify color scheme consistency

### CSS Pattern Conversion
- [ ] Layout containers → UnoCSS grid/flex
- [ ] Custom colors → UnoCSS color utilities
- [ ] Spacing → UnoCSS spacing utilities
- [ ] Typography → UnoCSS text utilities
- [ ] Borders/shadows → UnoCSS border/shadow utilities
- [ ] Animations → UnoCSS animate utilities

### Testing
- [ ] Test all page layouts
- [ ] Verify responsive behavior
- [ ] Check form styling
- [ ] Validate accessibility
- [ ] Test JavaScript interactions
- [ ] Cross-browser compatibility

## Common Patterns

### Navigation Bar
```html
<header class="bg-gradient-to-r from-conservation-500 to-conservation-600 shadow-lg">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center py-4">
      <h1 class="text-2xl font-bold text-white tracking-tight">Komodo Hub</h1>
      <nav class="flex items-center space-x-4">
        <a href="#" class="text-conservation-100 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 hover:bg-conservation-700">Link</a>
      </nav>
    </div>
  </div>
</header>
```

### Form Layout
```html
<div class="max-w-md mx-auto">
  <form class="bg-white rounded-lg shadow-md p-6 space-y-4">
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
      <input type="email" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-conservation-500 focus:border-conservation-500 sm:text-sm">
    </div>
    <button type="submit" class="w-full inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-conservation-600 hover:bg-conservation-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-conservation-500">
      Submit
    </button>
  </form>
</div>
```

### Grid Layout
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
    Card content
  </div>
</div>
```

## Responsive Design

### Breakpoints
- `sm:` - 640px and up
- `md:` - 768px and up
- `lg:` - 1024px and up
- `xl:` - 1280px and up
- `2xl:` - 1536px and up

### Mobile-First Approach
```html
<!-- Mobile first, then larger screens -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  Content
</div>
```

## Performance Considerations

1. **Purging**: UnoCSS automatically purges unused styles
2. **Minification**: Use `--minify` flag for production builds
3. **Safelist**: Add dynamic classes to safelist in config
4. **Bundle Size**: Only generated classes are included

## Testing

After migration, test:
1. All page layouts render correctly
2. Responsive breakpoints work properly
3. Forms are functional and styled
4. JavaScript interactions still work
5. Accessibility standards are met
6. Cross-browser compatibility

## Rollback Plan

If issues arise:
1. Switch back to original templates
2. Remove UnoCSS links
3. Restore original CSS links
4. Templates are preserved with `-uno` suffix

## Next Steps

1. Complete template migration following the checklist
2. Test all functionality
3. Optimize for production
4. Update documentation
5. Train team on UnoCSS usage