import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Button from '../components/Button'

describe('Button Component', () => {
  it('deve renderizar o texto do botão', () => {
    render(<Button>Clique aqui</Button>)
    expect(screen.getByText('Clique aqui')).toBeInTheDocument()
  })

  it('deve chamar onClick quando clicado', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()
    
    render(<Button onClick={handleClick}>Clique</Button>)
    
    await user.click(screen.getByText('Clique'))
    
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})