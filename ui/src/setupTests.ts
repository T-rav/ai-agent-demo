// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// Mock scrollIntoView for tests
Object.defineProperty(Element.prototype, 'scrollIntoView', {
  value: jest.fn(),
  writable: true,
});

// Mock ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

// Mock fetch for tests
global.fetch = jest.fn();

// Mock TextEncoder/TextDecoder
const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Mock axios
jest.mock('axios', () => ({
  __esModule: true,
  default: {
    post: jest.fn(() => Promise.resolve({ data: {} })),
    isAxiosError: jest.fn(() => false),
  },
}));
