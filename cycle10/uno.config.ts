import { defineConfig, presetUno, presetAttributify, presetIcons, transformerDirectives, transformerVariantGroup } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
      warn: true,
    })
  ],

  // Custom theme configuration to match Komodo Hub's conservation theme
  theme: {
    colors: {
      // Primary conservation colors
      'conservation': {
        50: '#f0f9f0',
        100: '#dcf2dc',
        200: '#bce5bc',
        300: '#8dd18d',
        400: '#5bb85b',
        500: '#2c5530', // Original primary green
        600: '#4a7c59', // Original secondary green
        700: '#1e3a21',
        800: '#152515',
        900: '#0a120a',
      },
      // Earth tones
      'earth': {
        50: '#faf8f5',
        100: '#f2ede4',
        200: '#e6d7c3',
        300: '#d4b896',
        400: '#c19668',
        500: '#b07a4a',
        600: '#9c663c',
        700: '#825134',
        800: '#6b422e',
        900: '#573728',
      },
      // Komodo dragon inspired colors
      'komodo': {
        50: '#f7f6f2',
        100: '#eeede4',
        200: '#ddd9c8',
        300: '#c4bfa3',
        400: '#aba077',
        500: '#96885d',
        600: '#8a7a52',
        700: '#736345',
        800: '#5e523a',
        900: '#4e4431',
      }
    },
    // Custom spacing
    spacing: {
      'xs': '0.25rem',
      'sm': '0.5rem',
      'md': '1rem',
      'lg': '1.5rem',
      'xl': '2rem',
      '2xl': '3rem',
      '3xl': '4rem',
    },
    // Custom border radius
    borderRadius: {
      'none': '0',
      'sm': '0.125rem',
      'DEFAULT': '0.25rem',
      'md': '0.375rem',
      'lg': '0.5rem',
      'xl': '0.75rem',
      '2xl': '1rem',
      '3xl': '1.5rem',
      'full': '9999px',
    },
    // Custom shadows that match the current design
    boxShadow: {
      'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      'DEFAULT': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
      'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
      'none': 'none',
    }
  },

  // Custom shortcuts for common Komodo Hub patterns
  shortcuts: [
    // Button variants with specific colors
    ['btn-primary', 'inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-conservation-600 hover:bg-conservation-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-conservation-500 transition-colors duration-200'],
    ['btn-secondary', 'inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-earth-600 hover:bg-earth-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-earth-500 transition-colors duration-200'],
    ['btn-success', 'inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-200'],
    ['btn-danger', 'inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200'],
    ['btn-warning', 'inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-colors duration-200'],
    ['btn-info', 'inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200'],

    // Card components
    ['card', 'bg-white rounded-lg shadow-md overflow-hidden'],
    ['card-header', 'px-6 py-4 bg-conservation-50 border-b border-conservation-200'],
    ['card-body', 'p-6'],
    ['card-footer', 'px-6 py-4 bg-gray-50 border-t border-gray-200'],
    ['card-primary', 'bg-white rounded-lg shadow-md overflow-hidden border-l-4 border-conservation-500'],
    ['card-secondary', 'bg-white rounded-lg shadow-md overflow-hidden border-l-4 border-earth-500'],
    ['card-success', 'bg-white rounded-lg shadow-md overflow-hidden border-l-4 border-green-500'],
    ['card-danger', 'bg-white rounded-lg shadow-md overflow-hidden border-l-4 border-red-500'],

    // Form components
    ['form-group', 'mb-4'],
    ['form-label', 'block text-sm font-medium text-gray-700 mb-1'],
    ['form-input', 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-conservation-500 focus:border-conservation-500 sm:text-sm'],
    ['form-textarea', 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-conservation-500 focus:border-conservation-500 sm:text-sm resize-vertical'],
    ['form-select', 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-conservation-500 focus:border-conservation-500 sm:text-sm'],

    // Alert components
    ['alert', 'p-4 rounded-md border-l-4'],
    ['alert-success', 'p-4 rounded-md border-l-4 bg-green-50 text-green-800 border-green-500'],
    ['alert-error', 'p-4 rounded-md border-l-4 bg-red-50 text-red-800 border-red-500'],
    ['alert-warning', 'p-4 rounded-md border-l-4 bg-yellow-50 text-yellow-800 border-yellow-500'],
    ['alert-info', 'p-4 rounded-md border-l-4 bg-blue-50 text-blue-800 border-blue-500'],

    // Navigation
    ['nav-link', 'text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200'],
    ['nav-link-active', 'text-white bg-conservation-700 px-3 py-2 rounded-md text-sm font-medium'],

    // Avatar
    ['avatar', 'w-10 h-10 rounded-full object-cover border-2 border-white shadow-sm'],
    ['avatar-sm', 'w-8 h-8 rounded-full object-cover border-2 border-white shadow-sm'],
    ['avatar-lg', 'w-16 h-16 rounded-full object-cover border-2 border-white shadow-md'],

    // Gradient backgrounds
    ['gradient-conservation', 'bg-gradient-to-r from-conservation-500 to-conservation-600'],
    ['gradient-earth', 'bg-gradient-to-r from-earth-500 to-earth-600'],
    ['gradient-komodo', 'bg-gradient-to-r from-komodo-500 to-komodo-600'],

    // Loading states
    ['loading-spinner', 'animate-spin h-5 w-5 text-conservation-600'],
  ],

  // Rules to include/exclude
  rules: [
    // Custom rules for specific patterns
    [/^text-(.*)-lg$/, ([, c]) => ({ 'font-size': '1.125rem', 'line-height': '1.75rem', color: `var(--un-color-${c})` })],
    [/^bg-(.*)-gradient$/, ([, c]) => ({ background: `linear-gradient(135deg, var(--un-color-${c}-500), var(--un-color-${c}-600))` })],
  ],

  // Transformers
  transformers: [
    transformerDirectives(),
    transformerVariantGroup(),
  ],

  // Content to scan
  content: {
    pipeline: {
      include: [
        // Scan all HTML templates
        'templates/**/*.html',
        // Scan any JavaScript files that might contain dynamic classes
        'static/js/**/*.js',
        // Include any Python files that might generate HTML with classes
        '**/*.py'
      ],
      exclude: [
        'node_modules/**',
        '**/*.min.js',
        '**/*.min.css'
      ]
    }
  },

  // Safelist - classes that should always be included
  safelist: [
    // Common utility classes that might be used dynamically
    'text-red-500',
    'text-green-500',
    'text-yellow-500',
    'text-blue-500',
    'bg-red-100',
    'bg-green-100',
    'bg-yellow-100',
    'bg-blue-100',
    // Dynamic color classes that might be generated
    'text-conservation-500',
    'text-earth-500',
    'text-komodo-500',
    'bg-conservation-500',
    'bg-earth-500',
    'bg-komodo-500',
    // Common button states
    'hover:bg-conservation-700',
    'focus:ring-conservation-500',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed'
  ],

  // Extractors for different file types
  extractors: [
    // Default extractor for HTML-like files
    (code) => code.match(/[\w-:]+(?!\w*\{)/g) || [],
    // Custom extractor for Jinja2 template syntax
    (code, id) => {
      if (id.includes('.html')) {
        // Extract classes from Jinja2 templates
        return code.match(/class\s*=\s*["']([^"']+)["']/g)?.map(
          match => match.replace(/class\s*=\s*["']([^"']+)["']/, '$1')
        ).join(' ').split(/\s+/) || []
      }
    }
  ],

  // CLI configuration
  cli: {
    entry: [
      {
        patterns: ['templates/**/*.html'],
        outFile: 'static/css/uno.css'
      }
    ]
  }
})