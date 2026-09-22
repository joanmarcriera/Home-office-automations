# Tailwind CSS

## What it is
Tailwind CSS is an open-source, utility-first CSS framework designed for rapid web user interface development. Instead of providing pre-designed UI components (like buttons or navigation bars with opinionated styling), Tailwind provides low-level utility classes—such as `flex`, `pt-4`, `text-center`, `bg-blue-500`, and `rotate-90`—that developers combine directly within markup (HTML, JSX, Vue, Svelte) to build custom designs without writing raw CSS stylesheet rules.

Operating as a dominant web development standard in early 2027 (especially with Tailwind CSS v4 featuring engine optimizations written in Rust), Tailwind integrates deeply with frontend frameworks like [Next.js](nextjs.md), Vite, React, and [v0.dev](v0dev.md) for generative UI workflows.

## What problem it solves
Traditional CSS approaches suffer from standard maintenance challenges: stylesheet bloat, named class collisions, naming fatigue (BEM methodology overhead), and difficulty predicting side effects when changing global stylesheets. Component frameworks like Bootstrap or Bulma solve UI construction speed but result in rigid, generic design aesthetic unless heavily overridden.

Tailwind CSS solves these issues by shifting styling into atomic utility classes embedded directly within markup:
- **No Class-Naming Fatigue**: Developers do not need to invent abstract class names (e.g., `.sidebar-inner-card-wrapper`).
- **Zero Stylesheet Bloat**: Unused utility classes are automatically pruned at build time via dynamic static analysis, keeping production CSS bundles small (frequently under 10 KB).
- **Safe Modifications**: Styles are scoped directly to the element or component template, making component refactoring isolated and predictable.

## Where it fits in the stack
**Development & Ops / Frontend & UI Styling Layer**. Tailwind CSS sits between user interface markup templates (JSX, TSX, HTML, Vue, Svelte) and browser rendering engines, processing markup classes during development and bundling optimized CSS artifacts during build steps.

## Typical use cases
- **Modern Web Application UI**: Styling responsive web apps built on [Next.js](nextjs.md), React, Vue, or Svelte.
- **Generative UI & Design Systems**: Consuming AI-generated React/Tailwind components from platforms like [v0.dev](v0dev.md) and customizing layout tokens.
- **Micro-Frontend & Component Libraries**: Building consistent, token-driven component design systems with design tokens (colors, spacing, typography).
- **Rapid Prototyping**: Rapidly assembling interface prototypes in HTML or JSX without switching context between markup and external stylesheets.

## Strengths
- **Utility-First Speed**: High velocity UI assembly directly inside markup templates.
- **Automated Purging / JIT Engine**: Generates only the CSS rules actually used in code, producing tiny bundle footprints.
- **Arbitrary Values & Custom Design Tokens**: Supports custom values on-the-fly (e.g., `top-[117px]`, `bg-[#1da1f2]`) and fluid responsive breakpoints (`md:flex`, `lg:grid-cols-4`).
- **Extensive Ecosystem**: Integrated with headless UI libraries (Radix UI, Headless UI, Shadcn UI) and generative AI UI generators.

## Limitations
- **HTML Markup Clutter**: HTML templates can become visually dense with long strings of utility class names.
- **Learning Curve**: Developers must familiarize themselves with utility class names and shorthand properties.
- **Build Step Required**: Requires a compilation pipeline (PostCSS, Vite plugin, or CLI compiler) to process templates into production CSS.

## When to use it
- When building frontend web applications using component frameworks (React, [Next.js](nextjs.md), Vue, Svelte).
- When consuming AI-generated component templates from tools like [v0.dev](v0dev.md) or Claude artifacts.
- When team velocity benefits from eliminating stylesheet context-switching and class-naming conventions.

## When not to use it
- For plain, static HTML pages served without any JavaScript or build tooling where simple vanilla CSS or classless CSS frameworks suffice.
- In legacy monolithic projects with thousands of pre-existing global CSS class hierarchies that cannot tolerate PostCSS or Tailwind build passes.

## Getting started

### Installation
Install Tailwind CSS v4 / Vite plugin in a modern frontend project:

```bash
npm install -D tailwindcss @tailwindcss/vite
```

### Vite / Next.js Configuration
Add Tailwind to your Vite configuration (`vite.config.ts`):

```typescript
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [tailwindcss()],
});
```

Include Tailwind in your base CSS entrypoint (`src/index.css`):

```css
@import "tailwindcss";
```

## CLI examples

### Compiling CSS via Tailwind CLI
```bash
# Process input CSS file and watch for template class changes in src/
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch

# Build production minified bundle with dynamic pruning
npx tailwindcss -i ./src/input.css -o ./dist/output.css --minify
```

## API examples

### Programmatic PostCSS Plugin Invocation
```javascript
import postcss from 'postcss';
import tailwindcss from '@tailwindcss/postcss';
import autoprefixer from 'autoprefixer';

async function compileTailwind(cssString) {
  const result = await postcss([
    tailwindcss(),
    autoprefixer()
  ]).process(cssString, { from: undefined });

  return result.css;
}
```

## Code examples

### React / Next.js Responsive Component with Tailwind Utility Classes
```tsx
import React from 'react';

interface UserCardProps {
  name: string;
  role: string;
  avatarUrl: string;
  status: 'online' | 'offline';
}

export const UserCard: React.FC<UserCardProps> = ({ name, role, avatarUrl, status }) => {
  return (
    <div className="flex flex-col sm:flex-row items-center gap-4 p-6 bg-white dark:bg-slate-900 rounded-xl shadow-md border border-slate-200 dark:border-slate-800 hover:shadow-lg transition-shadow duration-300 max-w-md mx-auto">
      <div className="relative">
        <img
          src={avatarUrl}
          alt={name}
          className="w-16 h-16 rounded-full object-cover border-2 border-indigo-500"
        />
        <span
          className={`absolute bottom-0 right-0 w-4 h-4 rounded-full border-2 border-white dark:border-slate-900 ${
            status === 'online' ? 'bg-emerald-500' : 'bg-slate-400'
          }`}
        />
      </div>
      <div className="text-center sm:text-left flex-1 min-w-0">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white truncate">
          {name}
        </h3>
        <p className="text-sm text-slate-500 dark:text-slate-400">{role}</p>
        <div className="mt-3 flex flex-wrap gap-2 justify-center sm:justify-start">
          <button className="px-3 py-1.5 text-xs font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors focus:ring-2 focus:ring-indigo-500 focus:outline-none">
            Message
          </button>
          <button className="px-3 py-1.5 text-xs font-medium text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors">
            Profile
          </button>
        </div>
      </div>
    </div>
  );
};
```

## Related tools / concepts
- [Next.js](nextjs.md) — Full-stack React framework featuring native Tailwind CSS integration.
- [v0.dev](v0dev.md) — Generative UI tool producing React and Tailwind CSS markup.
- [Material for MkDocs](material-for-mkdocs.md) — Documentation site framework customizable via CSS tokens.

## Sources / references
- [Tailwind CSS Official Website](https://tailwindcss.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS GitHub Repository](https://github.com/tailwindlabs/tailwindcss)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
