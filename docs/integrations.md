# Project Integrations Guide

## Overview
This document outlines all external integrations, APIs, libraries, and services required to complete the projects in this repository.

---

## Front-End Project Integrations

### Required APIs

#### Google Maps JavaScript API
- **Purpose**: Display interactive maps, markers, and location data
- **Documentation**: https://developers.google.com/maps/documentation/javascript/
- **Setup Steps**:
  1. Create a Google Cloud Platform account
  2. Enable Google Maps JavaScript API
  3. Generate API key
  4. Add API key to project (currently using: `AIzaSyDyzXYDJaMcu0wYaYBSua3HvTfT6ZSpASQ`)
  5. Configure API restrictions (HTTP referrers, API restrictions)
- **Features Used**:
  - Map initialization and display
  - Marker placement and customization
  - Map event handling (clicks, zoom)
  - Geocoding (optional)
- **Cost**: Free tier available (28,000 map loads/month), pay-as-you-go beyond that
- **Alternative**: Mapbox, Leaflet with OpenStreetMap

### Required Libraries & Frameworks

#### React
- **Version**: Latest stable (18.x+)
- **Purpose**: Build interactive UI components
- **Installation**: `npm install react react-dom`
- **Documentation**: https://react.dev/
- **Key Features**:
  - Component-based architecture
  - State management with hooks
  - Event handling
  - Conditional rendering

#### React Build Tools
- **Options**:
  - **Vite** (recommended): `npm create vite@latest`
  - **Create React App**: `npx create-react-app`
  - **Next.js**: `npx create-next-app`
- **Purpose**: Development server, bundling, hot reload

#### Chart.js (Extra Credit)
- **Version**: 4.x
- **Purpose**: Display store traffic data in modal
- **Installation**: `npm install chart.js react-chartjs-2`
- **Documentation**: https://www.chartjs.org/
- **Alternative**: Recharts, D3.js, Victory

### Mock API Server

#### Option 1: JSON Server
- **Installation**: `npm install -g json-server`
- **Purpose**: Quick REST API mock
- **Setup**: Create `db.json` with sample data
- **Start**: `json-server --watch db.json --port 3001`

#### Option 2: MSW (Mock Service Worker)
- **Installation**: `npm install msw --save-dev`
- **Purpose**: Intercept network requests in browser/Node
- **Documentation**: https://mswjs.io/

#### Option 3: Express.js
- **Installation**: `npm install express`
- **Purpose**: Custom Node.js API server
- **More control over endpoints and logic**

### Development Tools

#### Package Manager
- **npm** (comes with Node.js)
- **yarn**: `npm install -g yarn`
- **pnpm**: `npm install -g pnpm`

#### Node.js
- **Version**: 18.x or higher
- **Download**: https://nodejs.org/
- **Purpose**: JavaScript runtime for build tools

---

## Inventory Reconciliation Project Integrations

### Required Language & Runtime

#### Python
- **Version**: 3.10 or higher
- **Download**: https://www.python.org/downloads/
- **Purpose**: Main programming language for reconciliation script

### Required Libraries

#### Pandas
- **Installation**: `pip install pandas`
- **Purpose**: CSV manipulation, data analysis, comparison
- **Documentation**: https://pandas.pydata.org/
- **Key Features**:
  - DataFrame operations
  - CSV reading/writing
  - Data filtering and grouping
  - Merge and join operations

#### Pytest
- **Installation**: `pip install pytest`
- **Purpose**: Testing framework
- **Documentation**: https://docs.pytest.org/
- **Additional plugins**:
  - `pytest-cov` for coverage: `pip install pytest-cov`
  - `pytest-mock` for mocking: `pip install pytest-mock`

### Optional Libraries

#### NumPy
- **Installation**: `pip install numpy`
- **Purpose**: Numerical operations (if needed)
- **Often installed as pandas dependency**

#### Openpyxl
- **Installation**: `pip install openpyxl`
- **Purpose**: Excel file support (if extending to .xlsx)

### Development Tools

#### Virtual Environment
- **Built-in**: `python -m venv venv`
- **Activation**:
  - Windows: `venv\Scripts\activate`
  - Unix/Mac: `source venv/bin/activate`
- **Purpose**: Isolated Python environment

#### Linting & Formatting
- **Black**: `pip install black` (code formatter)
- **Flake8**: `pip install flake8` (linter)
- **mypy**: `pip install mypy` (type checker)

---

## Log Parsing Project Integrations

### Language Options & Libraries

#### Python Option

##### Standard Library (No Installation Required)
- **csv**: CSV parsing
- **xml.etree.ElementTree**: XML parsing
- **json**: JSON output generation
- **re**: Regular expressions for text parsing
- **datetime**: Timestamp handling

##### Optional Libraries
- **lxml**: `pip install lxml` (faster XML parsing)
- **pandas**: `pip install pandas` (advanced analysis)
- **python-dateutil**: `pip install python-dateutil` (flexible date parsing)

#### JavaScript/Node.js Option

##### Required Libraries
- **csv-parse**: `npm install csv-parse`
- **xml2js**: `npm install xml2js`
- **fast-xml-parser**: `npm install fast-xml-parser` (alternative)
- **date-fns**: `npm install date-fns` (date utilities)

##### Standard Library
- **fs**: File system operations (built-in)
- **JSON**: JSON handling (built-in)

#### Ruby Option

##### Standard Library
- **CSV**: CSV parsing (built-in)
- **REXML**: XML parsing (built-in)
- **JSON**: JSON generation (built-in)
- **Time/DateTime**: Timestamp handling (built-in)

##### Optional Gems
- **Nokogiri**: `gem install nokogiri` (better XML parsing)
- **Chronic**: `gem install chronic` (natural language date parsing)

### Development Tools

#### Testing Frameworks
- **Python**: pytest, unittest
- **JavaScript**: Jest, Mocha
- **Ruby**: RSpec, Minitest

---

## Ruby Project Integrations

### Required Language & Runtime

#### Ruby
- **Version**: 2.7 or higher (3.x recommended)
- **Download**: https://www.ruby-lang.org/en/downloads/
- **Purpose**: Main programming language
- **Installation**:
  - **macOS**: `brew install ruby`
  - **Linux**: `sudo apt-get install ruby-full`
  - **Windows**: RubyInstaller

### XML Parsing Libraries

#### Option 1: REXML (Built-in)
- **No installation required**
- **Purpose**: Basic XML parsing
- **Documentation**: https://ruby-doc.org/stdlib/libdoc/rexml/rdoc/REXML.html
- **Pros**: No dependencies, simple API
- **Cons**: Slower performance

#### Option 2: Nokogiri (Recommended)
- **Installation**: `gem install nokogiri`
- **Purpose**: Fast, robust XML/HTML parsing
- **Documentation**: https://nokogiri.org/
- **Features**:
  - XPath support
  - CSS selectors
  - Better performance
  - Error handling
- **Pros**: Fast, feature-rich, widely used
- **Cons**: Requires native extensions

### Testing Tools

#### Built-in Test Support
- **test_support.rb**: Already provided in repository
- **Purpose**: Custom assertion helpers

#### Optional Testing Frameworks
- **RSpec**: `gem install rspec` (BDD framework)
- **Minitest**: Built-in with Ruby (unit testing)

### Development Tools

#### Bundler
- **Installation**: `gem install bundler`
- **Purpose**: Dependency management
- **Usage**: Create `Gemfile`, run `bundle install`

#### RuboCop (Optional)
- **Installation**: `gem install rubocop`
- **Purpose**: Code linting and style checking

---

## Cross-Project Development Tools

### Version Control

#### Git
- **Purpose**: Source control
- **Download**: https://git-scm.com/
- **Required for**: Tracking progress, submission

### Code Editors

#### VS Code (Recommended)
- **Download**: https://code.visualstudio.com/
- **Extensions**:
  - ESLint (JavaScript)
  - Python
  - Ruby
  - Prettier (code formatting)
  - GitLens (Git integration)

#### Alternatives
- **JetBrains IDEs**: WebStorm, PyCharm, RubyMine
- **Sublime Text**
- **Vim/Neovim**

### Browser Developer Tools

#### Chrome DevTools
- **Purpose**: Debugging front-end, network inspection
- **Built into Chrome/Edge**

#### React Developer Tools
- **Installation**: Chrome/Firefox extension
- **Purpose**: Inspect React component tree

---

## Setup Priority & Order

### 1. Front-End Project
```bash
# Install Node.js first
node --version  # Verify installation

# Create React app
npm create vite@latest map-search-app -- --template react
cd map-search-app
npm install

# Install additional dependencies
npm install chart.js react-chartjs-2

# Set up mock API (choose one)
npm install -g json-server
# OR
npm install msw --save-dev
```

### 2. Inventory Reconciliation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install pandas pytest pytest-cov

# Verify installation
python --version
pip list
```

### 3. Log Parsing
```bash
# Python option (if not already set up)
pip install lxml python-dateutil

# JavaScript option
npm init -y
npm install csv-parse xml2js date-fns

# Ruby option
gem install nokogiri
```

### 4. Ruby Projects
```bash
# Verify Ruby installation
ruby --version

# Install Nokogiri (optional but recommended)
gem install nokogiri

# Install Bundler
gem install bundler

# Create Gemfile (optional)
bundle init
```

---

## API Keys & Credentials

### Google Maps API Key
- **Required for**: Front-end map search project
- **Setup**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Create new project or select existing
  3. Enable "Maps JavaScript API"
  4. Create credentials → API Key
  5. Restrict key (HTTP referrers, API restrictions)
- **Security**: Never commit API keys to public repositories
- **Environment Variables**: Store in `.env` file (add to `.gitignore`)

---

## Environment Configuration

### Front-End `.env` Example
```env
VITE_GOOGLE_MAPS_API_KEY=your_api_key_here
VITE_API_BASE_URL=http://localhost:3001
```

### Python `.env` Example (if needed)
```env
LOG_LEVEL=INFO
OUTPUT_DIR=./output
```

---

## Troubleshooting Common Integration Issues

### Google Maps API
- **Issue**: Map not loading
- **Solutions**:
  - Verify API key is correct
  - Check browser console for errors
  - Ensure billing is enabled on Google Cloud
  - Verify API restrictions allow your domain

### Python Pandas
- **Issue**: Installation fails
- **Solutions**:
  - Update pip: `pip install --upgrade pip`
  - Install build tools (Windows: Visual Studio Build Tools)
  - Try conda: `conda install pandas`

### Nokogiri (Ruby)
- **Issue**: Native extension build fails
- **Solutions**:
  - Install development tools
  - macOS: `xcode-select --install`
  - Ubuntu: `sudo apt-get install build-essential`
  - Windows: Install DevKit

### Node.js/npm
- **Issue**: Permission errors
- **Solutions**:
  - Use nvm (Node Version Manager)
  - Don't use sudo with npm
  - Fix npm permissions: https://docs.npmjs.com/resolving-eacces-permissions-errors

---

## Cost Considerations

### Free Tier Services
- **Google Maps API**: 28,000 map loads/month free
- **All development tools**: Free and open source

### Paid Services (Optional)
- **Google Maps API**: Beyond free tier
- **JetBrains IDEs**: Paid (free for students)

### Recommended: Stick to Free Options
All projects can be completed entirely with free, open-source tools and services.

---

## Additional Resources

### Documentation Links
- [MDN Web Docs](https://developer.mozilla.org/) - Web technologies
- [Python Documentation](https://docs.python.org/3/)
- [Ruby Documentation](https://ruby-doc.org/)
- [Node.js Documentation](https://nodejs.org/docs/)

### Learning Resources
- [React Tutorial](https://react.dev/learn)
- [Pandas Tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)
- [Ruby Koans](http://rubykoans.com/)

### Community Support
- [Stack Overflow](https://stackoverflow.com/)
- [GitHub Discussions](https://github.com/)
- [Reddit](https://www.reddit.com/r/programming/)