---
trigger: glob
globs: frontend/**/*
---
# Next.js & React Best Practices

## Component Architecture
- Use functional components with hooks exclusively
- Keep components small and focused on a single responsibility
- Extract reusable logic into custom hooks in `lib/hooks/`
- Colocate component-specific styles and tests

## TypeScript
- Define interfaces for all props and state
- Avoid `any` type—use `unknown` or proper generics
- Export types alongside components when needed externally
- Use strict TypeScript configuration

## State Management
- Use `useState` for local component state
- Use `SWR` for server state and data fetching (as configured in project)
- Lift state only when necessary for sharing between components
- Use context sparingly for truly global state

## Data Fetching
- Use `SWR` hooks for data fetching with caching
- Handle loading and error states explicitly
- Implement optimistic updates where appropriate
- Configure proper revalidation strategies

## File Structure
- Follow Pages Router conventions (`pages/` directory)
- Use `_app.tsx` for global providers and layouts
- Organize by feature: `components/article/`, `components/comment/`
- Keep API utilities in `lib/api/`

## Performance
- Use dynamic imports for code splitting large components
- Optimize images with Next.js Image component when possible
- Memoize expensive computations with `useMemo`
- Prevent unnecessary re-renders with `React.memo` and `useCallback`

## Styling
- Use CSS modules or consistent styling approach
- Follow mobile-first responsive design
- Maintain consistent spacing and typography
- Keep styles colocated with components

## Error Handling
- Implement error boundaries for graceful failures
- Display user-friendly error messages
- Log errors for debugging
- Handle API errors consistently across components

## Accessibility
- Use semantic HTML elements
- Include proper ARIA attributes when needed
- Ensure keyboard navigation works
- Maintain sufficient color contrast

## Code Style
- Use descriptive component and variable names
- Prefer named exports for components
- Keep JSX readable with proper formatting
- Extract complex conditionals into variables or functions
