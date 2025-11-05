# Migration Guide: Unified Form Spacing System

## Overview

This guide helps you migrate existing templates to use the new unified form spacing system, ensuring consistent alignment and preventing future spacing issues.

## Quick Migration Steps

### 1. Add Required CSS Files

Update your template's `<head>` section:

```html
<!-- Add this to your existing CSS links -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/form-system.css') }}">
```

### 2. Import Form Macros

Add at the top of your template:

```jinja2
{% from 'macros/form_macros.html' import
    form_input_icon_text, form_input_icon_only, form_input_standard,
    form_textarea, form_select, form_checkbox, form_button_primary,
    icon_user, icon_email, icon_password, icon_organization, icon_back %}
```

### 3. Replace Existing Form Elements

#### Before (Inconsistent Spacing):
```html
<div>
    <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
        Username
    </label>
    <div class="relative">
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none" id="username-icon-group">
            <div class="flex items-center">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                <span class="ml-4 text-gray-400 text-sm">Choose username</span>
            </div>
        </div>
        <input
            type="text"
            name="username"
            id="username"
            required
            class="block w-full pl-32 pr-4 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-conservation-500 focus:border-conservation-500 transition-colors duration-200 leading-5"
            placeholder=""
            onfocus="hideIconGroup('username-icon-group')"
            onblur="showIconGroup('username-icon-group', this.value)"
        >
    </div>
</div>
```

#### After (Using Macro):
```jinja2
{{ form_input_icon_text('username', 'Username',
    icon=icon_user(),
    helper_text='Choose username',
    required=true) }}
```

#### After (Using CSS Classes):
```html
<div class="form-field">
    <label for="username" class="form-label-required">Username</label>
    <div class="relative">
        <div class="form-icon-group" id="username-icon-group">
            <div class="flex items-center">
                <svg class="form-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {{ icon_user()|safe }}
                </svg>
                <span class="form-icon-text">Choose username</span>
            </div>
        </div>
        <input
            type="text"
            name="username"
            id="username"
            required
            class="form-input-icon-text"
            placeholder=""
            onfocus="hideIconGroup('username-icon-group')"
            onblur="showIconGroup('username-icon-group', this.value)"
        >
    </div>
</div>
```

## Migration Patterns by Element Type

### 1. Text Input Fields

#### With Icon + Helper Text:
```jinja2
<!-- Old way -->
<input type="text" class="block w-full pl-32 pr-4 py-3 border border-gray-300...">

<!-- New way (Macro) -->
{{ form_input_icon_text('fieldname', 'Label', icon=icon_user(), helper_text='Helper text') }}

<!-- New way (CSS Classes) -->
<input type="text" class="form-input-icon-text">
```

#### With Icon Only:
```jinja2
<!-- Old way -->
<input type="password" class="block w-full pl-24 pr-4 py-3 border border-gray-300...">

<!-- New way (Macro) -->
{{ form_input_icon_only('password', 'Password', type='password', icon=icon_password()) }}

<!-- New way (CSS Classes) -->
<input type="password" class="form-input-icon-only">
```

#### Standard Input:
```jinja2
<!-- Old way -->
<input type="text" class="block w-full px-4 py-3 border border-gray-300...">

<!-- New way (Macro) -->
{{ form_input_standard('simple_field', 'Simple Field') }}

<!-- New way (CSS Classes) -->
<input type="text" class="form-input-standard">
```

### 2. Select Dropdowns

```jinja2
<!-- Old way -->
<select name="user_type" class="block w-full pl-32 pr-4 py-3 border border-gray-300...">
    <option value="student">Student</option>
</select>

<!-- New way (Macro) -->
{{ form_select('user_type', 'User Type', [
    {'value': 'student', 'label': 'Student'},
    {'value': 'teacher', 'label': 'Teacher'}
]) }}

<!-- New way (CSS Classes) -->
<select name="user_type" class="form-select">
    <option value="student">Student</option>
</select>
```

### 3. Textareas

```jinja2
<!-- Old way -->
<textarea name="content" class="block w-full px-4 py-3 border border-gray-300..." rows="6"></textarea>

<!-- New way (Macro) -->
{{ form_textarea('content', 'Content', rows=6, helper_text='Enter your content') }}

<!-- New way (CSS Classes) -->
<textarea name="content" class="form-textarea" rows="6"></textarea>
```

### 4. Buttons

```jinja2
<!-- Old way -->
<button type="submit" class="w-full inline-flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-conservation-600 hover:bg-conservation-700...">
    Create Account
</button>

<!-- New way (Macro) -->
{{ form_button_primary('Create Account') }}

<!-- New way (CSS Classes) -->
<button type="submit" class="form-button-primary">Create Account</button>
```

## Template-Specific Migration Examples

### Register Template (register.html)

#### Before:
```html
<!-- Username Field -->
<div>
    <label for="username" class="block text-sm font-medium text-gray-700 mb-2">Username</label>
    <div class="relative">
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none" id="username-icon-group">
            <div class="flex items-center">
                <svg class="h-5 w-5 text-gray-400">...</svg>
                <span class="ml-4 text-gray-400 text-sm">Choose username</span>
            </div>
        </div>
        <input type="text" name="username" id="username" required
               class="block w-full pl-32 pr-4 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-conservation-500 focus:border-conservation-500 transition-colors duration-200 leading-5"
               placeholder=""
               onfocus="hideIconGroup('username-icon-group')"
               onblur="showIconGroup('username-icon-group', this.value)">
    </div>
</div>
```

#### After:
```jinja2
{% from 'macros/form_macros.html' import form_input_icon_text, icon_user %}
{{ form_input_icon_text('username', 'Username', icon=icon_user(), helper_text='Choose username', required=true) }}
```

### Login Template (login.html)

#### Before:
```html
<!-- Email Field -->
<div>
    <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
    <div class="relative">
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none" id="email-icon-group">
            <div class="flex items-center">
                <svg class="h-5 w-5 text-gray-400">...</svg>
                <span class="ml-4 text-gray-400 text-sm">Enter email address</span>
            </div>
        </div>
        <input type="email" name="email" id="email" required
               class="block w-full pl-32 pr-4 py-3 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-conservation-500 focus:border-conservation-500 transition-colors duration-200 leading-5"
               placeholder=""
               onfocus="hideIconGroup('email-icon-group')"
               onblur="showIconGroup('email-icon-group', this.value)">
    </div>
</div>
```

#### After:
```jinja2
{% from 'macros/form_macros.html' import form_input_icon_text, icon_email %}
{{ form_input_icon_text('email', 'Email Address', type='email', icon=icon_email(), helper_text='Enter email address', required=true) }}
```

## Migration Checklist

### For Each Template:

- [ ] Add CSS file link: `form-system.css`
- [ ] Import form macros at top of template
- [ ] Replace input fields with appropriate macro/CSS class
- [ ] Replace select dropdowns with `form_select` macro or `form-select` class
- [ ] Replace textareas with `form_textarea` macro or `form-textarea` class
- [ ] Replace buttons with `form_button_primary` macro or `form-button-primary` class
- [ ] Add JavaScript functions: `{{ form_javascript() }}`
- [ ] Test form functionality and appearance
- [ ] Verify responsive behavior on mobile
- [ ] Check accessibility with screen readers

### Common Issues to Watch For:

1. **Missing JavaScript**: Ensure `{{ form_javascript() }}` is included
2. **Icon paths**: Use macro icons or include proper SVG paths
3. **Form validation**: Test required fields and validation states
4. **Mobile responsiveness**: Check on actual mobile devices
5. **Browser compatibility**: Test in multiple browsers

## Testing Your Migration

### Visual Testing:
1. Compare old vs new template side-by-side
2. Check alignment of all form elements
3. Verify consistent spacing between fields
4. Test icon positioning and text alignment

### Functional Testing:
1. Test form submission functionality
2. Verify validation works correctly
3. Check JavaScript interactions (icon hiding/showing)
4. Test on mobile devices

### Accessibility Testing:
1. Use screen reader to navigate form
2. Test keyboard navigation (Tab key)
3. Verify focus indicators are visible
4. Check color contrast ratios

## Rollback Plan

If issues arise:

1. **Keep original template backup** before migration
2. **Test thoroughly** in development environment
3. **Stage deployment** to production
4. **Monitor user feedback** after deployment
5. **Quick rollback** available if critical issues found

## Benefits of Migration

✅ **Consistent spacing** across all templates
✅ **Reduced code duplication**
✅ **Faster development** with reusable components
✅ **Better maintainability**
✅ **Improved accessibility**
✅ **Mobile-responsive** by default
✅ **Future-proof** design system

## Support

For questions or issues during migration:
- Check the [Design System Documentation](DESIGN_SYSTEM.md)
- Review example implementation in `example_unified_form.html`
- Test against the working examples in modern templates

---

This migration ensures all templates use consistent spacing patterns, preventing future alignment issues and creating a cohesive user experience across the entire Komodo Hub application.