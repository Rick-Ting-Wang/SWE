#!/bin/bash

# Setup script for UnoCSS in Komodo Hub
# This script installs Node.js dependencies and builds the initial UnoCSS file

echo "🦎 Setting up UnoCSS for Komodo Hub..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Install dependencies
echo "📦 Installing UnoCSS dependencies..."
npm install

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static/css
mkdir -p static/js/components

# Build initial UnoCSS file
echo "🏗️  Building initial UnoCSS file..."
npm run build

# Check if the build was successful
if [ -f "static/css/uno.css" ]; then
    echo "✅ UnoCSS build successful!"
    echo "📊 File size: $(ls -lh static/css/uno.css | awk '{print $5}')"
else
    echo "❌ UnoCSS build failed. Please check the configuration."
    exit 1
fi

# Create a development watch script
echo "📝 Creating development scripts..."
cat > dev-unocss.sh << 'EOF'
#!/bin/bash
echo "👀 Starting UnoCSS watch mode..."
echo "Press Ctrl+C to stop"
npm run dev
EOF

chmod +x dev-unocss.sh

echo ""
echo "🎉 UnoCSS setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update templates to use UnoCSS classes"
echo "2. Run './dev-unocss.sh' to start development mode"
echo "3. Run 'npm run build' to build for production"
echo ""
echo "📚 Documentation:"
echo "- Configuration: uno.config.ts"
echo "- Build scripts: package.json"
echo "- Usage guide: test/README.md"