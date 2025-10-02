import { render, RenderOptions } from '@testing-library/react';
import { ReactElement } from 'react';

// Custom render function that can be extended with providers if needed
const customRender = (ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) =>
  render(ui, { ...options });

export * from '@testing-library/react';
export { customRender as render };

// Export builders and factories for easy access
export * from './builders';
export * from './factories';
