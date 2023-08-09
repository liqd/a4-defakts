import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import { AiReportExplanation } from '../AiReportExplanation'

test('Snapshot Read More <AiReportExplanation>', () => {
  const { container } = render(
    <AiReportExplanation AiReport="This is the ai report" />
  )
  expect(container).toMatchSnapshot()
})

test('Snapshot Read Less <AiReportExplanation>', () => {
  const { container } = render(
    <AiReportExplanation AiReport="This is the ai report" />
  )
  const button = screen.getByRole('button')
  fireEvent.click(button)
  expect(container).toMatchSnapshot()
})

test('Render <AiReportExplanation>', () => {
  render(<AiReportExplanation AiReport="This is the ai report" />)
  const comment = screen.getByText('Read more')
  expect(comment).toBeTruthy()
})

test('Read More <AiReportExplanation>', () => {
  render(<AiReportExplanation AiReport="This is the ai report" />)
  const readMore = screen.getByText('Read more')
  expect(readMore).toBeTruthy()
  const button = screen.getByRole('button')
  expect(button).toBeTruthy()
  fireEvent.click(button)
  const readLess = screen.getByText('Read less')
  expect(readLess).toBeTruthy()
})
