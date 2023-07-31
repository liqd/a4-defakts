import React, { useState } from 'react'
import django from 'django'

const translated = {
  intro: django.gettext('This comment contains disinformation. Defakts uses an Artificial ' +
  'Intelligence to scan content for disinformation. Disinformation often shows ' +
  'certain characteristics that allow for a reliable identification.'),
  ariaReadMore: django.gettext('Click to view the AI explanation for reporting this comment.'),
  ariaReadLess: django.gettext('Click to hide the AI explanation for reporting this comment.'),
  readMore: django.gettext('Read more'),
  readLess: django.gettext('Read less')
}

export const AiReportExplanation = ({ AiReport }) => {
  const [isExpanded, setIsExpanded] = useState()

  const toggleExpand = () => {
    setIsExpanded(!isExpanded)
  }

  return (
    <li className="alert alert--danger d-flex text-start mb-3">
      <i
        className="fas fa-exclamation-circle text-danger pt-1 pe-2"
        aria-hidden="True"
      />
      <p>
        {translated.intro + ' '}
        {isExpanded && AiReport + ' '}
        <button
          className="btn--link text-danger"
          type="button"
          onClick={toggleExpand}
          aria-label={isExpanded ? translated.ariaReadLess : translated.ariaReadMore}
        >
          {isExpanded ? translated.readLess : translated.readMore}
        </button>
      </p>
    </li>
  )
}
