import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'
import '@testing-library/jest-dom'

// Limpa após cada teste
afterEach(() => {
  cleanup()
})