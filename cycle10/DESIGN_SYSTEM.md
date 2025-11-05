# Komodo Hub Design System

## Overview

This document outlines the unified design system for Komodo Hub, focusing on consistent spacing, typography, and form element styling across all templates. The system prevents future spacing inconsistencies and provides reusable components for rapid development.

## Form Element Spacing Standards

### Input Field Classes

| Class Name | Use Case | Padding | Example |
|------------|----------|---------|---------|
| `form-input-icon-text` | Input with icon + helper text | `pl-32 pr-4 py-3` | Username, Email fields |
| `form-input-icon-only` | Input with icon only | `pl-24 pr-4 py-3` | Password fields |
| `form-input-standard` | Standard input without icons | `px-4 py-3` | Simple text fields |
| `form-textarea` | Textarea fields | `px-4 py-3` | Content, descriptions |
| `form-select` | Select dropdown with icons | `pl-32 pr-4 py-3` | Organization selection |
| `form-select-standard` | Select without icons | `px-4 py-3` | Simple dropdowns |

### Spacing Specifications

- **Icon left margin**: `pl-3` (12px from container edge)
- **Icon-text spacing**: `ml-4` (16px between icon and helper text)
- **Input field height**: `py-3` (12px vertical padding)
- **Standard horizontal padding**: `px-4` (16px both sides)
- **Icon field left padding**: `pl-32` (128px total - accommodates icon + text)
- **Icon-only left padding**: `pl-24` (96px total - accommodates icon only)

## Usage Examples

### 1. Input Field with Icon and Helper Text
```html
<!-- Using CSS classes directly -->
<div class="form-field">
    <label for="username" class="form-label">Username</label>
    <div class="relative">
        <div class="form-icon-group" id="username-icon-group">
            <div class="flex items-center">
                <svg class="form-icon">...user icon...</svg>
                <span class="form-icon-text">Choose username</span>
            </div>
        </div>
        <input type="text" name="username" class="form-input-icon-text"
               onfocus="hideIconGroup('username-icon-group')"
               onblur="showIconGroup('username-icon-group', this.value)">
    </div>
</div>

<!-- Using Jinja2 macro -->
{% from 'macros/form_macros.html' import form_input_icon_text, icon_user %}
{{ form_input_icon_text('username', 'Username', icon=icon_user(), helper_text='Choose username') }}
```

### 2. Select Dropdown
```html
<!-- Standard select -->
<select name="user_type" class="form-select">
    <option value="student">Student</option>
    <option value="teacher">Teacher</option>
</select>

<!-- Using macro -->
{% from 'macros/form_macros.html' import form_select %}
{{ form_select('user_type', 'User Type', [
    {'value': 'student', 'label': 'Student'},
    {'value': 'teacher', 'label': 'Teacher'}
]) }}
```

### 3. Textarea Field
```html
<!-- Standard textarea -->
<textarea name="content" class="form-textarea" rows="6"
          placeholder="Write your content here..."></textarea>

<!-- Using macro -->
{% from 'macros/form_macros.html' import form_textarea %}
{{ form_textarea('content', 'Content', placeholder='Write your content here...', rows=6) }}
```

## File Structure

```
static/css/
├── form-system.css          # Unified form spacing classes
├── uno.css                  # UnoCSS framework
└── uno-components.css       # Custom UnoCSS components

templates/macros/
└── form_macros.html         # Reusable Jinja2 form components
```

## Implementation Guidelines

### 1. Include Required Files
Add these to your template's `<head>` section:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/uno.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/form-system.css') }}">
```

### 2. Import Form Macros
At the top of your template:
```jinja2
{% from 'macros/form_macros.html' import
    form_input_icon_text, form_input_icon_only, form_input_standard,
    form_textarea, form_select, form_checkbox, form_button_primary,
    icon_user, icon_email, icon_password, icon_organization %}
```

### 3. Use Consistent Form Structure
```html
<form method="post" class="space-y-6">
    {{ form_input_icon_text('username', 'Username', icon=icon_user(), helper_text='Choose username', required=true) }}
    {{ form_input_icon_text('email', 'Email', type='email', icon=icon_email(), helper_text='Enter email address', required=true) }}
    {{ form_input_icon_only('password', 'Password', type='password', icon=icon_password(), required=true) }}

    <div class="form-actions">
        {{ form_button_primary('Create Account') }}
    </div>
</form>
```

## JavaScript Functions

Include the form interaction JavaScript:
```jinja2
{{ form_javascript() }}
```

This provides:
- `hideIconGroup(groupId)` - Hides icon group on focus
- `showIconGroup(groupId, inputValue)` - Shows icon group on blur if empty

## Responsive Design

All form elements are mobile-responsive:
- Text inputs use `text-base` on mobile to prevent zoom
- Touch-friendly tap targets (minimum 44px height)
- Responsive padding that adapts to screen size

## Accessibility Standards

- Proper focus indicators with `focus:ring-2`
- High contrast mode support
- Screen reader compatible labels
- Keyboard navigation support

## Migration Guide

### For Existing Templates

1. **Identify current spacing classes** in your template
2. **Replace with appropriate form-system class**:
   - `pl-32 pr-4 py-3 border...` → `form-input-icon-text`
   - `pl-24 pr-4 py-3 border...` → `form-input-icon-only`
   - `px-4 py-3 border...` → `form-input-standard`
3. **Add icon group containers** if using icons
4. **Include JavaScript functions** for interactive behavior

### For New Templates

1. **Always use the macro system** when possible
2. **Follow the established patterns** shown in examples
3. **Test on mobile devices** for responsive behavior
4. **Validate accessibility** with screen readers

## Common Patterns

### Registration Form
```jinja2
{% from 'macros/form_macros.html' import
    form_input_icon_text, form_select, form_button_primary,
    icon_user, icon_email, icon_password %}

<form method="post" class="space-y-6">
    {{ form_input_icon_text('username', 'Username', icon=icon_user(), helper_text='Choose username', required=true) }}
    {{ form_input_icon_text('email', 'Email', type='email', icon=icon_email(), helper_text='Enter email address', required=true) }}
    {{ form_input_icon_only('password', 'Password', type='password', icon=icon_password(), required=true) }}
    {{ form_select('user_type', 'User Type', user_types, required=true) }}

    <div class="form-actions">
        {{ form_button_primary('Create Account', icon=icon_add()) }}
    </div>
</form>
{{ form_javascript() }}
```

### Login Form
```jinja2
<form method="post" class="space-y-6">
    {{ form_input_icon_text('email', 'Email Address', type='email', icon=icon_email(), helper_text='Enter email address', required=true) }}
    {{ form_input_icon_only('password', 'Password', type='password', icon=icon_password(), required=true) }}

    <div class="form-actions">
        {{ form_button_primary('Sign In', icon=icon_login()) }}
    </div>
</form>
{{ form_javascript() }}
```

## Troubleshooting

### Common Issues

1. **Icons not aligning properly**
   - Ensure proper `relative` container positioning
   - Check icon group has correct `pl-3` spacing
   - Verify icon-text has `ml-4` spacing

2. **Input fields different widths**
   - All form classes include `w-full` for full width
   - Check parent container constraints

3. **Mobile zoom on focus**
   - Ensure `text-base` class is applied on mobile
   - Use responsive breakpoints if needed

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Graceful degradation for older browsers

## Future Enhancements

- Additional form validation states
- More icon options
- File upload components
- Date picker integration
- Multi-step form patterns

---

This design system ensures consistent, maintainable, and accessible form elements across the entire Komodo Hub application. Regular updates will be made to expand component coverage and improve user experience.