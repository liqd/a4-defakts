import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import { AiReportExplanation } from '../AiReportExplanation'

test('Snapshot to confirm Read More is rendered <AiReportExplanation>', () => {
  const { container } = render(
    <AiReportExplanation AiReport="This is the ai report" />
  )
  expect(container).toMatchSnapshot()
})

test('Snapshot to confirm Read Less is rendered after clicking Read More button <AiReportExplanation>', () => {
  const { container } = render(
    <AiReportExplanation AiReport="This is the ai report" />
  )
  const button = screen.getByRole('button')
  fireEvent.click(button)
  expect(container).toMatchSnapshot()
})

test('Test render <AiReportExplanation> with Read More button', () => {
  render(<AiReportExplanation AiReport="This is the ai report" />)
  const comment = screen.getByText('Read more')
  expect(comment).toBeTruthy()
})

test('Test functionality of Read More <AiReportExplanation>', () => {
  render(<AiReportExplanation AiReport="This is the ai report" />)
  const readMore = screen.getByText('Read more')
  expect(readMore).toBeTruthy()
  const button = screen.getByRole('button')
  expect(button).toBeTruthy()
  fireEvent.click(button)
  const readLess = screen.getByText('Read less')
  expect(readLess).toBeTruthy()
})
